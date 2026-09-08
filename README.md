# phanesbot

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Solana](https://img.shields.io/badge/solana-1.18%2B-orange)](https://solana.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Unofficial Phanes Bot Python SDK — Solana trading data, leaderboard analytics, and real-time WebSocket feed.**

> 📊 Live leaderboard tracking · WebSocket trade streams · Wallet analytics · Historical data export

## Features

- **Leaderboard Analytics** — Track top traders, win rates, and ROI across Phanes
- **Real-Time WebSocket** — Stream trades, new listings, and whale alerts
- **Wallet Deep-Dive** — Analyze any wallet's trading history, tokens held, and PnL
- **Historical Export** — Export trading data to CSV/JSON for custom analysis
- **Multi-Asset** — SOL, USDC, and all SPL tokens supported

## Quick Start

```bash
pip install git+https://github.com/asuransia15-netizen/phanesbot.git
```

```python
from phanesbot import PhanesClient

client = PhanesClient(api_key="your_key_here")

# Get top traders
leaderboard = client.get_leaderboard(timeframe="24h", limit=20)

# Stream real-time trades
for trade in client.stream_trades(token="SOL"):
    print(f"{trade['trader']} {trade['side']} {trade['amount']} SOL")

# Analyze a wallet
wallet = client.get_wallet("WALLET_ADDRESS")
print(f"PnL: {wallet['pnl']} | Win Rate: {wallet['win_rate']}%")
```

## CLI

```bash
# View leaderboard
phanes-cli leaderboard --timeframe 24h

# Track a wallet
phanes-cli wallet WALLET_ADDRESS

# Stream trades
phanes-cli stream --token SOL
```

## Dependencies

- `requests>=2.28.0` — HTTP client
- `websocket-client>=1.6.0` — Real-time streaming

## Documentation

Visit [phanesbot-dev.github.io](https://phanesbot-dev.github.io)

## Disclaimer

Unofficial third-party SDK. Not affiliated with Phanes Bot. Trading cryptocurrencies carries significant risk.

## License

MIT © phanesbot-dev