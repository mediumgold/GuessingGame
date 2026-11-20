import sys
from Guess import Guess

if len(sys.argv) != 2 or sys.argv[1] not in ("play", "test"):
    print("Usage: python3 words.py [play|test]")
    sys.exit(1)

Guess(sys.argv[1] == "test").start()
