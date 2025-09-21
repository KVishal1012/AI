# 🚀 Urban Planning Agent - Quick Start Guide

## 🎯 Choose Your Deployment Method

### Option 1: Quick Local Deployment (Recommended for Testing)
```bash
# 1. Make sure you have your .env file configured
cp .env.example .env
# Edit .env with your GCP credentials

# 2. Run the deployment script
./deploy.sh

# Choose option 1 (Deploy Locally) from the menu
```

### Option 2: Docker Compose (Recommended for Development)
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your GCP credentials

# 2. Deploy with Docker Compose
docker-compose up -d

# 3. Check status
docker-compose ps
docker-compose logs -f urban-planning-agent
```

### Option 3: Google Cloud Run (Recommended for Production)
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your GCP credentials

# 2. Run deployment script
./deploy.sh

# Choose option 3 (Deploy to Google Cloud Run) from the menu
```

---

## 📋 Pre-Deployment Checklist

### ✅ GCP Setup (Required for AI features)
- [ ] Create Google Cloud Project
- [ ] Enable Vertex AI API
- [ ] Enable Cloud Storage API
- [ ] Create Service Account with required permissions
- [ ] Download and base64-encode service account key
- [ ] Add credentials to `.env` file

### ✅ Local Setup
- [ ] Install Docker and Docker Compose
- [ ] Clone the repository
- [ ] Configure `.env` file
- [ ] Run `pip install -r requirements_urban_planning.txt` (optional)

---

## 🔧 Configuration Files Created

| File | Purpose | Status |
|------|---------|--------|
| `Dockerfile.urban-planning` | Docker container definition | ✅ Created |
| `docker-compose.yml` | Multi-service deployment | ✅ Created |
| `app.yaml` | Google App Engine config | ✅ Created |
| `k8s-deployment.yaml` | Kubernetes deployment | ✅ Created |
| `deploy.sh` | Interactive deployment script | ✅ Created |
| `DEPLOYMENT_GUIDE.md` | Comprehensive deployment guide | ✅ Created |

---

## 🌐 Access Your Deployed Agent

### Local Deployment
- **URL:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **Logs:** `docker logs urban-planning-agent`

### Cloud Run Deployment
- **URL:** Provided by `gcloud run deploy` command
- **Health Check:** `YOUR_URL/health`
- **Logs:** `gcloud logging read "resource.type=cloud_run_revision"`

### Docker Compose
- **URL:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **Logs:** `docker-compose logs -f urban-planning-agent`

---

## 🧪 Testing Your Deployment

### Run the Test Suite
```bash
# Test locally
python test.py

# Test in container
docker exec urban-planning-agent python test.py
```

### Health Check
```bash
# Check if service is responding
curl http://localhost:8000/health

# Should return: {"status": "healthy", "timestamp": "..."}
```

### AI Features Test
```bash
# Test AI capabilities
python -c "
from urban_planning_agent import UrbanPlanningAgent
agent = UrbanPlanningAgent()
print('✅ AI features working!')
"
```

---

## 📊 Monitoring & Troubleshooting

### View Logs
```bash
# Docker
docker logs urban-planning-agent

# Docker Compose
docker-compose logs -f

# Cloud Run
gcloud logging read
```

### Common Issues

1. **GCP Authentication Failed**
   ```bash
   # Check .env file
   cat .env

   # Test GCP credentials
   gcloud auth application-default login
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000

   # Kill the process
   kill -9 PID
   ```

3. **Memory Issues**
   ```bash
   # Increase Docker memory
   docker run --memory=4g urban-planning-agent

   # Or in docker-compose.yml
   services:
     urban-planning-agent:
       deploy:
         resources:
           limits:
             memory: 4G
   ```

---

## 🎯 Next Steps

1. **Test the Agent:** Run `python test.py` to verify functionality
2. **Explore Features:** Check the examples in `urban_planning_agent_examples.py`
3. **Customize:** Modify the agent for your specific urban planning needs
4. **Scale:** Use the deployment configurations for production scaling
5. **Monitor:** Set up logging and monitoring for production deployments

---

## 📞 Support

- **Documentation:** See `DEPLOYMENT_GUIDE.md` for detailed instructions
- **Logs:** Check container logs for error details
- **Health:** Use `/health` endpoint to verify service status
- **Tests:** Run `python test.py` to validate functionality

---

*🎉 Your Urban Planning Agent is ready for deployment! Choose the option that best fits your needs and start transforming urban planning with AI.*
