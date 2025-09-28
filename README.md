# 🚀 YieldSync - AI-Powered DeFi Investment Platform

**YieldSync** is the first **AI-powered, multi-chain pooled investment platform** for DeFi. We start with **Stage 1 AI recommendations**, then evolve into **full investment execution** — solo or group — with on-chain governance and multi-chain support.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Development](#-development)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Stage 1 (Current)
- 🤖 **AI-Powered Recommendations** - Personalized DeFi investment suggestions
- 🔗 **Multi-Chain Wallet Integration** - Connect wallets across different blockchains
- 📊 **Real-Time Pool Analysis** - Live data from DefiLlama API
- 🎯 **Risk Scoring** - Comprehensive risk assessment algorithm
- 📈 **Portfolio Tracking** - Monitor wallet activity and token transfers
- 👤 **User Profiling** - Risk tolerance and experience-based customization

### Future Stages
- 💰 **Full Investment Execution** - Automated DeFi investments
- 🏛️ **On-Chain Governance** - Decentralized decision making
- 👥 **Group Investments** - Collaborative investment strategies

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Celery Worker │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Background)  │
│   Port: 3000    │    │   Port: 8000    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   PostgreSQL    │              │
         └──────────────►│   Database      │◄─────────────┘
                        │   Port: 5432    │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │     Redis       │
                        │   Port: 6379    │
                        └─────────────────┘
```

### Tech Stack

**Backend:**
- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Primary database
- Redis - Caching & task queue
- Celery - Background task processing
- Alembic - Database migrations
- Google Gemini AI - AI recommendations

**Frontend:**
- Next.js 15 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Lucide React - Icons

**Infrastructure:**
- Docker & Docker Compose - Containerization
- DefiLlama API - DeFi data source

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (v20.10+) - [Download here](https://docs.docker.com/get-docker/)
- **Docker Compose** (v2.0+) - [Download here](https://docs.docker.com/compose/install/)
- **Git** - [Download here](https://git-scm.com/downloads)

### Optional (for local development):
- **Node.js** (v18+) - [Download here](https://nodejs.org/)
- **Python** (v3.11+) - [Download here](https://python.org/)
- **PostgreSQL** (v15+) - [Download here](https://postgresql.org/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yieldsync.git
cd yieldsync
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=yieldsync
POSTGRES_SERVER=db
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Environment
ENV=production
PROJECT_NAME=YieldSync AI

# Optional: Add your API keys
# GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 📦 Installation

### Method 1: Docker (Recommended)

This is the easiest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/yieldsync.git
cd yieldsync

# 2. Create environment file
cp .env.example .env

# 3. Start all services
docker-compose up --build

# 4. Run database migrations
docker-compose exec api alembic upgrade head
```

### Method 2: Local Development

If you prefer to run services locally:

#### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your local database settings

# 5. Run database migrations
alembic upgrade head

# 6. Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend/YieldSync

# 2. Install dependencies
npm install

# 3. Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 4. Start the development server
npm run dev
```

#### Database Setup

```bash
# 1. Install PostgreSQL
# Follow instructions for your OS

# 2. Create database
createdb yieldsync

# 3. Run migrations
cd backend
alembic upgrade head
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=yieldsync
POSTGRES_SERVER=db
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Environment
ENV=production
PROJECT_NAME=YieldSync AI

# API Keys (Optional)
GEMINI_API_KEY=your_gemini_api_key_here
DEFILLAMA_API_KEY=your_defillama_api_key_here
```

### Docker Configuration

The application uses Docker Compose with the following services:

- **frontend**: Next.js application
- **api**: FastAPI backend
- **worker**: Celery background worker
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker

## 🛠️ Development

### Development Mode

For development with hot reload:

```bash
# Use development compose file
docker-compose -f docker-compose.dev.yml up --build
```

### Available Scripts

#### Backend Scripts

```bash
# Run tests
docker-compose exec api python -m pytest

# Run database migrations
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Access database shell
docker-compose exec db psql -U admin -d yieldsync

# Access Redis CLI
docker-compose exec redis redis-cli
```

#### Frontend Scripts

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

### Code Structure

```
yieldsync/
├── backend/                 # Backend API
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── main.py         # FastAPI app
│   │   └── worker.py       # Celery worker
│   ├── tests/              # Test files
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/YieldSync/     # Frontend application
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   ├── data/               # Static data
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Production setup
├── docker-compose.dev.yml  # Development setup
└── README.md              # This file
```

## 📚 API Documentation

### Interactive API Docs

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Health Check
```http
GET /health
```

#### Users
```http
GET /users          # Get all users
POST /users         # Create user
GET /users/{id}     # Get user by ID
```

#### Wallets
```http
GET /wallets        # Get all wallets
POST /wallets       # Create wallet
GET /wallets/{id}   # Get wallet by ID
```

#### Pools
```http
GET /pools          # Get all DeFi pools
GET /pools/{id}     # Get pool by ID
```

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Get all pools
curl http://localhost:8000/pools

# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using the port
lsof -i :3000  # or :8000, :5432, :6379

# Kill the process
kill -9 <PID>
```

#### 2. Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up --build
```

#### 3. Frontend Can't Connect to Backend

- Ensure backend is running on port 8000
- Check CORS configuration in `backend/app/main.py`
- Verify `NEXT_PUBLIC_API_URL` environment variable

#### 4. Docker Build Issues

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs frontend
docker-compose logs worker

# Follow logs in real-time
docker-compose logs -f api
```

### Database Issues

```bash
# Access database
docker-compose exec db psql -U admin -d yieldsync

# Run migrations
docker-compose exec api alembic upgrade head

# Reset database
docker-compose exec db psql -U admin -c "DROP DATABASE yieldsync;"
docker-compose exec db psql -U admin -c "CREATE DATABASE yieldsync;"
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** for your changes
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/yieldsync/issues)
3. Create a new issue with detailed information
4. Join our [Discord community](https://discord.gg/yieldsync)

## 🙏 Acknowledgments

- [DefiLlama](https://defillama.com/) for DeFi data
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Google Gemini](https://ai.google.dev/) for AI capabilities

---

**Made with ❤️ by the YieldSync team**
