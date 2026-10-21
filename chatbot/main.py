import sys

try:
    from sendingMessage import *
except (FileNotFoundError, EnvironmentError, RuntimeError) as exc:
    print(f"Startup error: {exc}", file=sys.stderr)
    sys.exit(1)
except (KeyboardInterrupt, EOFError):
    print("\nGood bye....")