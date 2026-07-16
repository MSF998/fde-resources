# Langchain & Pydantic

**Date:** 2026-17-16 | **Track:** Technical | **Session:** XX

## Key Concepts

- When the number of tools increase we bring in the concept of Agents
- Or we can have a planner LLM (Orchestrator)
  - We only tell it about tools but not access to it
  - It will only give out a path/execution plan
  - The plan will be given to the tool bound LLM

### Chat prompt template

```python
from langchain_core.prompts import ChatPromptTemplate

order_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract the following information from the restaurant kiosk conversation:

- items: item name and quantity
- special_instruction
- order_type
- payment_method
- discount_percent

Do not invent missing information.
Return the extracted information clearly.
"""
    ),
    (
        "human",
        "Conversation:\n{conversation}"
    )
])

order_chain = order_prompt | llm

response = order_chain.invoke({
    "conversation": order_1
})

print(response.content)
```

```python
order_prompt.invoke({"conversation": "Hi"})

# Output:
# ChatPromptValue(messages=[SystemMessage(content='\nExtract the following information from the restaurant kiosk conversation:\n\n- items: item name and quantity\n- special_instruction\n- order_type\n- payment_method\n- discount_percent\n\nDo not invent missing information.\nReturn the extracted information clearly.\n', additional_kwargs={}, response_metadata={}), HumanMessage(content='Conversation:\nHi', additional_kwargs={}, response_metadata={})])
```

- Improving the prompt

```python
from langchain_core.prompts import ChatPromptTemplate

order_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract the order information from the restaurant kiosk conversation.

Return only a Python dictionary in exactly this structure:

{{
    "items": [
        {{
            "name": "item name",
            "quantity": 1
        }}
    ],
    "special_instruction": "instruction",
    "order_type": "dine_in or takeaway",
    "payment_method": "cash, card or upi",
    "discount_percent": 10,
}}

Rules:
- quantity must be an integer.
- discount_percent must be a number or null.
- discount_requested must be true or false.
- Use null when information is missing.
- Do not invent information.
- Do not add explanations or Markdown.
"""
    ),
    (
        "human",
        "Conversation:\n{conversation}"
    )
])

order_chain = order_prompt | llm

response = order_chain.invoke({
    "conversation": order_1
})

print(response.content)
# Output:

{
    "items": [
        {
            "name": "paneer wrap",
            "quantity": 2
        },
        {
            "name": "cold coffee",
            "quantity": 1
        }
    ],
    "special_instruction": "Make one wrap without onions.",
    "order_type": "takeaway",
    "payment_method": "upi",
    "discount_percent": 10
}
```

- We use two curly braces to escape LCEL syntax. One curly is what langchain thinks as an input. Two curly escapes it

- LLMs cannot maintain consistency due their probabilistic nature
- Enter pydantic to maintain structure information

### Pydantic

- A python class is simply a customized data structure
- ```python
    from pydantic import BaseModel, Field
    from typing import Literal

    class Order(BaseModel):
    name: str
    quantity: int = Field(gt=0)
  ```

- `Field` is used to desribe the variable
- Calling it with LLM

```python
    structured_llm = llm.with_structured_output(OrderItem)
    response = structured_llm.invoke(
    "The customer ordered three paneer wraps."
    )
    response.model_dump()
    # {'name': 'Paneer Wrap', 'quantity': 3}

```

- Langchain is going to convert the pydantic schema into a prompt and give to the LLM
- Pydantic validates the output which the LLM generates

- A complete approach

```python
from pydantic import BaseModel, Field
from typing import Literal

class KioskOrder(BaseModel):
    items: list[OrderItem] # Takes in multiple orders
    special_instruction: str | None = None
    order_type: Literal["dine_in", "takeaway"]
    payment_method: Literal["cash", "card", "upi"]
    discount_percent: int | None = Field(default=None, ge=0, le=100)
```

- langchain tool with sql

```python
import sqlite3
from langchain_core.tools import tool

@tool
def place_order(items: list[dict], order_type: str,
                payment_method: str, discount_percent: int = 0):
    """Calculate and save a restaurant order."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        saved_items, subtotal = [], 0

        for item in items:
            row = conn.execute(
                "SELECT price FROM menu_items WHERE item_code = ?",
                (item["item_code"],)
            ).fetchone()

            if not row:
                return {"status": "failed", "reason": f"Invalid item: {item['item_code']}"}

            price = row[0]
            line_total = price * item["quantity"]
            subtotal += line_total
            saved_items.append((item["item_code"], item["quantity"], price, line_total))

        total = round(subtotal * (1 - discount_percent / 100))

        cur = conn.execute("""
            INSERT INTO orders
            (order_type, payment_method, discount_percent, total_amount)
            VALUES (?, ?, ?, ?)
        """, (order_type, payment_method, discount_percent, total))

        order_id = cur.lastrowid

        conn.executemany("""
            INSERT INTO order_items
            (order_id, item_code, quantity, unit_price, line_total)
            VALUES (?, ?, ?, ?, ?)
        """, [(order_id, *item) for item in saved_items])

    return {"order_id": order_id, "status": "placed", "total_amount": total}

```

- pydantic schema for order

```python
class OrderItem(BaseModel):
    item_code: Literal[
        "paneer_tikka", "paneer_wrap", "veg_burger",
        "french_fries", "cold_coffee"
    ]
    quantity: int = Field(gt=0)


class KioskOrder(BaseModel):
    items: list[OrderItem]
    order_type: Literal["dine_in", "takeaway"]
    payment_method: Literal["cash", "card", "upi"]
    discount_percent: int = Field(default=0, ge=0, le=100)
```

- binding tool

```python
structured_llm = llm.with_structured_output(KioskOrder)
tool_llm = llm.bind_tools([place_order])
```

- Extracting the order

```python
extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the restaurant order. Use menu item codes. Stick to the definition and values"),
    ("human", "{conversation}")
])

extract_chain = extract_prompt | structured_llm

order = extract_chain.invoke({"conversation": order_1})
print(order)

# items=[OrderItem(item_code='paneer_wrap', quantity=2), OrderItem(item_code='cold_coffee', quantity=1)] order_type='takeaway' payment_method='upi' discount_percent=10

order.model_dump()
# {'items': [{'name': 'PWRAP', 'quantity': 2},
#   {'name': 'CCOFFEE', 'quantity': 1}],
#  'special_instruction': 'Make one wrap without onions.',
#  'order_type': 'takeaway',
#  'payment_method': 'upi',
#  'discount_percent': 10}
```

- placing the order

```python
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, ToolMessage
import json

tool_prompt = ChatPromptTemplate.from_messages([
    ("system", "Place the order using the tool. After it is saved, confirm briefly."),
    MessagesPlaceholder("messages")
])

tool_chain = tool_prompt | tool_llm

user_message = HumanMessage(
    content=f"Place this order:\n{order.model_dump_json()}"
)

tool_request = tool_chain.invoke({
    "messages": [user_message]
})

print(tool_request.tool_calls)
#[{'name': 'place_order', 'args': {'items': [{'item_code': 'paneer_wrap', 'quantity': 2}, {'item_code': 'cold_coffee', 'quantity': 1}], 'order_type': 'takeaway', 'payment_method': 'upi', 'discount_percent': 10}, 'id': 'call_RsGwgRyDDRRa7I94NzdjsaZj', 'type': 'tool_call'}]

import json
from langchain_core.messages import HumanMessage, ToolMessage

messages = [
    HumanMessage(content=f"Place this order:\n{order.model_dump_json()}")
]

while True:
    response = tool_chain.invoke({"messages": messages})
    messages.append(response)

    if not response.tool_calls:
        print(response.content)
        break

    for call in response.tool_calls:
        tool_output = place_order.invoke(call["args"])

        messages.append(
            ToolMessage(
                content=json.dumps(tool_output),
                tool_call_id=call["id"]
            )
        )

# Your order has been successfully placed with order ID 12. The total amount is 450.

```

- Instead of mutiple LLM calls we can integrate the tool itself with Pydantic
- **Bind the tool with Pydantic**
  ```python
  @tool(args_schema=KioskOrder)
  ```

```python
import sqlite3
from langchain_core.tools import tool

@tool(args_schema=KioskOrder)
def place_order(items: list[OrderItem], order_type: str,
                payment_method: str, discount_percent: int = 0):
    """Calculate and save a restaurant order."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        saved_items, subtotal = [], 0

        for item in items:
            row = conn.execute(
                "SELECT price FROM menu_items WHERE item_code = ?",
                (item.item_code,)
            ).fetchone()

            if not row:
                return {"status": "failed",
                        "reason": f"Invalid item: {item.item_code}"}

            price = row[0]
            line_total = price * item.quantity
            subtotal += line_total
            saved_items.append(
                (item.item_code, item.quantity, price, line_total)
            )

        total = round(subtotal * (1 - discount_percent / 100))

        cur = conn.execute("""
            INSERT INTO orders
            (order_type, payment_method, discount_percent, total_amount)
            VALUES (?, ?, ?, ?)
        """, (order_type, payment_method, discount_percent, total))

        order_id = cur.lastrowid

        conn.executemany("""
            INSERT INTO order_items
            (order_id, item_code, quantity, unit_price, line_total)
            VALUES (?, ?, ?, ?, ?)
        """, [(order_id, *item) for item in saved_items])

    return {
        "order_id": order_id,
        "status": "placed",
        "total_amount": total
    }
```

- converting the while loop to a langhchain object and build a chain
- create a function for the while loop and convert it into a runable lambda
- runnable lamda is a function converted to work with langchain

- tool repo

  ```python
  from langchain_core.prompts import ChatPromptTemplate
  from langchain_core.runnables import RunnableLambda

  tools = [place_order]
  tools_repo1 = {tool.name: tool for tool in tools}
  tool_llm1 = llm.bind_tools(tools)

  prompt = ChatPromptTemplate.from_messages([
      (
          "system",
          "Place the kiosk order using the tool. "
          "Use valid menu item codes. "
          "After the tool succeeds, confirm the order briefly."
      ),
      ("human", "{conversation}")
  ])
  ```

- while loop within a function

```python
def run_tool_loop(response):
    messages = [response]

    while response.tool_calls:
        for tool_call in response.tool_calls:
            tool = tools_repo1[tool_call["name"]]

            # Full ToolCall goes in; ToolMessage comes out
            tool_message = tool.invoke(tool_call)
            messages.append(tool_message)

        response = tool_llm1.invoke(messages)
        messages.append(response)

    return response
```

- **langhchain order chain**

```python
order_chain = (
    prompt
    | tool_llm1
    | RunnableLambda(run_tool_loop)
)
```

- complete flow

```python
order_text = """
Customer: Give me two paneer tikkas and one cold coffee.
This is takeaway, I will pay by UPI.
Apply a 10 percent discount.
"""


result = order_chain.invoke({
    "conversation": order_text
})

print(result.content)
```

- Emailing Syntax

```python
from google.colab import userdata

GMAIL_ADDRESS = userdata.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = userdata.get("GMAIL_APP_PASSWORD")
CHEF_EMAIL = userdata.get("CHEF_EMAIL")

import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = GMAIL_ADDRESS
msg["To"] = CHEF_EMAIL
msg["Subject"] = "Test order"
msg.set_content("Two paneer tikkas and one cold coffee.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    smtp.send_message(msg)

print("Email sent")
```

- pydantic class for the email to the chef

```python
class SendEmailInput(BaseModel):
    items: list[OrderItem]
    special_request: str | None = None
```

- email

```python
@tool(args_schema=SendEmailInput)
def send_order_email(
    items: list[OrderItem],
    special_request: str | None = None
):
    """Send order details to the chef."""

    item_lines = "\n".join(
        f"- {item.item_code}: {item.quantity}"
        for item in items
    )

    msg = EmailMessage()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = CHEF_EMAIL
    msg["Subject"] = "New Restaurant Order"
    msg.set_content(
        f"Items:\n{item_lines}\n\n"
        f"Special request: {special_request or 'None'}"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)

    return {"status": "email_sent"}
```

- repo and binding

```python
tool_llm2 = llm.bind_tools([send_order_email])
tools_repo2 = {"send_order_email": send_order_email}

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Read the order, call send_order_email, and confirm after it succeeds."
    ),
    ("human", "{conversation}")
])

def run_tools(response):
    messages = [response]

    while response.tool_calls:
        for call in response.tool_calls:
            tool_message = tools_repo2[call["name"]].invoke(call)
            messages.append(tool_message)

        response = tool_llm2.invoke(messages)
        messages.append(response)

    return response
```

- chain

```python
email_chain = prompt | tool_llm2 | RunnableLambda(run_tools)

order_text = """
Give me two paneer tikkas and one cold coffee.
Make the paneer tikka less spicy.
"""

result = email_chain.invoke({"conversation": order_text})

print(result.content)
```

- **building parallel chains**

```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    order_result=order_chain,
    email_result=email_chain
)
result = parallel_chain.invoke({
    "conversation": order_text
})
```

### Off topic

- How to mount google drive to collab

```python
from google.colab import drive
drive.mount("/content/drive")
```

- sqlite in collab and stored in G drive

```python
DB_PATH = "/content/drive/MyDrive/restaurant.db"

conn = sqlite3.connect(DB_PATH)

pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
""", conn)
```
