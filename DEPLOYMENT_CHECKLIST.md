# 🚀 eTraceAI Deployment Checklist

## Pre-Deployment Verification

Before deploying, ensure all the following files are present and configured correctly:

### ✅ Required Files

- [ ] `Dockerfile` - Docker container configuration
- [ ] `docker-compose.yml` - Docker Compose orchestration
- [ ] `.dockerignore` - Files to exclude from Docker build
- [ ] `requirements.txt` - Python dependencies with versions
- [ ] `README.md` - Project documentation
- [ ] `DOCKER_DEPLOYMENT.md` - Detailed deployment guide
- [ ] `deploy.sh` - Linux/Mac deployment script
- [ ] `deploy.bat` - Windows deployment script

### ✅ Application Files

- [ ] `app/dashboard.py` - Main Streamlit application (with modern UI)
- [ ] `app/taxonomy_matcher.py` - Taxonomy matching module
- [ ] `app/cluster.py` - Clustering analysis
- [ ] `app/phylum_barplot.py` - Visualization generation
- [ ] `models/deep_model.py` - Deep learning model

### ✅ Directory Structure

```
eTraceAI/
├── app/                  ✓ Contains all Python application files
├── models/               ✓ Contains deep learning model files
├── data/                 ✓ Will store input FASTA files
├── output/               ✓ Will store analysis results
├── reference_db/         ✓ Contains reference databases
├── blast+/               ✓ Contains BLAST binaries (Windows only)
├── Dockerfile            ✓ Created
├── docker-compose.yml    ✓ Created
├── .dockerignore         ✓ Created
├── requirements.txt      ✓ Updated with all dependencies
├── README.md             ✓ Created
├── DOCKER_DEPLOYMENT.md  ✓ Created
├── deploy.sh             ✓ Created
└── deploy.bat            ✓ Created
```

## Deployment Steps

### Option 1: Quick Deploy (Recommended)

#### Windows:
1. Open Command Prompt or PowerShell
2. Navigate to project directory:
   ```batch
   cd "C:\Users\SHUBHAM\Desktop\ednaAI - Copy"
   ```
3. Run deployment script:
   ```batch
   deploy.bat
   ```
4. Select option 1: "Build and start the application"
5. Wait for build to complete (5-10 minutes first time)
6. Access at: http://localhost:8501

#### Linux/Mac:
1. Open Terminal
2. Navigate to project directory:
   ```bash
   cd /path/to/ednaAI
   ```
3. Make script executable:
   ```bash
   chmod +
   x deploy.sh
   ```
4. Run deployment script:
   ```bash
   ./deploy.sh
   ```
5. Select option 1: "Build and start the application"
6. Wait for build to complete (5-10 minutes first time)
7. Access at: http://localhost:8501

### Option 2: Manual Docker Compose

```bash
# Navigate to project directory
cd "C:\Users\SHUBHAM\Desktop\ednaAI - Copy"

# Build and start
docker-compose up --build -d

# View logs
docker-compose logs -f

# Access application
# Open browser: http://localhost:8501
```

### Option 3: Docker CLI

```bash
# Build image
docker build -t etraceai:latest .

# Run container
docker run -d \
  -p 8501:8501 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/reference_db:/app/reference_db" \
  -v "$(pwd)/models:/app/models" \
  --name etraceai-app \
  etraceai:latest

# View logs
docker logs -f etraceai-app
```

## Post-Deployment Verification

### 1. Check Container Status

```bash
docker ps
```

Expected output should show `etraceai-app` running on port 8501.

### 2. Check Health Status

```bash
docker inspect --format='{{.State.Health.Status}}' etraceai-app
```

Should return: `healthy`

### 3. Check Logs

```bash
docker-compose logs etraceai
```

Look for:
- No error messages
- "You can now view your Streamlit app in your browser"
- "Network URL: http://0.0.0.0:8501"

### 4. Access Application

1. Open browser
2. Navigate to: http://localhost:8501
3. Verify all pages load:
   - [ ] Home page displays
   - [ ] Navigation menu works
   - [ ] Modern UI is visible (gradients, animations)
   - [ ] File uploader is present

### 5. Test Functionality

- [ ] Upload a sample FASTA file
- [ ] Processing pipeline runs without errors
- [ ] Results page shows data
- [ ] Visualizations render correctly
- [ ] FASTA preview works
- [ ] Developer Info page displays correctly

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs etraceai
```

**Common fixes:**
- Port 8501 in use: Change port in docker-compose.yml
- Insufficient memory: Increase Docker memory in settings
- Build errors: Run `docker-compose build --no-cache`

### Application Not Accessible

1. Verify container is running: `docker ps`
2. Check port mapping: `docker port etraceai-app`
3. Test with curl: `curl http://localhost:8501/_stcore/health`
4. Check firewall settings
5. Try 127.0.0.1 instead of localhost

### BLAST+ Issues

BLAST+ is installed from Ubuntu repos. If issues occur:
1. Check logs for BLAST errors
2. Verify BLAST installation: `docker exec etraceai-app blastn -version`
3. Rebuild with specific BLAST version if needed

### Performance Issues

1. Increase Docker resources:
   - Docker Desktop → Settings → Resources
   - Increase CPUs to 4+
   - Increase Memory to 8GB+

2. Modify docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
```

## Production Deployment Checklist

### Security

- [ ] Change default ports
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Use secrets management for API keys
- [ ] Run container as non-root user
- [ ] Enable Docker security scanning

### Monitoring

- [ ] Set up log aggregation
- [ ] Configure health checks
- [ ] Set up monitoring alerts
- [ ] Configure backup strategy

### Scaling

- [ ] Consider load balancer
- [ ] Set up container orchestration (Kubernetes)
- [ ] Configure auto-scaling
- [ ] Set up CDN for static assets

## Cloud Deployment

### AWS

1. Launch EC2 instance (t2.large or better)
2. Install Docker and Docker Compose
3. Clone repository
4. Run deployment script
5. Configure Security Group (allow port 8501)
6. Access via public IP

### Azure

1. Create Azure Container Instance
2. Push image to Azure Container Registry
3. Deploy from registry
4. Configure networking
5. Access via Azure URL

### Google Cloud

1. Build and push to Container Registry
2. Deploy to Cloud Run
3. Configure service settings
4. Access via provided URL

## Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify all files are present
3. Ensure Docker has sufficient resources
4. Review [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
5. Contact: nitian.shubh@gmail.com

## Version Information

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.9+
- **Streamlit**: 1.28.0
- **PyTorch**: 2.1.0
- **BLAST+**: Latest from apt

---

**Deployment Date**: _____________

**Deployed By**: _____________

**Environment**: ☐ Development ☐ Staging ☐ Production

**Status**: ☐ Success ☐ Failed ☐ In Progress

**Notes**:
_______________________________________________
_______________________________________________
_______________________________________________

