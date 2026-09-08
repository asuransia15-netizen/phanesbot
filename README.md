# phanesbot

Python SDK for Phanes Bot — Solana trading data, leaderboard analytics, and real-time WebSocket feed

## Features

- ✅ Real-time WebSocket feed for live trading data
- ✅ Token narrative and social sentiment analysis
- ✅ Leaderboard and trending token discovery
- ✅ CLI tool for quick access: phanes-cli

## Installation

### PyPI
```bash
pip install git+https://github.com/phanesbot-dev/phanesbot.git
```

## Quick Start

```python
from phanesbot import *

# Initialize client
client = Client()

# Get trending tokens
trending = client.get_trending()
print(trending)
```

## Documentation

Full documentation coming soon.

## License

MIT
