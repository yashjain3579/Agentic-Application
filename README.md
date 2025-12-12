# Agentic App

A simple and smart autonomous agent that understands what you're asking and executes multi-step operations for you. Just tell it what you want in plain English!

## What Does It Do?

Imagine you want to do complex calculations or string operations. Instead of writing code for each step, you just tell the agent what you want in natural language and it figures out the rest.

For example:
- `Add 5 and 10, then multiply by 2` → Returns 30
- `Add 100 and 50, then divide by 3` → Returns 50
- `Multiply 5 by 4, then to the power of 2` → Returns 400

---

## Quick Start (Copy & Paste These Commands)

### Step 1: Clone the Repo

```bash
git clone https://github.com/yashjain3579/Agentic-Application.git
cd Agentic-Application
```

### Step 2: Test It (Choose ONE)

#### Option A: Quick Test (Run Included test.py)

```bash
python test.py
```

**You should see:**
```
Test 1: Add 5 and 10
Result: 15

Test 2: Add 5 and 10, then multiply by 2
Result: 30

Test 3: Multiply 5 and 4, then to the power of 2
Result: 400

All basic tests passed!
```

#### Option B: Detailed Test (See Each Step)

```bash
python test_detailed.py
```

**You should see each operation with detailed steps:**
```
============================================================
TEST 1: Simple Math
============================================================
[Step details shown here...]
Final Result: 15
```

#### Option C: Command Line (Try Any Operation)

Run any operation directly without changing files:

```bash
python -m agentic_app "Add 5 and 10"
```

**Output:**
```
Result: 15
```

More examples:
```bash
python -m agentic_app "Multiply 10 and 5, then divide by 2"
# Result: 25

python -m agentic_app "Add 10 and 5, then multiply by 2, then to the power of 2"
# Result: 900

python -m agentic_app "Uppercase hello world"
# Result: HELLO WORLD
```

#### Option D: Full Test Suite (39 Tests)

```bash
pip install pytest
python -m pytest tests/ -v
```

**You should see:**
```
======================== 39 passed in 0.XX seconds ========================
```

### Which Option To Choose?

| Option | What It Does | Time |
|--------|-------------|------|
| **A** | Pre-made tests - SIMPLEST! | 1 sec |
| **B** | See step-by-step execution | 2 sec |
| **C** | Try custom operations | Real-time |
| **D** | Run all 39 tests | 5 sec |

**Recommendation:** Start with **Option A** - just run it!

---

## What Commands Does It Understand?

### Arithmetic Operations

```
Add 5 and 10              → 15
Subtract 5 from 20        → 15
Multiply 5 and 4          → 20
Divide 20 by 4            → 5
2 to the power of 3       → 8
Square 5                  → 25
Square root of 16         → 4
```

### String Operations

```
Uppercase hello           → HELLO
Lowercase HELLO           → hello
Length of hello           → 5
Concatenate hello world   → helloworld
Replace hello with hi     → hi
```

### Chaining Operations (Use "then")

```
Add 5 and 10, then multiply by 2
→ (5 + 10) * 2 = 30

Multiply 10 and 5, then divide by 2
→ (10 * 5) / 2 = 25

Add 10 and 5, then multiply by 2, then to the power of 2
→ ((10 + 5) * 2)^2 = 900
```

---

## Project Structure

```
Agentic-Application/
├── agentic_app/                 # The code
│   ├── __init__.py
│   ├── tools.py                 # 18 built-in tools
│   ├── agent.py                 # The smart brain
│   └── app.py                   # Easy-to-use API
│
├── tests/                       # Tests
│   ├── __init__.py
│   └── test_agentic_app.py      # 39 test cases
│
├── README.md                    # This file
├── requirements.txt             # Dependencies
└── .gitignore
```

---

## Features

✓ **Natural Language**: Just tell it what you want  
✓ **Smart Chaining**: Connect operations with "then"  
✓ **18 Built-in Tools**: Arithmetic, strings, conversions  
✓ **Zero Dependencies**: No external packages needed  
✓ **Well Tested**: 39 tests, all passing  
✓ **Easy to Extend**: Add your own custom tools  

---

## Need to Run Tests?

Make sure you have pytest:

```bash
pip install pytest
python -m pytest tests/ -v
```

**Expected Result:**
```
======================== 39 passed in 0.XX seconds ========================
```

---

## Want to Add Your Own Tool?

```python
from agentic_app import create_app
from agentic_app.tools import Tool, ToolParameter, ToolType

app = create_app()

# Create a custom tool
square = Tool(
    name="square",
    description="Square a number",
    func=lambda x: x ** 2,
    parameters=[ToolParameter("x", "float")],
    tool_type=ToolType.ARITHMETIC,
)

# Register it
app.register_tool(square)

# Use it
result = app.tool_registry.get("square").invoke(x=5)
print(result)  # 25
```

---

## Requirements

- **Python**: 3.8 or newer
- **Dependencies**: ZERO for basic usage (pytest optional for testing)
- **OS**: Windows, Mac, or Linux

---

## Author

Yash Jain (@yashjain3579)

---

**Happy Querying!**
