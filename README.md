# Clario Backend

A basic FastAPI backend server with RESTful API endpoints.

## Features

- FastAPI framework with automatic API documentation
- CORS middleware enabled
- Health check endpoint
- CRUD operations for items
- Pydantic models for data validation
- Hot reload for development

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

#### Option 1: Using the runner script
```bash
python run_server.py
```

#### Option 2: Direct uvicorn command
```bash
cd .venv/app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Option 3: Using environment variables
```bash
# Set custom configuration
export HOST=0.0.0.0
export PORT=8000
export RELOAD=true
export LOG_LEVEL=info

python run_server.py
```

## API Endpoints

### Base URLs
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/items` | Get all items |
| GET | `/items/{item_id}` | Get specific item |
| POST | `/items` | Create new item |
| PUT | `/items/{item_id}` | Update item |
| DELETE | `/items/{item_id}` | Delete item |

### Example Usage

#### Create an item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Sample Item", "description": "A test item", "price": 29.99}'
```

#### Get all items
```bash
curl "http://localhost:8000/items"
```

#### Get specific item
```bash
curl "http://localhost:8000/items/1"
```

## Development

The server runs with hot reload enabled by default, so any changes to the code will automatically restart the server.

## Production Deployment

For production deployment:

1. Set `RELOAD=false` in environment variables
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS origins
4. Add database integration
5. Implement proper authentication and authorization

### Example Production Command
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## Project Structure

```
Clario/
├── .venv/
│   └── app/
│       └── main.py          # Main FastAPI application
├── requirements.txt         # Python dependencies
├── run_server.py           # Server runner script
└── README.md              # This file
```
