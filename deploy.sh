#!/bin/bash

# eTraceAI Deployment Script for Linux/Mac
# This script simplifies the deployment process

set -e

echo "============================================"
echo "  eTraceAI Docker Deployment Script"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Docker and Docker Compose are installed"

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p data output reference_db models

# Function to display menu
show_menu() {
    echo ""
    echo "Select an option:"
    echo "1) Build and start the application"
    echo "2) Start the application (existing build)"
    echo "3) Stop the application"
    echo "4) View logs"
    echo "5) Restart the application"
    echo "6) Clean up (remove containers and images)"
    echo "7) Exit"
    echo ""
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter your choice [1-7]: " choice

    case $choice in
        1)
            print_info "Building and starting eTraceAI..."
            docker-compose up --build -d
            print_success "eTraceAI is now running!"
            print_info "Access the application at: http://localhost:8501"
            ;;
        2)
            print_info "Starting eTraceAI..."
            docker-compose up -d
            print_success "eTraceAI is now running!"
            print_info "Access the application at: http://localhost:8501"
            ;;
        3)
            print_info "Stopping eTraceAI..."
            docker-compose down
            print_success "eTraceAI has been stopped"
            ;;
        4)
            print_info "Displaying logs (Press Ctrl+C to exit)..."
            docker-compose logs -f
            ;;
        5)
            print_info "Restarting eTraceAI..."
            docker-compose restart
            print_success "eTraceAI has been restarted"
            ;;
        6)
            print_warning "This will remove all containers and images. Are you sure? (y/n)"
            read -p "" confirm
            if [ "$confirm" = "y" ]; then
                print_info "Cleaning up..."
                docker-compose down -v
                docker rmi etraceai-etraceai 2>/dev/null || true
                print_success "Cleanup complete"
            else
                print_info "Cleanup cancelled"
            fi
            ;;
        7)
            print_info "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option. Please try again."
            ;;
    esac
done
