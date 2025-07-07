# Manual Setup Instructions for ShikshaSetu

## Prerequisites

1. **Python 3.11+** - Download from [python.org](https://python.org)
2. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org)
3. **Docker Desktop** - Download from [docker.com](https://docker.com)
4. **Git** - Download from [git-scm.com](https://git-scm.com)

## Quick Start (Windows)

### Option 1: Automated Setup

```bash
# Run the startup script
./start-project.bat
```

### Option 2: Manual Setup

#### 1. Start Database Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis
```

#### 2. Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Start the backend server
python main.py
```

#### 3. Setup Frontend (New Terminal)

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## Testing the Scraping System

1. **Visit Test Page**: http://localhost:3000/test-scraping
2. **Click on scraping buttons** to test NSP, UGC, AICTE scraping
3. **Monitor job status** in real-time
4. **Check admin panel**: http://localhost:3000/admin (requires admin login)

## Admin Panel Access

To access the admin panel, you'll need to create an admin user:

1. **Register a normal user** at http://localhost:3000/auth/signup
2. **Update user role to admin** in the database:
   ```sql
   UPDATE users SET role = 'admin' WHERE email = 'your-email@example.com';
   ```
3. **Login and access**: http://localhost:3000/admin

## Database Access

- **Host**: localhost
- **Port**: 5432
- **Database**: shiksha_setu
- **Username**: postgres
- **Password**: password

Connect using any PostgreSQL client like pgAdmin, DBeaver, or CLI:

```bash
psql -h localhost -p 5432 -U postgres -d shiksha_setu
```

## Redis Access

- **Host**: localhost
- **Port**: 6379
- **No password required**

## Troubleshooting

### Backend Issues

1. **Port 8000 already in use**: Change PORT in backend/.env
2. **Database connection failed**: Ensure Docker is running and postgres service is up
3. **Module not found**: Ensure virtual environment is activated and dependencies installed

### Frontend Issues

1. **Port 3000 already in use**: Use `npm run dev -- --port 3001`
2. **API connection failed**: Ensure backend is running on port 8000
3. **Build errors**: Delete node_modules and run `npm install` again

### Docker Issues

1. **Docker daemon not running**: Start Docker Desktop
2. **Port conflicts**: Check if ports 5432/6379 are already in use
3. **Permission errors**: Run as administrator on Windows

### Database Issues

1. **Connection refused**: Wait for postgres service to fully start (30 seconds)
2. **Authentication failed**: Check username/password in .env files
3. **Database doesn't exist**: It will be created automatically on first connection

## Development Workflow

1. **Make backend changes**: Server auto-reloads (if using uvicorn with --reload)
2. **Make frontend changes**: Next.js auto-reloads in development
3. **Database changes**: Use Alembic migrations in backend
4. **New dependencies**: Add to requirements.txt (backend) or package.json (frontend)

## Production Deployment

For production deployment:

1. **Update environment variables** in .env files
2. **Build frontend**: `npm run build`
3. **Use production WSGI server**: Gunicorn instead of uvicorn
4. **Enable Docker Compose**: `docker-compose up -d` for all services
5. **Setup reverse proxy**: Nginx for frontend/backend routing
6. **Enable HTTPS**: SSL certificates for secure connections

## Monitoring

- **System Health**: http://localhost:8000/health
- **Admin Dashboard**: http://localhost:3000/admin
- **Job Monitoring**: http://localhost:3000/admin/scraping-jobs
- **API Metrics**: http://localhost:8000/docs

## Support

If you encounter issues:

1. Check the console/terminal for error messages
2. Review the logs in backend/logs/ directory
3. Ensure all prerequisites are properly installed
4. Verify environment variables are correctly set
