from agentic_app import create_app

app = create_app(verbose=True)

print("\n" + "="*60)
print("TEST 1: Simple Math")
print("="*60)
result = app.query("Add 5 and 10")
print(f"Final Result: {result}\n")

print("="*60)
print("TEST 2: Chain Operations")
print("="*60)
result = app.query("Multiply 10 and 5, then divide by 2")
print(f"Final Result: {result}\n")

print("="*60)
print("TEST 3: Complex Chain")
print("="*60)
result = app.query("Add 10 and 5, then multiply by 2, then to the power of 2")
print(f"Final Result: {result}\n")

print("="*60)
print("TEST 4: String Operation")
print("="*60)
result = app.query("Uppercase hello world")
print(f"Final Result: {result}\n")

print("="*60)
print("All detailed tests completed!")
print("="*60)
