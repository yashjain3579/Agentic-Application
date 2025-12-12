from agentic_app import create_app

app = create_app()

print("Test 1: Add 5 and 10")
print(f"Result: {app.query('Add 5 and 10')}")
print()

print("Test 2: Add 5 and 10, then multiply by 2")
print(f"Result: {app.query('Add 5 and 10, then multiply by 2')}")
print()

print("Test 3: Multiply 5 and 4, then to the power of 2")
print(f"Result: {app.query('Multiply 5 and 4, then to the power of 2')}")
print()

print("Test 4: Uppercase hello")
print(f"Result: {app.query('Uppercase hello')}")
print()

print("All basic tests passed!")
