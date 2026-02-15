# AI Data Engineer

Everyday data engineering tasks automated with AI.

## Description

This project is a collection of scripts and agents designed to automate common data engineering tasks. It includes capabilities for web crawling, interacting with Hugging Face datasets, and more. The goal is to leverage AI to streamline data acquisition and processing workflows.

## Features

- **Web Crawling:** Scripts to fetch and parse content from websites.
- **Hugging Face Integration:** Load and process datasets from the Hugging Face Hub.
- **AI-powered Agents:** Utilizes agents for more complex, multi-step data tasks.
- **Modern Python Tooling:** Uses `uv` for package management and a structured project setup.

## Setup and Installation

This project uses `uv` for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai_dataengineer
    ```

2.  **Create a virtual environment and install dependencies:**

    Using `uv`:
    ```bash
    uv venv
    uv sync
    ```

    If you are not using `uv`, you can use `pip` with the `requirements.lock` (if generated) or `pyproject.toml`:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    pip install -r requirements.lock 
    # or if you don't have a lock file
    # pip install . 
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add any necessary environment variables (e.g., API keys).
    ```
    HUGGING_FACE_API_KEY="your_api_key_here"
    ```

## Usage

The main scripts in this project are `data_engineer.py` and `agents.py`.

To run a script:
```bash
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
python data_engineer.py
```
or
```bash
uv run python data_engineer.py
```

Look inside the scripts for more details on their specific functionality and command-line arguments.