# 🛠️ Complete Installation & Setup Guide

## 📋 Pre-Installation Checklist

### Required Software
- ✅ **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- ✅ **Docker Compose** v2.0+
- ✅ **Git** (for cloning)
- ✅ **Text Editor** (VS Code recommended)

### Required Accounts
- ✅ **SiliconFlow Account** (Free tier available)
  - Sign up at: https://siliconflow.cn
  - Get API key from dashboard

### Optional (For Monitoring)
- ⭕ **Langfuse Account** (Free tier available)
  - Sign up at: https://langfuse.com
  - Get API keys from settings

---

## 🚀 Installation Steps

### Step 1: Download Project

**Option A: From provided folder**
```bash
# Extract the ai-vision-agent-pro folder
# Navigate to it
cd ai-vision-agent-pro
```

**Option B: Clone from GitHub**
```bash
git clone https://github.com/yourusername/ai-vision-agent-pro.git
cd ai-vision-agent-pro
```

### Step 2: Verify Docker Installation

```bash
# Check Docker
docker --version
# Should show: Docker version 20.10.x or higher

# Check Docker Compose
docker-compose --version
# Should show: Docker Compose version 2.x.x or higher
```

### Step 3: Configure Backend Environment

```bash
# Copy example environment file
cp backend/.env.example backend/.env

# Edit the file
# Windows: notepad backend/.env
# Mac/Linux: nano backend/.env
# VS Code: code backend/.env
```

**Required Configuration:**
```env
# REQUIRED - Get from https://siliconflow.cn
SILICONFLOW_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# OPTIONAL - For monitoring
LANGFUSE_ENABLED=false
# If enabling Langfuse, add:
# LANGFUSE_PUBLIC_KEY=pk-xxxxx
# LANGFUSE_SECRET_KEY=sk-xxxxx
```

### Step 4: Run Setup Script (Optional but Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
# Manually run these commands:
cp backend\.env.example backend\.env
echo VITE_API_URL=http://localhost:8000 > frontend\.env
```

### Step 5: Build and Start Services

```bash
# Build Docker images (first time only)
docker-compose build

# Start all services
docker-compose up -d

# View logs (optional)
docker-compose logs -f
```

**Expected Output:**
```
Creating network "ai-vision-agent-pro_ai-vision-network" ... done
Creating ai-vision-backend ... done
Creating ai-vision-frontend ... done
```

### Step 6: Verify Services

**Check if services are running:**
```bash
docker-compose ps
```

**Expected output:**
```
NAME                  STATUS
ai-vision-backend     Up (healthy)
ai-vision-frontend    Up
```

### Step 7: Access the Application

Open your browser and visit:

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🧪 Test Installation

### Quick Health Check

```bash
# Test backend
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy","timestamp":"2024-xx-xx...","active_tasks":0}
```

### Generate Test Image

```bash
# Run test script
python test_api.py

# Follow prompts
# Select 'y' to run generation test
```

### Manual UI Test

1. Open http://localhost:5173
2. Enter prompt: `"A serene mountain landscape"`
3. Click **Generate Image**
4. Wait 30-60 seconds
5. Image should appear
6. Click **Download** to save

---

## 🔧 Troubleshooting

### Problem: "Docker not found"

**Solution:**
```bash
# Install Docker
# Windows/Mac: Download Docker Desktop
# https://www.docker.com/products/docker-desktop

# Linux:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Problem: "Port already in use"

**Solution:**
```bash
# Check what's using port 8000
# Linux/Mac:
lsof -i :8000

# Windows:
netstat -ano | findstr :8000

# Stop the conflicting service or change port in docker-compose.yml
```

### Problem: "SILICONFLOW_API_KEY not set"

**Solution:**
```bash
# 1. Check if .env exists
ls backend/.env

# 2. Verify content
cat backend/.env

# 3. Ensure no spaces around =
# CORRECT:   SILICONFLOW_API_KEY=sk-xxxxx
# INCORRECT: SILICONFLOW_API_KEY = sk-xxxxx

# 4. Restart backend
docker-compose restart backend
```

### Problem: "Services won't start"

**Solution:**
```bash
# View detailed logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problem: "Frontend shows connection error"

**Solution:**
```bash
# 1. Check backend is running
curl http://localhost:8000/api/v1/health

# 2. Check CORS settings in backend/.env
# Ensure FRONTEND_URL=http://localhost:5173

# 3. Clear browser cache
# Chrome: Ctrl+Shift+Delete

# 4. Restart services
docker-compose restart
```

### Problem: "Image generation fails"

**Solution:**
```bash
# 1. Verify API key is valid
# Login to siliconflow.cn and check key

# 2. Check backend logs
docker-compose logs backend | grep ERROR

# 3. Test API key manually
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test image","max_iterations":1}'

# 4. Check SiliconFlow service status
# Visit: https://status.siliconflow.cn
```

---

## 📊 Monitoring Setup (Optional)

### Enable Langfuse

1. **Create Langfuse Account**
   - Visit: https://langfuse.com
   - Sign up (free)
   - Create new project

2. **Get API Keys**
   - Go to Settings → API Keys
   - Create new key pair
   - Copy Public Key and Secret Key

3. **Configure Backend**
   ```bash
   # Edit backend/.env
   LANGFUSE_ENABLED=true
   LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx
   LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```

4. **Restart Services**
   ```bash
   docker-compose restart backend
   ```

5. **View Traces**
   - Generate an image
   - Visit Langfuse dashboard
   - See generation traces, steps, and metrics

---

## 🔄 Updating the Application

### Pull Latest Changes
```bash
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Update Dependencies

**Backend:**
```bash
cd backend
# Edit requirements.txt
docker-compose build backend
docker-compose up -d backend
```

**Frontend:**
```bash
cd frontend
# Edit package.json
docker-compose build frontend
docker-compose up -d frontend
```

---

## 🛑 Stopping Services

### Temporary Stop
```bash
# Stop services (keeps data)
docker-compose stop

# Start again
docker-compose start
```

### Complete Shutdown
```bash
# Stop and remove containers
docker-compose down

# Remove all data (volumes)
docker-compose down -v
```

---

## 🎯 Common Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart specific service
docker-compose restart backend

# Rebuild specific service
docker-compose build --no-cache backend
docker-compose up -d backend

# Enter container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Check resource usage
docker stats

# Clean up everything
docker-compose down -v
docker system prune -a
```

---

## 📱 Development Mode

### Backend Local Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Local Development
```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Access at http://localhost:5173
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Change default ports
- [ ] Use strong API keys
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Use environment-specific .env files
- [ ] Enable rate limiting
- [ ] Set up monitoring alerts
- [ ] Regular security updates
- [ ] Backup important data
- [ ] Review CORS settings

---

## 📈 Performance Optimization

### For Better Performance:

1. **Use Production Build**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Enable Caching**
   - Add Redis for task storage
   - Cache API responses

3. **Scale Services**
   ```bash
   docker-compose up -d --scale backend=3
   ```

4. **Monitor Resources**
   ```bash
   docker stats
   ```

---

## 🎓 Learning Resources

### Official Documentation
- [Docker Docs](https://docs.docker.com)
- [FastAPI Tutorial](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)
- [LangGraph Guide](https://python.langchain.com/docs/langgraph)

### Video Tutorials
- Docker Basics: Search "Docker Tutorial" on YouTube
- FastAPI Course: FastAPI Official Playlist
- React Crash Course: Official React Docs

---

## ✅ Installation Complete!

You should now have:
- ✅ Running backend at localhost:8000
- ✅ Running frontend at localhost:5173
- ✅ Ability to generate images
- ✅ Full documentation access

### Next Steps:
1. Generate your first image
2. Explore the API docs
3. Try different prompts
4. Enable monitoring (optional)
5. Customize the UI (optional)

---

## 🆘 Need Help?

1. Check [README.md](README.md)
2. Review [QUICKSTART.md](QUICKSTART.md)
3. Run `test_api.py`
4. Check Docker logs
5. Visit GitHub Issues

**Happy creating! 🎨**
