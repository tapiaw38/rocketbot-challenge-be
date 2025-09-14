# RocketBot Challenge - Backend API

This project is a Python-based REST API designed for task management following hexagonal architecture principles. It provides a simple and efficient solution for CRUD operations on tasks.

## Features

- RESTful API design for easy integration
- Hexagonal architecture (Ports and Adapters) pattern
- In-memory data storage (no database required)
- Automatic API documentation with Swagger/OpenAPI
- Docker containerization support
- CORS enabled for frontend development
- Input validation with Pydantic models
- CI/CD pipeline with GitHub Actions
- Automated code formatting and linting
- Comprehensive test coverage (70%)

## API Endpoints

The API provides the following endpoints for task management:

- `GET /tasks` - Retrieve all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update an existing task
- `DELETE /tasks/{id}` - Delete a task by ID

## Architecture

The project follows the hexagonal architecture pattern with the following layers:

- **Domain**: Core business entities (`Task`) and repository interfaces
- **Use Cases**: Business logic for CRUD operations
- **Adapters**: Concrete implementations (in-memory repository, web controllers)
- **Infrastructure**: Configuration and application entry point

## Requirements

- Python 3.8 or higher installed
- Docker and Docker Compose installed on your system
- Make sure `make` is available on your system to use the provided Makefile for managing the project

## Makefile Commands

The project includes a Makefile with convenient commands for development and deployment:

| Command              | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `make build`         | Build Docker images                                         |
| `make run`           | Run containers in detached mode                             |
| `make dev`           | Build and run with hot reload (recommended for development) |
| `make stop`          | Stop all containers                                         |
| `make logs`          | View container logs (follow mode)                           |
| `make clean`         | Stop containers and clean up volumes/images                 |
| `make test-build`    | Build test Docker image                                     |
| `make test`          | Run tests in Docker container                               |
| `make test-coverage` | Run tests with coverage report                              |
| `make format`        | Format code with Black and isort                            |
| `make check-format`  | Check code formatting without making changes                |
| `make lint`          | Run flake8 and mypy linting                                 |
| `make quality`       | Run format, lint, and test (full quality check)             |

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd rocketbot-challenge-be
   ```

2. **Build and run with Docker Compose**:

   ```bash
   make dev
   ```

3. **Access the API**:
   - API Base URL: <http://localhost:8000>
   - Swagger UI: <http://localhost:8000/docs>
   - ReDoc: <http://localhost:8000/redoc>

## Development Setup

### Using Docker (Recommended)

1. **Start the development environment**:

   ```bash
   make dev
   ```

2. **For development with hot reload**:

   ```bash
   make dev
   ```

   The application will automatically reload when you make changes to the code.

### Manual Setup (Alternative)

1. **Create virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python main.py
   ```

## API Usage Examples

### 1. Create a Task (POST /tasks)

**Request**:

```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy bread",
       "category": "Home"
     }'
```

**Response**:

```json
{
  "id": 1,
  "title": "Buy bread",
  "category": "Home",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 2. Get All Tasks (GET /tasks)

**Request**:

```bash
curl -X GET "http://localhost:8000/tasks"
```

**Response**:

```json
[
  {
    "id": 1,
    "title": "Buy bread",
    "category": "Home",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "title": "Deploy project",
    "category": "Work",
    "created_at": "2024-01-15T11:00:00",
    "updated_at": "2024-01-15T11:00:00"
  }
]
```

### 3. Update a Task (PUT /tasks/{id})

**Request**:

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy pastries",
       "category": "Home"
     }'
```

**Response**:

```json
{
  "id": 1,
  "title": "Buy pastries",
  "category": "Home",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

### 4. Delete a Task (DELETE /tasks/{id})

**Request**:

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

**Response**:

```json
{
  "message": "Task 1 eliminada correctamente"
}
```

## Project Structure

```bash
rocketbot-challenge-be/
├── src/
│   ├── core/
│   │   ├── domain/
│   │   │   ├── model.py
│   │   │   └── repository_interface.py
│   │   └── use_cases/
│   │       └── task_use_cases.py
│   ├── adapters/
│   │   ├── datasources/
│   │   │   └── repositories/
│   │   │       └── inmemory/
│   │   │           └── task_repository.py
│   │   ├── services/
│   │   │   └── task/
│   │   │       └── task_service.py
│   │   └── web/
│   │       └── controllers/
│   │           └── task/
│   │               └── task_controller.py  #
│   ├── schemas/
│   │   └── schemas.py
│   └── routes/
│       └── routes_manager.py
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── env.example
├── .gitignore
└── README.md
```

## Technologies Used

### Core Framework

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running FastAPI
- **Python 3.10+**: Programming language

### Infrastructure & DevOps

- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline automation

### Code Quality & Testing

- **pytest**: Testing framework with async support
- **Black**: Code formatter for consistent style
- **isort**: Import sorting and organization
- **Flake8**: Python linting and style checking
- **MyPy**: Static type checking
- **pytest-cov**: Code coverage analysis

## Key Features

### Architecture & Design

- **Hexagonal architecture** (Ports and Adapters)
- **Clear separation of concerns** across layers
- **Dependency injection** with FastAPI
- **Repository pattern** implementation

### API & Documentation

- **RESTful API design** for easy integration
- **Automatic data validation** with Pydantic
- **Auto-generated documentation** with Swagger/OpenAPI
- **Proper HTTP error handling** with status codes
- **CORS configured** for frontend development
- **Health check endpoints** for monitoring

### Data & Storage

- **In-memory repository** (no database required)
- **Automatic timestamps** for created/updated fields
- **Auto-incremental IDs** starting from 1

### DevOps & Quality

- **Docker containerization** support
- **Comprehensive test suite** with Docker support
- **CI/CD pipeline** with GitHub Actions
- **Automated code formatting** with Black and isort
- **Static analysis** with Flake8 and MyPy
- **Code coverage** reporting (70% target)

## Development

### Running in Development Mode

```bash
make dev
```

### Testing

The project includes a comprehensive test suite with Docker support for isolated testing.

#### Quick Start Testing

```bash
make test-build

make test

make test-coverage

./test.sh build
./test.sh coverage
```

#### Test Commands

| Command              | Description                               |
| -------------------- | ----------------------------------------- |
| `make test-build`    | Build the test Docker image               |
| `make test`          | Run all tests in Docker                   |
| `make test-verbose`  | Run tests with verbose output             |
| `make test-coverage` | Run tests with coverage report            |
| `make test-specific` | Run specific test (set TEST=path/to/test) |
| `make test-clean`    | Clean up test containers and images       |

#### Test Script Usage

The `test.sh` script provides a user-friendly interface:

```bash

./test.sh help

TEST=tests/unit/adapters/datasources/repositories/task/test_repository.py ./test.sh specific

./test.sh shell
```

#### Test Structure

```bash
tests/
├── unit/
│   └── adapters/
│       └── datasources/
│           └── repositories/
│               └── task/
│                   ├── test_repository.py
│                   └── test_repository_fixtures.py
├── conftest.py
└── README.md
```

#### Coverage Reports

After running tests with coverage, open the HTML report:

```bash
# On Linux/Mac
open test-results/htmlcov/index.html

# On Windows
start test-results/htmlcov/index.html
```

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline using GitHub Actions that ensures code quality and consistency.

### Pipeline Stages

1. **Code Quality Checks**:

   - **Flake8**: Python linting for code style and errors
   - **Black**: Automatic code formatting
   - **isort**: Import sorting and organization
   - **MyPy**: Static type checking

2. **Testing**:

   - **pytest**: Comprehensive test suite execution
   - **Coverage**: Code coverage analysis (70% target)
   - **Docker**: Isolated testing environment

3. **Build & Deploy**:
   - **Docker Build**: Container image creation
   - **Security Scanning**: Vulnerability checks
   - **Deployment**: Automated deployment to staging/production

### GitHub Actions Workflow

The pipeline runs automatically on:

- **Push to main/develop branches**
- **Pull Request creation/updates**
- **Manual trigger**

### Pipeline Status

[![CI/CD Pipeline](https://github.com/your-username/rocketbot-challenge-be/workflows/CI/badge.svg)](https://github.com/your-username/rocketbot-challenge-be/actions)

## Code Quality & Formatting

The project enforces strict code quality standards through automated tools and CI/CD checks.

### Code Formatting

**Black** is used for consistent code formatting:

- Line length: 88 characters
- Consistent quote style
- Proper indentation
- Automatic code reformatting

**isort** handles import organization:

- Alphabetical sorting
- Grouped by type (standard, third-party, local)
- Compatible with Black formatting

### Linting

**Flake8** performs static analysis:

- PEP 8 compliance
- Code complexity checks
- Unused imports detection
- Syntax error detection

**MyPy** provides static type checking:

- Type annotation validation
- Missing import detection
- Untyped definitions checking

### Quality Commands

```bash
# Format code automatically
make format

# Check formatting without changes
make check-format

# Run all linting checks
make lint

# Complete quality check (format + lint + test)
make quality
```

This ensures code quality checks run automatically before each commit.

### Code Quality Metrics

- **Test Coverage**: 70%
- **Linting**: Zero errors/warnings
- **Type Coverage**: 100% for core modules
- **Formatting**: Consistent across all files

The application will automatically reload when code changes are detected.

### Available Make Commands

See the [Makefile Commands](#makefile-commands) section above for a complete list of available commands.

### Testing the API

You can test the API using:

1. **Swagger UI**: <http://localhost:8000/docs>
2. **curl** (examples above)
3. **Postman** or any HTTP client
4. **Vue.js Frontend** (see frontend repository)

## Important Notes

- Data is stored in memory and will be lost when the application restarts
- The API is configured to accept requests from any origin (CORS)
- All endpoints return responses in JSON format
- Timestamps are handled in ISO 8601 format
- Task IDs are auto-incremental starting from 1

## Environment Variables

Copy `env.example` to `.env` and modify as needed:

```bash
cp env.example .env
```

Available environment variables:

- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `API_RELOAD`: Enable auto-reload (default: true)
- `API_WORKERS`: Number of workers (default: 1)
- `ENVIRONMENT`: Environment mode (default: development)

## Development Workflow

### Code Quality Workflow

1. **Before committing**:

   ```bash
   make format    # Format code
   make lint      # Check for issues
   make test      # Run tests
   ```

2. **Complete quality check**:

   ```bash
   make quality   # Runs format + lint + test
   ```

3. **Pre-commit setup** (optional):

   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Contributing Guidelines

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** following the code style
4. **Run quality checks**: `make quality`
5. **Commit your changes**: `git commit -m "Add your feature"`
6. **Push to your fork**: `git push origin feature/your-feature`
7. **Create a Pull Request**

### Code Style Guidelines

- **Follow PEP 8** standards (enforced by Flake8)
- **Use Black** for consistent formatting
- **Organize imports** with isort
- **Add type hints** where possible
- **Write tests** for new functionality
- **Maintain 70%+ test coverage**

### Troubleshooting

#### Common Issues

**Formatting errors**:

```bash
make format  # Auto-fix formatting
```

**Linting errors**:

```bash
make lint    # Check for issues
```

**Test failures**:

```bash
make test-verbose  # Run with detailed output
```

**Docker issues**:

```bash
make clean   # Clean up containers and images
make build   # Rebuild images
```
