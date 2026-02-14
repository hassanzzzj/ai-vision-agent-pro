# 🚀 Quick Start Guide

Get AI Vision Agent Pro running in 5 minutes!

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- SiliconFlow API key ([Get free key](https://siliconflow.cn))

## Step 1: Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-vision-agent-pro.git
cd ai-vision-agent-pro

# Run setup script (Linux/Mac)
./setup.sh

# OR manually setup (Windows)
cp backend/.env.example backend/.env
# Edit backend/.env and add your SILICONFLOW_API_KEY
```

## Step 2: Configure API Key

Edit `backend/.env`:

```env
SILICONFLOW_API_KEY=your_key_here
```

**Get your key:**
1. Visit https://siliconflow.cn
2. Sign up (free)
3. Go to API Keys section
4. Copy your key

## Step 3: Launch

```bash
docker-compose up -d
```

Wait 30-60 seconds for services to start.

## Step 4: Access

Open browser:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## Step 5: Generate Your First Image

1. Enter a prompt: `"A futuristic city at night with neon lights"`
2. Click **Generate Image**
3. Wait ~30 seconds
4. Download your image!

## 🎉 That's it!

### Troubleshooting

**Services not starting?**
```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose restart
```

**API key error?**
- Verify key in `backend/.env`
- Check no extra spaces
- Restart: `docker-compose restart backend`

**Port already in use?**
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3000:80"    # Frontend
```

### Next Steps

- Read [README.md](README.md) for full documentation
- Try different prompts
- Adjust max iterations for quality
- Enable Langfuse for monitoring

### Common Prompts to Try

```
A serene mountain landscape with aurora borealis
A cute robot reading a book in a cozy library
An astronaut riding a horse on Mars
A cyberpunk street market with holographic signs
```

### Stop Services

```bash
docker-compose down
```

### Need Help?

- [Full Documentation](README.md)
- [GitHub Issues](https://github.com/yourusername/ai-vision-agent-pro/issues)
- [Contributing Guide](CONTRIBUTING.md)

Happy generating! 🎨
