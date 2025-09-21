#!/bin/bash

# Urban Planning Agent - Quick Deployment Script
# This script provides easy deployment options for the urban planning agent

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check if Docker is installed
    if command_exists docker; then
        print_success "Docker is installed"
    else
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check if docker-compose is installed
    if command_exists docker-compose; then
        print_success "Docker Compose is installed"
    else
        print_warning "Docker Compose is not installed. Using 'docker compose' instead."
    fi

    # Check if .env file exists
    if [ -f ".env" ]; then
        print_success ".env file exists"
    else
        print_warning ".env file not found. Creating from template..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_info "Please edit .env file with your GCP credentials before deployment"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    fi
}

# Function to build Docker image
build_image() {
    print_info "Building Docker image..."
    docker build -f Dockerfile.urban-planning -t urban-planning-agent:latest .
    print_success "Docker image built successfully"
}

# Function to deploy locally with Docker
deploy_local() {
    print_info "Deploying locally with Docker..."

    # Stop any existing containers
    docker stop urban-planning-agent 2>/dev/null || true
    docker rm urban-planning-agent 2>/dev/null || true

    # Run the container
    docker run -d \
        --name urban-planning-agent \
        -p 8000:8000 \
        --env-file .env \
        -v $(pwd)/data:/app/data \
        -v $(pwd)/logs:/app/logs \
        urban-planning-agent:latest

    print_success "Agent deployed locally on port 8000"
    print_info "Check status: docker logs urban-planning-agent"
    print_info "Stop agent: docker stop urban-planning-agent"
}

# Function to deploy with Docker Compose
deploy_compose() {
    print_info "Deploying with Docker Compose..."

    if command_exists docker-compose; then
        docker-compose up -d
    else
        docker compose up -d
    fi

    print_success "Agent deployed with Docker Compose"
    print_info "Check status: docker-compose ps"
    print_info "View logs: docker-compose logs -f urban-planning-agent"
    print_info "Stop agent: docker-compose down"
}

# Function to deploy to Google Cloud Run
deploy_cloud_run() {
    print_info "Deploying to Google Cloud Run..."

    # Check if gcloud is installed
    if ! command_exists gcloud; then
        print_error "gcloud CLI is not installed. Please install Google Cloud SDK first."
        exit 1
    fi

    # Get project ID from .env file
    if [ -f ".env" ]; then
        PROJECT_ID=$(grep "PROJECT_ID" .env | cut -d '=' -f2 | tr -d '"')
        if [ -z "$PROJECT_ID" ]; then
            print_error "PROJECT_ID not found in .env file"
            exit 1
        fi
    else
        print_error ".env file not found"
        exit 1
    fi

    # Build and push image
    print_info "Building and pushing Docker image to GCR..."
    docker build -f Dockerfile.urban-planning -t gcr.io/$PROJECT_ID/urban-planning-agent:latest .
    docker push gcr.io/$PROJECT_ID/urban-planning-agent:latest

    # Deploy to Cloud Run
    print_info "Deploying to Cloud Run..."
    gcloud run deploy urban-planning-agent \
        --image gcr.io/$PROJECT_ID/urban-planning-agent:latest \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 1 \
        --set-env-vars-file .env

    print_success "Agent deployed to Google Cloud Run"
}

# Function to show status
show_status() {
    print_info "Checking deployment status..."

    # Check if container is running
    if docker ps | grep -q urban-planning-agent; then
        print_success "Agent container is running"
        print_info "Container logs:"
        docker logs urban-planning-agent --tail 10
    else
        print_warning "Agent container is not running"
    fi

    # Check health endpoint
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Health check passed"
    else
        print_warning "Health check failed"
    fi
}

# Function to show logs
show_logs() {
    print_info "Showing agent logs..."
    docker logs -f urban-planning-agent
}

# Function to stop deployment
stop_deployment() {
    print_info "Stopping deployment..."

    # Stop Docker container
    docker stop urban-planning-agent 2>/dev/null || true
    docker rm urban-planning-agent 2>/dev/null || true

    # Stop Docker Compose
    if command_exists docker-compose; then
        docker-compose down 2>/dev/null || true
    else
        docker compose down 2>/dev/null || true
    fi

    print_success "Deployment stopped"
}

# Main menu
show_menu() {
    echo
    echo "🚀 Urban Planning Agent - Deployment Script"
    echo "=========================================="
    echo "1. Deploy Locally (Docker)"
    echo "2. Deploy with Docker Compose"
    echo "3. Deploy to Google Cloud Run"
    echo "4. Check Status"
    echo "5. Show Logs"
    echo "6. Stop Deployment"
    echo "7. Build Image Only"
    echo "8. Exit"
    echo
}

# Main script
main() {
    check_prerequisites

    while true; do
        show_menu
        read -p "Choose an option (1-8): " choice

        case $choice in
            1)
                build_image
                deploy_local
                ;;
            2)
                deploy_compose
                ;;
            3)
                deploy_cloud_run
                ;;
            4)
                show_status
                ;;
            5)
                show_logs
                ;;
            6)
                stop_deployment
                ;;
            7)
                build_image
                ;;
            8)
                print_info "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-8."
                ;;
        esac

        echo
        read -p "Press Enter to continue..."
    done
}

# Run main function
main "$@"
