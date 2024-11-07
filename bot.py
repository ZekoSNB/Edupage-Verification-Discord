#!/usr/bin/env python3
from Bot.__main__ import main
import time, traceback


if __name__ == "__main__":
    try:
        print("Bot starting......")
        main()
    except Exception as e:
        print("Bot encountered an error and will restart", exc_info=e)
        time.sleep(5)
