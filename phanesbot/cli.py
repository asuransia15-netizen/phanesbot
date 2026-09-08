#!/usr/bin/env python3
"""phanes-cli — Command-line interface for Phanes Bot"""

import argparse
import sys
from phanesbot import PhanesBot

def main():
    parser = argparse.ArgumentParser(description="Phanes Bot CLI")
    parser.add_argument("--token", help="Phanes API token")
    parser.add_argument("--narrative", help="Get token narrative by ID")
    parser.add_argument("--x-user", help="Get X/Twitter user data")
    parser.add_argument("--launchpad", help="Get launchpad data (window: 1h, 24h, 7d)", default="24h")
    parser.add_argument("--ws", action="store_true", help="Connect to WebSocket feed")

    args = parser.parse_args()
    bot = PhanesBot(token=args.token)

    if args.narrative:
        result = bot.get_token_narrative(args.narrative)
        print(result)
    elif args.x_user:
        result = bot.get_x_user(args.x_user)
        print(result)
    elif args.ws:
        ws = bot.connect_websocket()
        print("Connected to WebSocket!")
        for i in range(10):
            msg = ws.recv()
            print(f"[{i}] {msg}")
    else:
        result = bot.get_launchpad_data(args.launchpad)
        print(result)

if __name__ == "__main__":
    main()