# Jinja2 Prompting & Prompt Management Notes

## 1. Jinja2 for Prompt Templating

**Why:** Separates prompt logic (conditionals, loops, includes) from Python code. Great for RAG/agent prompts with variable context, few-shot examples, etc.

### Basic Template

```python
from jinja2 import Template

tpl = Template("""
You are {{ role }}.

Context:
{% for doc in docs %}
- {{ doc }}
{% endfor %}

{% if strict %}
Answer ONLY from context above.
{% endif %}

Question: {{ question }}
""")

prompt = tpl.render(
    role="a fiqh assistant",
    docs=["Hadith 1...", "Hadith 2..."],
    strict=True,
    question="What breaks wudu?"
)
```

### File-Based Templates (recommended)

```
prompts/
  system/
    v1_rag_qa.j2
    v2_rag_qa.j2
  agent/
    v1_tool_call.j2
```

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("prompts/"))
tpl = env.get_template("system/v2_rag_qa.j2")
prompt = tpl.render(question=q, docs=docs)
```

### Reusable Blocks (inheritance)

```jinja
{# base.j2 #}
{% block persona %}You are a helpful assistant.{% endblock %}
{% block rules %}{% endblock %}
```

```jinja
{# v2_rag_qa.j2 #}
{% extends "base.j2" %}
{% block persona %}You are a precise RAG QA agent.{% endblock %}
{% block rules %}
- Cite sources
- Say "I don't know" if unsure
{% endblock %}
```

### Macros (few-shot examples)

```jinja
{% macro example(q, a) %}
Q: {{ q }}
A: {{ a }}
{% endmacro %}

{{ example("What is zakat?", "A mandatory charity...") }}
{{ example("What is nisab?", "The minimum threshold...") }}
```

---

## 2. Prompt Versioning Strategies

### A. File naming (simplest)

`v1_extract.j2`, `v2_extract.j2` → track in git, diff via git log.

### B. Metadata header in template

```jinja
{#
version: 2.3.0
author: msf
changelog: added citation requirement
model_tested: gemini-2.5-flash
#}
You are...
```

Parse it out at load time for logging/observability (pairs well with LangSmith).

### C. Registry pattern (production-grade)

```python
import yaml, hashlib

class PromptRegistry:
    def __init__(self, path="prompts/registry.yaml"):
        self.registry = yaml.safe_load(open(path))

    def get(self, name, version="latest"):
        entry = self.registry[name][version]
        tpl = env.get_template(entry["file"])
        return tpl, entry["version"]

    def render(self, name, version="latest", **kwargs):
        tpl, v = self.get(name, version)
        rendered = tpl.render(**kwargs)
        hash_ = hashlib.md5(rendered.encode()).hexdigest()[:8]
        return rendered, {"prompt_version": v, "hash": hash_}
```

```yaml
# registry.yaml
rag_qa:
  latest: { file: "system/v2_rag_qa.j2", version: "2.3.0" }
  v1: { file: "system/v1_rag_qa.j2", version: "1.0.0" }
```

Log `prompt_version` + `hash` alongside every LLM call → correlate prompt version with output quality in LangSmith.

### D. DB-backed versioning

Store templates in Postgres/SQLite with `(name, version, content, created_at, is_active)` — enables rollback without redeploying code.

### Best Practices

- Never hardcode prompts inline in agent code — always load from `.j2` files.
- Use semantic versioning (major = behavior change, minor = wording tweak).
- Log `{template_name, version, hash, rendered_vars}` on every call for reproducibility.
- Keep one template per responsibility (system prompt, tool-call prompt, summarization prompt).

---

## 3. Working with `docs` in RAG Prompts

### Structured objects, not raw strings

```python
docs = [
    {"id": "hadith_142", "source": "Sahih Bukhari", "text": "...", "score": 0.91},
    {"id": "fiqh_009", "source": "Al-Muwatta", "text": "...", "score": 0.87},
]
```

Lets the template control formatting, citation, and filtering.

### Render with metadata (citations / grounding)

```jinja
Context:
{% for doc in docs %}
[{{ loop.index }}] Source: {{ doc.source }} (id: {{ doc.id }})
{{ doc.text }}
{% endfor %}

Cite sources using [number] when you use them.
```

Built-in loop helpers: `loop.index`, `loop.first`, `loop.last`.

### Filter/sort inside the template

```jinja
{% for doc in docs | sort(attribute='score', reverse=True) if doc.score > 0.75 %}
[{{ loop.index }}] {{ doc.text }}
{% endfor %}
```

Useful for CRAG (Corrective RAG) filtering without touching Python code.

### Truncate long docs (token budget control)

```jinja
{% for doc in docs %}
{{ doc.text[:500] }}{% if doc.text|length > 500 %}...{% endif %}
{% endfor %}
```

Better to truncate in Python first — Jinja only does character slicing, not token counting.

### Madhhab-aware conditional grouping

```jinja
{% for madhhab, group in docs | groupby('madhhab') %}
### {{ madhhab }} view:
{% for doc in group %}
- {{ doc.text }}
{% endfor %}
{% endfor %}
```

`groupby` separates Hanafi/Shafi'i/etc. opinions cleanly in the prompt structure.

### Empty-context handling

```jinja
{% if docs %}
Context:
{% for doc in docs %}{{ doc.text }}{% endfor %}
{% else %}
No relevant context found. Say you don't have enough information.
{% endif %}
```

Prevents hallucination when retrieval returns nothing (Self-RAG style guardrail).

**Key filters:** `sort`, `groupby`, `selectattr`, `rejectattr`, `unique`, `truncate`, `join`.

---

## 4. `docs` Are Structured Data, Not Files

Jinja never touches raw `.pdf`/`.docx` files — it only renders plain dicts/lists/strings that Python hands it.

### The pipeline

```
PDF/DOCX file
    → parsed & chunked (LangChain loaders, PyPDF, etc.)
    → embedded → stored in vector DB
    → retrieved at query time as text chunks + metadata
    → THAT is what "docs" means in the Jinja template
```

A "doc" by the time it reaches Jinja:

```python
{
    "id": "hadith_142",
    "source": "Sahih Bukhari",   # which file it came from
    "text": "...",                 # the extracted chunk of text
    "score": 0.91,                  # similarity score
    "madhhab": "Hanafi"
}
```

### File handling happens before Jinja

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("fiqh_book.pdf")
pages = loader.load()   # returns LangChain Document objects

# Each Document has:
# page.page_content  -> the text
# page.metadata       -> {"source": "fiqh_book.pdf", "page": 12}
```

Mapping LangChain `Document` objects into plain dicts for the template:

```python
docs = [
    {"text": d.page_content, "source": d.metadata["source"], "score": s}
    for d, s in retrieved_results
]
```

**Flow summary:** file → text extraction → chunking → vector search → plain dict/list → Jinja template (pure string rendering, no file I/O).
