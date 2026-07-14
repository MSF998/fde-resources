# Langchain

**Date:** 2026-14-14 | **Track:** Technical | **Session:** XX

## Key Concepts

### Principles to remeber while building any AI app

1. Who is talking (Session ID)
2. What should the your model see
3. Structure of the information
4. How much history should LLM see
5. What happens when we scale

### Tool Calling in Langchain

- Tool calling without langchain

```python
user_query = input("Enter your query: ")
prompt = f"""Imagine you're a helpful assistant, answer the user query-
I have a function 'weather_api' return the name of 'weather_api' only with no other text if the user asks a weather related question else answer normally
The function has no args, and returns the temperature in string format.
User query -
{user_query}"""
response = llm.invoke(prompt)
if(response.content == 'weather_api'):
  output = weather_api()
  new_query = user_query + response.content + f"Function output :{output}"
  response = llm.invoke(new_query)
  print(response.content)

else:
  response.content
```

- Langchain tool defination

```python
from langchain_core.tools import tool

@tool
def get_city_weather(city: str):
    """
    Fetches the current weather conditions for a specified city.

    Use this tool whenever a user asks about the weather, temperature,
    or humidity in a specific location.

    Args:
        city (str): The name of the city to check the weather for.
                    Examples: "Delhi", "Mumbai", "Bengaluru", "New York".

    Returns:
        dict: A dictionary containing the weather details with the following keys:
            - temperature (int): The current temperature in degrees Celsius.
            - humidity (int): The relative humidity percentage.
            - condition (str): A brief, readable description of the weather
                               (e.g., "Hot", "Humid", "Pleasant", "Unknown").
    """
    fake_weather_db = {
        "Delhi": {"temperature": 34, "humidity": 48, "condition": "Hot"},
        "Mumbai": {"temperature": 31, "humidity": 78, "condition": "Humid"},
        "Bengaluru": {"temperature": 27, "humidity": 60, "condition": "Pleasant"},
    }
    return fake_weather_db.get(
        city,
        {"temperature": 30, "humidity": 50, "condition": "Unknown"}
    )

# We call it using
get_city_weather.invoke({"city":"Delhi"})
# {'temperature': 34, 'humidity': 48, 'condition': 'Hot'}
```

- maintain tool instruction in the doc string of the function which will be appended to the llm's system prompt
- maintain a tool repo as dict. where the key is the tool name and value is the tool
  - ```python
      tool_repo = {'get_city_weather': get_city_weather, 'add_two_number': add_two_number}
    ```

- bind tools with llm object example

```python
sysmsg = "Imagine you're a helpful travel assistant, please answer the query carefuly, call the tools if necessary, don't followup just answer"
from langchain.messages import HumanMessage, SystemMessage, ToolMessage

# Defining your LLM
llm = ChatOpenAI(
    model="gpt-5-mini"
)
#Tell your LLM about tools available. it holds	Schema/Description
llm_with_tools = llm.bind_tools([get_city_weather])
query = "What is the weather like in Delhi?"
messages_to_send = [sysmsg] + [HumanMessage(query)]
response = llm_with_tools.invoke(messages_to_send)

# Tool call is supposed to be done by langchain not the llm
tool_details = response.tool_calls[0]
tool_message = tool_repo[tool_name].invoke(tool_details)
messages_to_send.append(response)
messages_to_send.append(tool_message)
llm.invoke(messages_to_send).content
```

- polished way of tool calling

```python
message_to_send = []
sysmsg = "IMagine you're a helpful travel assistant, please answer the query carefuly, call the tools if necessary, don't followup just answer"
from langchain.messages import HumanMessage, SystemMessage, ToolMessage

# Defining your LLM
llm = ChatOpenAI(
    model="gpt-5-mini"
)
#Tell your LLM about tools available
llm_with_tools = llm.bind_tools([get_city_weather])

# Make your system prompt
system_message = SystemMessage(content = sysmsg)
# Make your user prompt
user_query = input("Please enter your message: ")
print()
user_message = HumanMessage(content = user_query)

# COmbine the messages
messages_to_send = [system_message, user_message]


response = llm_with_tools.invoke(messages_to_send)

# Append the AI message
messages_to_send.append(response)

if(response.tool_calls):
  # Get details of the first tool
  tool_details = response.tool_calls[0]
  # GEt the name of the tool to call
  tool_name = tool_details['name']
  # Calling that tool from repo with all tool details
  tool_output = tool_repo[tool_name].invoke(tool_details) # Ooutput will be tool message

  messages_to_send.append(tool_output)
  response = llm_with_tools.invoke(messages_to_send)
  print(response.content)
else:
  print(response.content)
```

- langhcain structured tools and multiple tool calls

```python
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
  # This is already a LangChain tool
duckduckgo_search = DuckDuckGoSearchRun()
tools = [
    get_city_weather,
    duckduckgo_search
]

tool_repo = {
    tool.name: tool
    for tool in tools
}
# tool_repo output
# {'get_city_weather': StructuredTool(name='get_city_weather', description='Fetches the current weather conditions for a specified city.\n\nUse this tool whenever a user asks about the weather, temperature,\nor humidity in a specific location.\n\nArgs:\n    city (str): The name of the city to check the weather for.\n                Examples: "Delhi", "Mumbai", "Bengaluru", "New York".\n\nReturns:\n    dict: A dictionary containing the weather details with the following keys:\n        - temperature (int): The current temperature in degrees Celsius.\n        - humidity (int): The relative humidity percentage.\n        - condition (str): A brief, readable description of the weather\n                           (e.g., "Hot", "Humid", "Pleasant", "Unknown").', args_schema=<class 'langchain_core.utils.pydantic.get_city_weather'>, func=<function get_city_weather at 0x7aa1cef22700>),
#  'duckduckgo_search': DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper(region='wt-wt', safesearch='moderate', time='y', max_results=5, backend='auto', source='text'))}
message_to_send = []
sysmsg = "IMagine you're a helpful travel assistant, please answer the query carefuly, call the tools if necessary, don't followup just answer"

# Defining your LLM
llm = ChatOpenAI(
    model="gpt-5-mini"
)
#Tell your LLM about tools available
llm_with_tools = llm.bind_tools([get_city_weather])

# Make your system prompt
system_message = SystemMessage(content = sysmsg)
# Make your user prompt
user_query = input("Please enter your message: ")
print()
user_message = HumanMessage(content = user_query)

# COmbine the messages
messages_to_send = [system_message, user_message]


response = llm_with_tools.invoke(messages_to_send)

# Append the AI message
messages_to_send.append(response)

if(response.tool_calls):
  # Get details of the first tool
  for tool_details in response.tool_calls:
  # GEt the name of the tool to call
  tool_name = tool_details['name']
  # Calling that tool from repo with all tool details
  tool_output = tool_repo[tool_name].invoke(tool_details) # Ooutput will be tool message

  messages_to_send.append(tool_output)
  response = llm_with_tools.invoke(messages_to_send)
  print(response.content)
else:
  print(response.content)
  messages_to_send.append(response)
```

## What I Built / Tried

-

## Insights & Opinions

-

## Questions / Gaps

-

## Links to Projects

-
