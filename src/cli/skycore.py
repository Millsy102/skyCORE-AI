# 📦 Module imports
import sys
from runtime import SkyCoreRuntime

# Function: main — handles a core step in this module
def main():
    runtime = SkyCoreRuntime()
    runtime.boot()
    if "--cli" in sys.argv:
        runtime.start_cli()
    else:
        runtime.start_ui()

# 🚀 Main entry point for script
if __name__ == "__main__":
    main()