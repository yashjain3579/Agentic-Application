# Agentic App

A simple and smart autonomous agent that understands what you're asking and executes multi-step operations for you. Just tell it what you want in plain English!

## What Does It Do?

Imagine you want to do complex calculations or string operations. Instead of writing code for each step, you just tell the agent what you want in natural language and it figures out the rest.

For example:
- \Add 5 and 10, then multiply by 2\ ? Returns 30
- \Add 100 and 50, then divide by 3\ ? Returns 50
- \Multiply 5 by 4, then to the power of 2\ ? Returns 400

## Getting Started

### Installation

It's super simple - no complicated dependencies to install!

\\\ash
# Clone the repository
git clone https://github.com/yashjain3579/Agentic-Application.git
cd Agentic-Application

# That's it! No pip install needed for basic usage
# (Only if you want to run tests, install pytest)
pip install pytest
\\\

### Quick Example

Let's try it out:

\\\python
from agentic_app import create_app

# Create the agent
app = create_app()

# Ask it to do something
result = app.query(\"Add 5 and 10\")
print(result)  # Output: 15

# Try a more complex operation
result = app.query(\"Add 5 and 10, then multiply by 2\")
print(result)  # Output: 30

# Even more complex
result = app.query(\"Add 100 and 50, then divide by 3, then to the power of 2\")
print(result)  # Output: 2500
\\\

### See It In Action

Create a file called \	est_it.py\:

\\\python
from agentic_app import create_app

app = create_app(verbose=True)

print(\"\\n--- Test 1: Simple Addition ---\")
result = app.query(\"Add 5 and 10\")
print(f\"Result: {result}\\n\")

print(\"--- Test 2: Chained Operations ---\")
result = app.query(\"Add 1 and 1, then multiply by 10, then subtract 2\")
print(f\"Result: {result}\\n\")

print(\"--- Test 3: Power Operation ---\")
result = app.query(\"2 to the power of 8\")
print(f\"Result: {result}\\n\")
\\\

Run it:
\\\ash
python test_it.py
\\\

## What Commands Does It Understand?

The agent understands these operations:

\\\
Arithmetic:
  - \"Add 5 and 10\" ? 15
  - \"Subtract 5 from 20\" ? 15
  - \"Multiply 5 and 4\" ? 20
  - \"Divide 20 by 4\" ? 5
  - \"2 to the power of 3\" ? 8

String Operations:
  - \"Concatenate hello and world\" ? helloworld
  - \"Uppercase hello\" ? HELLO
  - \"Lowercase HELLO\" ? hello
  - \"Length of hello\" ? 5

Conversions:
  - \"To integer 5.5\" ? 5
  - \"To float 5\" ? 5.0
  - \"To string 123\" ? \"123\"
\\\

## How To Chain Commands

Use \"then\" to chain operations:

\\\python
# Do this step, then that step, then the other step
result = app.query(\"Add 10 and 5, then multiply by 2, then to the power of 2\")
print(result)  # ((10 + 5) * 2)^2 = 60000
\\\

## Project Structure

\\\
Agentic-Application/
+-- agentic_app/           # The main code
¦   +-- __init__.py        # Package setup
¦   +-- tools.py           # All the tools (18 total)
¦   +-- agent.py           # The smart brain
¦   +-- app.py             # Easy-to-use API
¦
+-- tests/                 # Tests to make sure it works
¦   +-- __init__.py
¦   +-- test_agentic_app.py  # 39 tests
¦
+-- README.md              # This file
+-- requirements.txt       # Dependencies
+-- .gitignore             # Git stuff
\\\

## Features

 **Natural Language**: Just speak what you want  
 **Smart Chaining**: Automatically connects operations  
 **18 Built-in Tools**: Arithmetic, strings, conversions  
 **Add Your Own**: Easy to create custom tools  
 **Well Tested**: 39 tests, all passing  
 **Zero Dependencies**: No external packages needed  
 **Simple Code**: Clean, readable, ~500 lines  

## Running Tests

Want to make sure everything works?

\\\ash
pip install pytest
python -m pytest tests/ -v
\\\

You should see:
\\\
39 passed in 0.XX seconds ?
\\\

## Need More Help?

### Register Custom Tools

Want to add your own operation? Easy!

\\\python
from agentic_app import create_app
from agentic_app.tools import Tool, ToolParameter, ToolType

app = create_app()

# Create a custom tool
square_tool = Tool(
    name=\"square\",
    description=\"Square a number\",
    func=lambda x: x ** 2,
    parameters=[ToolParameter(\"x\", \"float\")],
    tool_type=ToolType.ARITHMETIC,
)

# Register it
app.register_tool(square_tool)

# Use it
tool = app.tool_registry.get(\"square\")
result = tool.invoke(x=5)
print(result)  # 25
\\\

### List All Available Tools

\\\python
app = create_app()
tools = app.list_tools()
for tool in tools:
    print(f\"{tool.name}: {tool.description}\")
\\\

## Requirements

- **Python**: 3.8 or newer
- **Dependencies**: None! (pytest is optional for testing)
- **OS**: Windows, Mac, or Linux

## Author

Yash Jain (@yashjain3579)

---

**Happy Querying!**
