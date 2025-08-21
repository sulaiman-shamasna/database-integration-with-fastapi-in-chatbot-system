# Database Integration with FastAPI in Chatbot System

![DB-System](plots/DB-System.svg)

A modern, production-ready chatbot system built with FastAPI, featuring database integration, LLM capabilities, and a well-structured architecture.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- OpenAI API key

### Installation

1. **Clone the repository**
    ```bash
    git clone git@github.com:sulaiman-shamasna/database-integration-with-fastapi-in-chatbot-system.git
    cd database-integration-with-fastapi-in-chatbot-system
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**
    ```bash
    cp .env.example .env
    # Edit .env with your database credentials and OpenAI API key
    ```

4. **Initialize database**
    ```bash
    # Create PostgreSQL database
    createdb ChatbotApplicationDatabase
    
    # Run migrations
    alembic upgrade head
    ```

5. **Start the application**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

6. **Access the API**
    - **Swagger UI**: http://localhost:8000/docs
    - **ReDoc**: http://localhost:8000/redoc
    - **Health Check**: http://localhost:8000/

## 🏗️ Project Structure

```
├── 📁 alembic/                    # Database migrations
├── 📁 learn-more/                 # 📚 Detailed documentation
├── 📁 repositories/               # Data access layer
├── 📁 routers/                    # API endpoints
├── 📁 services/                   # Business logic layer
├── 📁 plots/                      # Architecture diagrams
├── 📄 main.py                     # FastAPI application entry point
├── 📄 models.py                   # SQLAlchemy models
├── 📄 schemas.py                  # Pydantic schemas
├── 📄 database.py                 # Database configuration
├── 📄 settings.py                 # Application settings
└── 📄 requirements.txt            # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Application Settings
APP_NAME=Chatbot Application
DEBUG=false
ENVIRONMENT=development

# Database Configuration
# Option 1: Use a single DATABASE_URL (recommended for production)
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name

# Option 2: Use individual database components
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ChatbotApplicationDatabase
DB_USER=postgres
DB_PASSWORD=your_secure_password

# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# (Optional) Vector Database Settings — currently not used
# VECTOR_DB_TYPE=memory
# SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

**Note**: 
- `OPENAI_API_KEY` is required and will cause an error if not provided
- If using `DATABASE_URL`, individual DB components are optional
- If not using `DATABASE_URL`, `DB_PASSWORD` is required
- All other settings have sensible defaults

## 📚 API Endpoints

### Conversation Management
- `GET /conversations` - List conversations
- `GET /conversations/{id}` - Get conversation details
- `POST /conversations` - Create conversation
- `PUT /conversations/{id}` - Update conversation
- `DELETE /conversations/{id}` - Delete conversation
- `GET /conversations/{id}/messages` - Get conversation messages

### LLM Integration
- `POST /llm/conversations` - Create conversation with AI title
- `POST /llm/text/generate` - Generate AI response
- `POST /llm/text/generate/stream` - Stream AI response

## 🧪 Testing

Test the API using Swagger UI at http://localhost:8000/docs or use curl:

```bash
# Health check
curl http://localhost:8000/

# Create a conversation
curl -X POST "http://localhost:8000/llm/conversations" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Tell me about Python programming"}'

# Generate AI response
curl -X POST "http://localhost:8000/llm/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What are the benefits of Python?", "conversation_id": 1}'
```

## 📖 Documentation

- **📚 [Learn More](./learn-more/README.md)** - Comprehensive project documentation
- **🔧 [API Docs](./learn-more/README.md#api-design)** - Detailed API documentation
- **🏗️ [Architecture](./learn-more/README.md#system-architecture)** - System design and patterns
- **💾 [Database](./learn-more/README.md#database-design)** - Database schema and design
- **🤖 [LLM Integration](./learn-more/README.md#llm-integration)** - AI integration details

## 🛠️ Development

### Key Features
- 🤖 **AI-Powered Conversations**: OpenAI GPT-3.5-turbo integration
- 💾 **Persistent Storage**: PostgreSQL with SQLAlchemy ORM
- 🚀 **High Performance**: Async/await architecture
- 📚 **Auto-Documentation**: OpenAPI/Swagger generation
- 🔄 **Database Migrations**: Alembic version control
- 🌐 **RESTful API**: Clean, consistent design
- 🔒 **Environment Security**: Secure configuration management

### Architecture Patterns
- **Repository Pattern**: Abstract data access layer
- **Service Layer**: Business logic encapsulation
- **Dependency Injection**: FastAPI's built-in DI system
- **Layered Architecture**: Clear separation of concerns

## 🚀 Deployment

### Production Considerations
- Use production PostgreSQL instance
- Set `DEBUG=false` in production
- Configure proper logging and monitoring
- Set up reverse proxy (nginx)
- Use process manager (systemd, supervisor)
- Implement health checks and monitoring


<!-- ### Docker Support
```bash
# Build and run with Docker
docker build -t chatbot-system .
docker run -p 8000:8000 chatbot-system
``` -->

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **PostgreSQL**: https://www.postgresql.org/
- **OpenAI**: https://platform.openai.com/
- **Alembic**: https://alembic.sqlalchemy.org/

---

**Need more details?** Check out our [📚 comprehensive documentation](./learn-more/README.md) for in-depth information about architecture, design patterns, and implementation details.



