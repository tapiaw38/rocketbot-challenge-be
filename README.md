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

| Command               | Description                                                 |
| --------------------- | ----------------------------------------------------------- |
| `make build`          | Build Docker images                                         |
| `make run`            | Run containers in detached mode                             |
| `make dev`            | Build and run with hot reload (recommended for development) |
| `make stop`           | Stop all containers                                         |
| `make logs`           | View container logs (follow mode)                           |
| `make clean`          | Stop containers and clean up volumes/images                 |
| `make test-build`     | Build test Docker image                                     |
| `make test`           | Run tests in Docker container                               |
| `make test-coverage`  | Run tests with coverage report                              |

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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running FastAPI
- **Python 3.8+**: Programming language
- **Docker**: Containerization platform

## Key Features

- ✅ Hexagonal architecture (Ports and Adapters)
- ✅ Clear separation of concerns
- ✅ In-memory repository (no database required)
- ✅ Automatic data validation with Pydantic
- ✅ Auto-generated documentation with Swagger/OpenAPI
- ✅ Proper HTTP error handling
- ✅ CORS configured for frontend development
- ✅ Health check and documentation endpoints
- ✅ Docker containerization support
- ✅ Comprehensive test suite with Docker support

## Development

### Running in Development Mode

```bash
make dev
```

### Testing

The project includes a comprehensive test suite with Docker support for isolated testing.

#### Quick Start Testing

```bash
# Build test image
make test-build

# Run all tests
make test

# Run tests with coverage report
make test-coverage

# Using the test script (alternative)
./test.sh build
./test.sh coverage
```

#### Test Commands

| Command                | Description                                    |
| ---------------------- | ---------------------------------------------- |
| `make test-build`      | Build the test Docker image                   |
| `make test`            | Run all tests in Docker                       |
| `make test-verbose`    | Run tests with verbose output                 |
| `make test-coverage`   | Run tests with coverage report                |
| `make test-specific`   | Run specific test (set TEST=path/to/test)     |
| `make test-clean`      | Clean up test containers and images           |

#### Test Script Usage

The `test.sh` script provides a user-friendly interface:

```bash
# Show help
./test.sh help

# Run specific test file
TEST=tests/unit/adapters/datasources/repositories/task/test_repository.py ./test.sh specific

# Open shell in test container for debugging
./test.sh shell
```

#### Test Structure

```text
tests/
├── unit/                          # Unit tests
│   └── adapters/
│       └── datasources/
│           └── repositories/
│               └── task/
│                   ├── test_repository.py          # Core repository tests
│                   └── test_repository_fixtures.py # Advanced test scenarios
├── conftest.py                    # Test fixtures and configuration
└── README.md                      # Test documentation
```

#### Coverage Reports

After running tests with coverage, open the HTML report:

```bash
# On Linux/Mac
open test-results/htmlcov/index.html

# On Windows
start test-results/htmlcov/index.html
```

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
