# Clario Backend

A FastAPI-based backend application for Clario, featuring ML-powered learning resource recommendations and Google OAuth2 authentication.

## Features

- **ML-Powered Recommendations**: TF-IDF and cosine similarity-based learning resource recommendations
- **Google OAuth2 Authentication**: Secure authentication using Google OAuth2
- **RESTful API**: Clean, well-documented API endpoints
- **Database Integration**: SQLite database with flexible raw SQL queries
- **Real-time Ready**: Architecture ready for real-time features

## Project Structure

```
backend/
├── app/
│   ├── main.py                       # FastAPI entry point
│   ├── config.py                     # Configuration settings
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py            # Authentication endpoints
│   │   ├── user_routes.py            # User management endpoints
│   │   ├── ml_routes.py              # ML recommendation endpoints
│   │   ├── system_routes.py          # System health and status
│   │   └── routes.py                 # Main router
│   ├── ml/                           # ML package
│   │   ├── __init__.py
│   │   ├── recommender.py            # Core recommendation logic
│   │   ├── preprocess.py             # NLP preprocessing utilities
│   │   ├── model/                    # Saved ML models
│   │   ├── data/                     # ML datasets
│   │   ├── utils/                    # ML utilities
│   │   └── tests/                    # ML tests
│   ├── services/
│   │   └── auth_service.py           # Authentication service
│   ├── utils/
│   │   └── db_utils.py               # Database utilities
│   └── schemas/
│       └── ml_schema.py              # Pydantic models
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=app/data/clario.db

# ML Configuration
ML_DATA_DIR=app/ml/data
ML_MODEL_DIR=app/ml/model

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Google OAuth2 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Create credentials (OAuth 2.0 Client ID)
5. Add authorized redirect URIs:
   - `http://localhost:8000/api/v1/auth/google/callback` (development)
   - Your production callback URL
6. Copy the Client ID and Client Secret to your `.env` file

### 4. Run the Application

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication
- `GET /api/v1/auth/google/login` - Initiate Google OAuth2 login
- `GET /api/v1/auth/google/callback` - Handle Google OAuth2 callback
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile
- `GET /api/v1/users/preferences` - Get user preferences
- `PUT /api/v1/users/preferences` - Update user preferences

### ML Recommendations
- `GET /api/v1/ml/recommendations` - Get learning resource recommendations
- `GET /api/v1/ml/recommendations/by-type` - Get recommendations by resource type
- `GET /api/v1/ml/resource-types` - Get available resource types
- `POST /api/v1/ml/recommendations` - Get recommendations (POST method)

### System
- `GET /api/v1/system/health` - Basic health check
- `GET /api/v1/system/status` - Detailed system status
- `GET /api/v1/system/metrics` - System metrics

## Testing

Run the ML tests:

```bash
# Run all tests
pytest app/ml/tests/

# Run specific test file
pytest app/ml/tests/test_recommender.py

# Run with verbose output
pytest app/ml/tests/test_recommender.py -v
```

## ML System

The ML system uses:

- **TF-IDF Vectorization**: For text preprocessing
- **Cosine Similarity**: For recommendation scoring
- **scikit-learn**: For ML operations
- **pandas**: For data handling

### Adding New Resources

To add new learning resources, update the `app/ml/data/resources.csv` file with:

```csv
id,title,type,description,url
11,"New Course Title","course","Course description","https://example.com/course"
```

The system will automatically retrain when new data is added.

## Deployment

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Create `vercel.json` configuration:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

3. Deploy:
```bash
vercel --prod
```

## Development Notes

- The system is designed to be flexible and easily extensible
- Database operations use raw SQL for better control
- ML models are automatically saved and loaded
- Error handling is comprehensive with proper logging
- CORS is configured for frontend integration

## Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass before submitting

## License

This project is part of the Clario learning platform.
