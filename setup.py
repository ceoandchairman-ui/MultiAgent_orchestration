from setuptools import setup, find_packages

setup(
    name="multiagent-orchestration",
    version="0.1.0",
    description="Multi-Agent Orchestration System with MCP and A2A Protocol",
    author="CEO and Chairman UI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "httpx>=0.25.0",
        "websockets>=12.0",
        "aiohttp>=3.9.0",
        "redis>=5.0.0",
        "python-socketio>=5.10.0",
        "python-json-logger>=2.0.0",
        "pyyaml>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ]
    },
)
