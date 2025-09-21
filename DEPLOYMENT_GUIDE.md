# Urban Planning Agent - Deployment Guide

## 🚀 Deployment Options

### Option 1: Local Development Deployment
### Option 2: Docker Container Deployment
### Option 3: Cloud Deployment (GCP)
### Option 4: Kubernetes Deployment

---

## 📋 Prerequisites

### System Requirements
- Python 3.12+
- 8GB RAM minimum, 16GB recommended
- 10GB free disk space
- Internet connection for GCP services

### GCP Requirements
- Google Cloud Project with billing enabled
- Vertex AI API enabled
- Cloud Storage API enabled
- Service Account with appropriate permissions

---

## ⚙️ Configuration Setup

### 1. Environment Variables
Create a `.env` file in the project root:

```bash
# GCP Configuration
SERVICE_ACCOUNT_KEY="<base64-encoded-service-account-json>"
PROJECT_ID="<your-gcp-project-id>"

# Optional: Custom settings
AGENT_LOG_LEVEL="INFO"
MAX_MEMORY_USAGE="8GB"
ENABLE_CACHING="true"
```

### 2. GCP Service Account Setup
1. Go to Google Cloud Console
2. Create a new service account or use existing one
3. Grant these roles:
   - `Vertex AI User`
   - `Storage Admin`
   - `BigQuery User` (optional)
4. Download the JSON key file
5. Base64 encode the key: `base64 -i key.json`
6. Add the encoded string to your `.env` file

---

## 🐳 Docker Deployment (Recommended)

### Build the Docker Image
```bash
# Build the image
docker build -t urban-planning-agent:latest .

# Or use the provided Dockerfile
docker build -f Dockerfile.urban-planning -t urban-planning-agent:latest .
```

### Run with Docker
```bash
# Run locally
docker run -p 8000:8000 --env-file .env urban-planning-agent:latest

# Run with volume mounting
docker run -p 8000:8000 -v $(pwd)/data:/app/data --env-file .env urban-planning-agent:latest
```

### Docker Compose (Production)
```yaml
version: '3.8'
services:
  urban-planning-agent:
    build:
      context: .
      dockerfile: Dockerfile.urban-planning
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## ☁️ Google Cloud Platform Deployment

### Option A: Cloud Run (Serverless)

1. **Build and push to GCR:**
```bash
# Build the image
docker build -t gcr.io/YOUR_PROJECT/urban-planning-agent:latest .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT/urban-planning-agent:latest
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy urban-planning-agent \
  --image gcr.io/YOUR_PROJECT/urban-planning-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "SERVICE_ACCOUNT_KEY=YOUR_KEY" \
  --set-env-vars "PROJECT_ID=YOUR_PROJECT" \
  --memory 2Gi \
  --cpu 1
```

### Option B: Google Kubernetes Engine (GKE)

1. **Create GKE cluster:**
```bash
gcloud container clusters create urban-planning-cluster \
  --region us-central1 \
  --num-nodes 3 \
  --machine-type e2-standard-4
```

2. **Deploy using kubectl:**
```bash
# Apply the deployment
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

### Option C: App Engine (Flexible)

Create `app.yaml`:
```yaml
runtime: python312
instance_class: F4
automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.7

env_variables:
  SERVICE_ACCOUNT_KEY: "YOUR_BASE64_KEY"
  PROJECT_ID: "YOUR_PROJECT_ID"

handlers:
- url: /.*
  script: auto
```

Deploy:
```bash
gcloud app deploy app.yaml
```

---

## 🏠 Local Development Deployment

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements_urban_planning.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your GCP credentials

# 3. Run the agent
python urban_planning_agent.py

# 4. Test the deployment
python test.py
```

### Development Server
```bash
# Run with Flask development server
export FLASK_APP=urban_planning_agent.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000
```

---

## 🔧 Production Configuration

### Environment Variables
```bash
# Performance
MAX_WORKERS=4
MEMORY_LIMIT=8GB
TIMEOUT=300

# Security
SECRET_KEY="your-secret-key-here"
ALLOWED_HOSTS="your-domain.com,api.your-domain.com"

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30

# Caching
REDIS_URL="redis://localhost:6379"
CACHE_TTL=3600
```

### Database Setup (Optional)
```bash
# PostgreSQL for persistent storage
DATABASE_URL="postgresql://user:password@localhost/urban_planning"

# Initialize database
python -c "from urban_planning_agent import init_db; init_db()"
```

---

## 📊 Monitoring & Scaling

### Health Checks
```bash
# Health endpoint
curl http://localhost:8000/health

# Metrics endpoint
curl http://localhost:8000/metrics
```

### Logging
```bash
# View application logs
docker logs urban-planning-agent

# GCP Cloud Logging
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=urban-planning-agent"
```

### Scaling Configuration
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: urban-planning-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: urban-planning-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 🔒 Security Best Practices

### 1. Secret Management
- Use GCP Secret Manager for sensitive data
- Rotate service account keys regularly
- Never commit secrets to version control

### 2. Network Security
```bash
# Firewall rules
gcloud compute firewall-rules create allow-urban-planning \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow access to urban planning agent"
```

### 3. SSL/TLS
```bash
# Enable HTTPS
gcloud compute ssl-certificates create urban-planning-cert \
  --certificate certificate.crt \
  --private-key private.key
```

---

## 🚀 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Urban Planning Agent

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: pip install -r requirements_urban_planning.txt

    - name: Run tests
      run: python test.py

    - name: Build and push Docker image
      run: |
        docker build -t urban-planning-agent:latest .
        docker tag urban-planning-agent:latest gcr.io/YOUR_PROJECT/urban-planning-agent:latest
        docker push gcr.io/YOUR_PROJECT/urban-planning-agent:latest

    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy urban-planning-agent \
          --image gcr.io/YOUR_PROJECT/urban-planning-agent:latest \
          --region us-central1 \
          --platform managed
```

---

## 📈 Performance Optimization

### Memory Management
```python
# In urban_planning_agent.py
import gc
import psutil

def optimize_memory():
    # Force garbage collection
    gc.collect()

    # Monitor memory usage
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        # Implement memory optimization strategies
        pass
```

### Caching Strategy
```python
from cachetools import TTLCache

# Global cache for expensive operations
analysis_cache = TTLCache(maxsize=1000, ttl=3600)

def cached_analysis(func):
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in analysis_cache:
            return analysis_cache[key]

        result = func(*args, **kwargs)
        analysis_cache[key] = result
        return result
    return wrapper
```

---

## 🐛 Troubleshooting

### Common Issues

1. **GCP Authentication Failed**
   ```bash
   # Check service account permissions
   gcloud iam service-accounts get-iam-policy YOUR_SERVICE_ACCOUNT

   # Test authentication
   gcloud auth application-default login
   ```

2. **Memory Issues**
   ```bash
   # Increase memory limits
   docker run --memory=4g urban-planning-agent

   # Monitor memory usage
   docker stats
   ```

3. **Port Conflicts**
   ```bash
   # Find process using port
   lsof -i :8000

   # Kill process
   kill -9 PID
   ```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- [ ] Update dependencies monthly
- [ ] Rotate GCP service account keys quarterly
- [ ] Monitor performance metrics weekly
- [ ] Backup data and configurations daily
- [ ] Review and update security policies monthly

### Getting Help
- Check the logs: `docker logs urban-planning-agent`
- Review GCP console for errors
- Check application health: `GET /health`
- Monitor metrics: `GET /metrics`

---

## 🎯 Quick Deployment Checklist

- [ ] GCP project created and billing enabled
- [ ] Service account created with required permissions
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Tests passing
- [ ] Docker image built (optional)
- [ ] Application deployed
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Backup strategy in place

---

*For detailed API documentation, see the README files in the project repository.*
