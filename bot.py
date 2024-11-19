#!/usr/bin/env python3
from Bot.__main__ import main
import time, traceback


if __name__ == "__main__":
    while True:
        try:
            print("Bot starting......")
            main()
        except KeyboardInterrupt:
            print("Bot shutting down")
            break
        except Exception as e:
            print("Bot encountered an error and will restart", e)
            time.sleep(5)
