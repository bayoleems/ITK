# ITK Platform

ITK is an intelligent search platform to provide advanced search capabilities and web scraping functionality.

## Features

- FastAPI-based REST API
- Intelligent search capabilities
- Web scraping functionality
- Scheduled tasks and background jobs

## Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ITK
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
ITK/
├── app/
│   ├── api/            # API routes and endpoints
│   ├── core/           # Core application components
│   ├── models/         # Data models and schemas
│   ├── services/       # Business logic and services
│   ├── utils/          # Utility functions and helpers
│   ├── main.py         # Application entry point
│   └── cli.py          # Command-line interface
├── sample_data/        # Sample data for testing
├── Dockerfile/        # Deployment
├── requirement.txt    # Project dependencies
└── .env              # Environment variables
```

## Running the Application

1. Start the development server:
```bash
PYTHONPATH=$PYTHONPATH:. python app/main.py
```

The server will start at `http://localhost:8000`

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/api-docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `GET /`: Root endpoint
- `GET /health`: Health check endpoint
- Additional endpoints are available through the API documentation

## CLI

1. Start the chat:
```bash
PYTHONPATH=$PYTHONPATH:. python app/cli.py
```

2. Use -c or --company to include company name:
```bash
PYTHONPATH=$PYTHONPATH:. python app/cli.py -c Stears
```

## Docker

1. Build the Docker image:
```bash
docker build -t itk-platform .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env itk-platform
```

3. Run the CLI version:
```bash
docker run -it --env-file .env itk-platform python app/cli.py -c Stears
```

## Dependencies

Key dependencies include:
- FastAPI: Modern web framework
- LangChain: Framework for developing applications powered by language models
- OpenAI: Integration with OpenAI's language models
- ChromaDB: Vector database for embeddings
- Playwright: Web automation and scraping
- APScheduler: Task scheduling

For a complete list of dependencies, see `requirement.txt`.
