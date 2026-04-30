# 🐳 eTraceAI Docker Deployment Guide

## Overview

This guide will help you deploy the eTraceAI application using Docker and Docker Compose. The application is containerized for easy deployment across different environments.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
  - [Install Docker on Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Install Docker on Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Install Docker on Linux](https://docs.docker.com/engine/install/)

- **Docker Compose**: Version 2.0 or higher (usually included with Docker Desktop)

## Quick Start

### 1. Clone or Navigate to the Repository

```bash
cd "C:\Users\SHUBHAM\Desktop\ednaAI - Copy"
```

### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This command will:
- Build the Docker image
- Install all dependencies
- Start the application
- Expose the application on port 8501

### 3. Access the Application

Once the containers are running, open your browser and navigate to:

```
http://localhost:8501
```

## Deployment Options

### Option 1: Using Docker Compose (Recommended)

**Start the application:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the application:**
```bash
docker-compose down
```

**Rebuild after code changes:**
```bash
docker-compose up --build
```

### Option 2: Using Docker Directly

**Build the image:**
```bash
docker build -t etraceai:latest .
```

**Run the container:**
```bash
docker run -d \
  -p 8501:8501 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/reference_db:/app/reference_db" \
  -v "$(pwd)/models:/app/models" \
  --name etraceai-app \
  etraceai:latest
```

**View logs:**
```bash
docker logs -f etraceai-app
```

**Stop the container:**
```bash
docker stop etraceai-app
docker rm etraceai-app
```

## Configuration

### Environment Variables

You can customize the application by setting environment variables in the `docker-compose.yml` file:

```yaml
environment:
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - PYTHONUNBUFFERED=1
```

### Port Configuration

To change the port the application runs on, modify the `ports` section in `docker-compose.yml`:

```yaml
ports:
  - "8080:8501"  # Change 8080 to your desired port
```

### Volume Mounts

The following directories are mounted as volumes for data persistence:

- `./data` - Input FASTA files
- `./output` - Analysis results and visualizations
- `./reference_db` - Reference database files
- `./models` - Deep learning model files

## Production Deployment

### Deploy on AWS

1. **Install Docker on EC2 instance:**
```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
```

2. **Install Docker Compose:**
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone repository and deploy:**
```bash
git clone <your-repo-url>
cd etraceai
docker-compose up -d
```

4. **Configure Security Group:**
   - Open port 8501 in your EC2 security group
   - Access via: `http://<your-ec2-public-ip>:8501`

### Deploy on Azure

1. **Create Azure Container Instance:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name etraceai \
  --image etraceai:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8501 \
  --dns-name-label etraceai-app
```

2. **Access the application:**
```
http://etraceai-app.<region>.azurecontainer.io:8501
```

### Deploy on Google Cloud Platform

1. **Build and push to Container Registry:**
```bash
gcloud builds submit --tag gcr.io/[PROJECT-ID]/etraceai
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy etraceai \
  --image gcr.io/[PROJECT-ID]/etraceai \
  --platform managed \
  --port 8501 \
  --allow-unauthenticated
```

### Deploy with NGINX Reverse Proxy

For production, it's recommended to use NGINX as a reverse proxy:

1. **Create `nginx.conf`:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

2. **Update `docker-compose.yml` to include NGINX:**
```yaml
services:
  etraceai:
    # ... existing config ...

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - etraceai
    networks:
      - etraceai-network
```

## Troubleshooting

### Application won't start

**Check logs:**
```bash
docker-compose logs etraceai
```

**Common issues:**
- Port 8501 already in use → Change port in docker-compose.yml
- Insufficient memory → Increase Docker memory allocation
- Missing dependencies → Rebuild image: `docker-compose build --no-cache`

### Permission issues with volumes

On Linux, you might need to adjust permissions:
```bash
sudo chown -R $USER:$USER data/ output/ reference_db/ models/
```

### Container stops unexpectedly

Check health status:
```bash
docker ps -a
docker inspect etraceai-app
```

View detailed logs:
```bash
docker logs etraceai-app --tail 100
```

### BLAST+ not found

The Dockerfile installs BLAST+ from the Ubuntu repositories. If you need a specific version:

1. Modify the Dockerfile to download from NCBI:
```dockerfile
RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-*-x64-linux.tar.gz && \
    tar -xzvf ncbi-blast-*-x64-linux.tar.gz && \
    mv ncbi-blast-*/bin/* /usr/local/bin/
```

## Performance Optimization

### Resource Allocation

Adjust CPU and memory limits in `docker-compose.yml`:

```yaml
services:
  etraceai:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

### Caching

The Docker build uses layer caching. To optimize:
- Place frequently changing files (source code) after stable files (dependencies)
- Use `.dockerignore` to exclude unnecessary files

## Security Best Practices

1. **Don't expose sensitive data:**
   - Use environment variables for API keys
   - Don't commit credentials to the repository

2. **Use secrets management:**
```yaml
services:
  etraceai:
    secrets:
      - entrez_api_key

secrets:
  entrez_api_key:
    file: ./secrets/entrez_api_key.txt
```

3. **Run container as non-root user:**
Add to Dockerfile:
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

4. **Keep images updated:**
```bash
docker-compose pull
docker-compose up -d
```

## Monitoring and Maintenance

### Health Checks

The container includes a health check that runs every 30 seconds:
```bash
docker inspect --format='{{.State.Health.Status}}' etraceai-app
```

### Backup Data

Regular backups of important directories:
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/ output/ models/ reference_db/
```

### Update Application

```bash
git pull origin main
docker-compose down
docker-compose up --build -d
```

## Support

For issues or questions:
- Check the logs: `docker-compose logs -f`
- Review the troubleshooting section above
- Contact: nitian.shubh@gmail.com

---

**eTraceAI** - AI-powered Environmental DNA Analysis Platform
