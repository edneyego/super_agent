from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="super-agent",
    version="1.0.0",
    author="Edney Oliveira",
    author_email="edneyego@gmail.com",
    description="Sistema Multi-Agente com LangGraph + MCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edneyego/super_agent",
    project_urls={
        "Bug Tracker": "https://github.com/edneyego/super_agent/issues",
        "Documentation": "https://github.com/edneyego/super_agent/blob/main/README.md",
        "Source Code": "https://github.com/edneyego/super_agent",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.13",
    install_requires=[
        "langchain>=0.1.0",
        "langgraph>=0.0.20",
        "langchain-openai>=0.0.5",
        "langchain-google-genai>=0.0.6",
        "langchain-anthropic>=0.0.1",
        "fastmcp>=0.1.0",
        "httpx>=0.25.0",
        "aiohttp>=3.9.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "rich>=13.7.0",
        "click>=8.1.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "isort>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "super-agent=src.cli:main",
        ],
    },
)