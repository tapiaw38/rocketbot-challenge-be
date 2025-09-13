#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' 


print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}


show_usage() {
    echo "RocketBot Challenge Test Runner"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build       Build the test Docker image"
    echo "  run         Run all tests"
    echo "  verbose     Run tests with verbose output"
    echo "  coverage    Run tests with coverage report"
    echo "  watch       Run tests in watch mode"
    echo "  specific    Run specific test (use TEST=path/to/test)"
    echo "  clean       Clean up test containers and images"
    echo "  shell       Open shell in test container"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 run"
    echo "  $0 coverage"
    echo "  TEST=tests/unit/adapters/datasources/repositories/task/test_repository.py $0 specific"
}


check_docker() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose is not installed or not in PATH"
        exit 1
    fi
}


build_tests() {
    print_status "Building test Docker image..."
    make test-build
    print_success "Test image built successfully"
}


run_tests() {
    print_status "Running tests..."
    make test
    print_success "Tests completed"
}


run_tests_verbose() {
    print_status "Running tests with verbose output..."
    make test-verbose
    print_success "Tests completed"
}


run_tests_coverage() {
    print_status "Running tests with coverage..."
    make test-coverage
    print_success "Tests completed with coverage report"
    print_status "Coverage report available at: test-results/htmlcov/index.html"
}


run_tests_watch() {
    print_status "Running tests in watch mode..."
    print_warning "Press Ctrl+C to stop watching"
    docker-compose -f docker-compose.test.yml run --rm tests pytest-watch
}


run_specific_test() {
    if [ -z "$TEST" ]; then
        print_error "Please specify TEST environment variable"
        echo "Example: TEST=tests/unit/adapters/datasources/repositories/task/test_repository.py $0 specific"
        exit 1
    fi
    print_status "Running specific test: $TEST"
    TEST="$TEST" make test-specific
    print_success "Specific test completed"
}


clean_tests() {
    print_status "Cleaning up test containers and images..."
    make test-clean
    print_success "Cleanup completed"
}


test_shell() {
    print_status "Opening shell in test container..."
    docker-compose -f docker-compose.test.yml run --rm tests /bin/bash
}


main() {
    check_docker

    case "${1:-help}" in
        "build")
            build_tests
            ;;
        "run")
            run_tests
            ;;
        "verbose")
            run_tests_verbose
            ;;
        "coverage")
            run_tests_coverage
            ;;
        "watch")
            run_tests_watch
            ;;
        "specific")
            run_specific_test
            ;;
        "clean")
            clean_tests
            ;;
        "shell")
            test_shell
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

main "$@"
