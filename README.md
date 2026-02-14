# 🎨 AI Vision Agent Pro

**Professional-grade Agentic Image Generation Platform**

Powered by LangGraph, SiliconFlow, and Langfuse for observable, iterative AI-driven image creation.

---

## 🌟 Features

### Core Capabilities
- ✨ **Agentic Workflow**: LangGraph-powered multi-step generation pipeline
- 🎯 **Intelligent Planning**: Automatic prompt optimization
- 🔄 **Iterative Refinement**: Quality-driven regeneration loop
- 📊 **Real-time Monitoring**: Langfuse integration for observability
- 🎨 **Professional UI**: Modern React interface with Tailwind CSS
- 🐳 **Docker Ready**: One-command deployment

### Workflow Architecture

```
User Prompt → Planner → Human Approval → Generator → Critic
                                            ↑            ↓
                                            └────────────┘
                                          (Iterative Loop)
```

**Nodes:**
1. **Planner**: Optimizes user prompts for better results
2. **Human Approval**: Optional human-in-the-loop checkpoint
3. **Generator**: Creates image using SiliconFlow API
4. **Critic**: Evaluates quality and decides on regeneration

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- SiliconFlow API Key ([Get one here](https://siliconflow.cn))
- (Optional) Langfuse account for monitoring

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-vision-agent-pro.git
cd ai-vision-agent-pro
```

2. **Configure environment**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys
```

Required environment variables:
```env
SILICONFLOW_API_KEY=your_api_key_here
LANGFUSE_ENABLED=false  # Set to true if using Langfuse
```

3. **Launch with Docker**
```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
/ai-vision-agent-pro
│
├── 📂 backend/                  # FastAPI + LangGraph
│   ├── 📂 app/
│   │   ├── 📂 api/              # REST endpoints
│   │   │   └── v1_routes.py     # /generate, /status, /feedback
│   │   ├── 📂 agent/            # LangGraph logic
│   │   │   ├── graph.py         # Workflow definition
│   │   │   ├── nodes.py         # Node functions
│   │   │   └── state.py         # State schema
│   │   ├── 📂 services/
│   │   │   ├── silicon_flow.py  # Image generation API
│   │   │   └── monitor.py       # Langfuse tracking
│   │   └── main.py              # FastAPI app
│   ├── .env                     # Environment variables
│   ├── Dockerfile.backend
│   └── requirements.txt
│
├── 📂 frontend/                 # React + Vite
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── ImageCanvas.jsx  # Image display
│   │   │   └── PromptBar.jsx    # Input interface
│   │   ├── 📂 hooks/
│   │   │   └── useImageGeneration.js
│   │   └── App.jsx
│   ├── Dockerfile.frontend
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Development Setup

### Backend (Local Development)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Local Development)

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

---

## 📡 API Reference

### POST `/api/v1/generate`
Start image generation workflow.

**Request:**
```json
{
  "prompt": "A futuristic city at night",
  "max_iterations": 3,
  "enable_monitoring": true
}
```

**Response:**
```json
{
  "task_id": "uuid-here",
  "status": "accepted",
  "message": "Image generation started"
}
```

### GET `/api/v1/status/{task_id}`
Get generation status.

**Response:**
```json
{
  "task_id": "uuid",
  "status": "completed",
  "progress": 100,
  "current_step": "done",
  "generated_image": "base64_image_data",
  "feedback": "Excellent quality!",
  "quality_score": 0.92
}
```

### POST `/api/v1/feedback`
Submit user feedback.

**Request:**
```json
{
  "task_id": "uuid",
  "rating": 0.9,
  "comment": "Great result!"
}
```

---

## 🎯 Usage Examples

### Basic Generation
```python
import requests

response = requests.post('http://localhost:8000/api/v1/generate', json={
    'prompt': 'A serene mountain landscape with aurora borealis',
    'max_iterations': 3
})

task_id = response.json()['task_id']
```

### Check Status
```python
status = requests.get(f'http://localhost:8000/api/v1/status/{task_id}')
print(status.json())
```

---

## 🔧 Configuration

### Backend Settings

**Environment Variables:**
- `ENVIRONMENT`: development/production
- `SILICONFLOW_API_KEY`: Your SiliconFlow API key
- `LANGFUSE_ENABLED`: Enable/disable monitoring
- `LANGFUSE_PUBLIC_KEY`: Langfuse public key
- `LANGFUSE_SECRET_KEY`: Langfuse secret key

### Frontend Settings

**Environment Variables:**
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

---

## 📊 Monitoring with Langfuse

1. Create account at [langfuse.com](https://langfuse.com)
2. Get API keys from dashboard
3. Update backend/.env:
```env
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=pk-xxx
LANGFUSE_SECRET_KEY=sk-xxx
```

4. View traces in Langfuse dashboard:
   - Generation steps
   - Quality scores
   - Performance metrics
   - User feedback

---

## 🎨 Customization

### Add Custom Nodes

Edit `backend/app/agent/nodes.py`:

```python
async def custom_node(state: AgentState) -> Dict[str, Any]:
    # Your custom logic
    return {"updated_state": "value"}
```

Update workflow in `backend/app/agent/graph.py`:

```python
workflow.add_node("custom", custom_node)
workflow.add_edge("planner", "custom")
```

### Modify UI Theme

Edit `frontend/tailwind.config.js` for colors:

```javascript
colors: {
  primary: {
    500: '#your-color',
  }
}
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "SILICONFLOW_API_KEY not set"**
- Solution: Add API key to `backend/.env`

**2. CORS errors**
- Solution: Check FRONTEND_URL in backend/.env
- Ensure frontend runs on correct port

**3. Docker build fails**
- Solution: Run `docker-compose down -v` then rebuild

**4. Image generation timeout**
- Solution: Increase `num_inference_steps` or check API status

### Debugging

Enable debug mode:
```bash
# Backend
export LOG_LEVEL=DEBUG

# View logs
docker-compose logs -f backend
```

---

## 🚀 Deployment

### Production Deployment

1. **Update environment variables**
```env
ENVIRONMENT=production
FRONTEND_URL=https://yourdomain.com
```

2. **Use production-ready secrets**
- Store API keys securely (AWS Secrets Manager, etc.)
- Use environment-specific .env files

3. **Enable HTTPS**
- Configure nginx/reverse proxy
- Add SSL certificates

4. **Scale with Docker Swarm/Kubernetes**
```bash
docker stack deploy -c docker-compose.yml ai-vision
```

---

## 📈 Performance Tips

1. **Caching**: Implement Redis for task storage
2. **Rate Limiting**: Add rate limits to API endpoints
3. **CDN**: Serve frontend via CDN
4. **Database**: Use PostgreSQL for production
5. **Queue**: Add Celery for background tasks

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 License

MIT License - see LICENSE file

---

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agentic workflows
- [SiliconFlow](https://siliconflow.cn) - Image generation API
- [Langfuse](https://langfuse.com) - LLM observability
- [FastAPI](https://fastapi.tiangolo.com) - Backend framework
- [React](https://react.dev) - Frontend library

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-vision-agent-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-vision-agent-pro/discussions)
- **Email**: support@yourdomain.com

---

## 🗺️ Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Multiple model support (DALL-E, Midjourney)
- [ ] Image editing capabilities
- [ ] Batch generation
- [ ] User authentication
- [ ] Gallery/history feature
- [ ] Advanced prompt engineering tools

---

**Made with ❤️ for the AI community**

⭐ Star this repo if you find it useful!
