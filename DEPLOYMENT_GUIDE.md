# ShikshaSetu Deployment Guide

## Quick Start for Development

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- PostgreSQL 14+
- Redis (for background jobs)

### 1. Frontend Development

```bash
# Navigate to project directory
cd "C:\Users\Alwin Jaison\Desktop\scholarship"

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 2. Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### 3. Database Setup

```bash
# Generate Prisma client
npm run db:generate

# Push database schema
npm run db:push

# Seed database (optional)
npm run db:seed
```

### 4. Background Workers (Optional)

```bash
# Start Celery worker
cd backend
celery -A celery_app worker --loglevel=info

# Start Celery beat (scheduler)
celery -A celery_app beat --loglevel=info
```

## Production Deployment

### Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop all services
docker-compose down
```

### Environment Variables

Create `.env` files with the following variables:

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/scholarship
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
DEBUG=False
CORS_ORIGINS=http://localhost:3000
```

## API Documentation

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:3000/admin

## Monitoring & Maintenance

### Health Checks
- Frontend: `http://localhost:3000/api/health`
- Backend: `http://localhost:8000/health`

### Logs
- Frontend: Browser console and Next.js logs
- Backend: FastAPI logs and Celery worker logs
- Database: PostgreSQL logs

### Backup
- Database: Regular PostgreSQL backups
- Redis: Periodic Redis snapshots
- Files: Application logs and uploads

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   ```

2. **Database connection issues**
   - Check PostgreSQL service is running
   - Verify database credentials
   - Check firewall settings

3. **Redis connection issues**
   - Ensure Redis service is running
   - Check Redis configuration
   - Verify Redis URL

### Performance Optimization

1. **Database**
   - Add indexes for frequently queried fields
   - Use connection pooling
   - Regular maintenance and cleanup

2. **Frontend**
   - Enable Next.js static generation
   - Implement proper caching strategies
   - Optimize images and assets

3. **Backend**
   - Use async/await for I/O operations
   - Implement proper caching
   - Monitor and optimize slow queries

## Security Considerations

1. **Authentication**
   - Use strong JWT secrets
   - Implement proper session management
   - Add rate limiting

2. **Data Protection**
   - Encrypt sensitive data
   - Use HTTPS in production
   - Regular security audits

3. **API Security**
   - Implement proper CORS settings
   - Add request validation
   - Monitor for suspicious activity

## Support

For issues and support:
- Check GitHub Issues: https://github.com/alwinjaison18/scholarship/issues
- Review documentation
- Check logs for error messages
