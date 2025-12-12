import sys
from .app import create_app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m agentic_app <query>")
        print("Example: python -m agentic_app 'Add 5 and 10'")
        print("Example: python -m agentic_app 'Multiply 10 and 5, then divide by 2'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    app = create_app(verbose=False)
    
    try:
        result = app.query(query)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
