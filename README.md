# ShikshaSetu - Indian Scholarship Portal

![ShikshaSetu Logo](public/logo.png)

**ShikshaSetu** is a comprehensive, production-grade Indian scholarship portal that scrapes live data from trusted sources and provides authentic scholarship opportunities to students. Built with modern, scalable technologies for reliability and performance.

## 🚀 Features

### Core Features

- **Real-time Scholarship Scraping**: Automatically scrapes and validates scholarships from trusted Indian sources
- **Link Validation & Quality Scoring**: Advanced validation system ensures authentic and working scholarship links
- **Smart Search & Filtering**: Powerful search with filters for category, amount, deadline, eligibility, and more
- **User Dashboard**: Personalized dashboard for applications, bookmarks, and notifications
- **Admin Panel**: Comprehensive admin interface for monitoring and management
- **Mobile-First Design**: Responsive design optimized for all devices
- **Accessibility**: WCAG 2.1 AA compliant for inclusive access

### Advanced Features

- **AI-Powered Recommendations**: Personalized scholarship suggestions based on user profile
- **Real-time Notifications**: Instant alerts for new scholarships and deadlines
- **Application Tracking**: Complete application lifecycle management
- **Analytics Dashboard**: Detailed insights and reporting
- **Background Processing**: Efficient task management with Celery
- **Caching & Performance**: Redis-based caching for optimal performance
- **Monitoring & Logging**: Comprehensive system monitoring with Prometheus and Grafana

## 🛠️ Technology Stack

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI components
- **React Query** - Data fetching and caching
- **NextAuth.js** - Authentication solution

### Backend

- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **PostgreSQL** - Robust relational database
- **Redis** - In-memory data store for caching
- **Celery** - Distributed task queue
- **Playwright** - Web scraping and automation

### AI & ML

- **LangChain** - AI/ML framework for data processing
- **OpenAI GPT** - AI-powered content extraction
- **Google Gemini** - Alternative AI model support

### DevOps & Deployment

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and load balancer
- **Prometheus** - Monitoring and alerting
- **Grafana** - Metrics visualization
- **GitHub Actions** - CI/CD pipeline

## 📋 Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.11 or higher
- **PostgreSQL** 15.x or higher
- **Redis** 7.x or higher
- **Docker** and **Docker Compose** (optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shiksha-setu.git
cd shiksha-setu
```

### 2. Environment Setup

```bash
# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
# Set DATABASE_URL, REDIS_URL, and other required variables
```

### 3. Database Setup

```bash
# Install Prisma CLI
npm install -g prisma

# Generate Prisma client
npx prisma generate

# Run database migrations
npx prisma migrate dev --name init
```

### 4. Install Dependencies

#### Frontend

```bash
# Install Node.js dependencies
npm install
```

#### Backend

```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 5. Run the Application

#### Development Mode

```bash
# Start frontend (Terminal 1)
npm run dev

# Start backend (Terminal 2)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (Terminal 3)
cd backend
celery -A celery_app worker --loglevel=info

# Start Celery beat (Terminal 4)
cd backend
celery -A celery_app beat --loglevel=info
```

#### Production Mode with Docker

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables

| Variable          | Description                  | Default                                                      |
| ----------------- | ---------------------------- | ------------------------------------------------------------ |
| `DATABASE_URL`    | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/shiksha_setu` |
| `REDIS_URL`       | Redis connection string      | `redis://localhost:6379`                                     |
| `NEXTAUTH_SECRET` | NextAuth.js secret key       | Required                                                     |
| `NEXTAUTH_URL`    | Application URL              | `http://localhost:3000`                                      |
| `GEMINI_API_KEY`  | Google Gemini API key        | Optional                                                     |
| `OPENAI_API_KEY`  | OpenAI API key               | Optional                                                     |

### Database Configuration

The application uses PostgreSQL with Prisma ORM. The database schema includes:

- Users and authentication
- Scholarships and applications
- Notifications and analytics
- Scraping jobs and system logs

### Scraping Configuration

ShikshaSetu scrapes from trusted Indian scholarship sources:

- **NSP (National Scholarship Portal)**: scholarships.gov.in
- **UGC**: ugc.ac.in
- **AICTE**: aicte-india.org
- **Government Departments**: Various ministry websites
- **Educational Institutions**: IITs, IIMs, Central Universities

## 🔍 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Scholarship Endpoints

- `GET /api/scholarships` - Get scholarships with filters
- `GET /api/scholarships/:id` - Get scholarship details
- `POST /api/scholarships/:id/bookmark` - Bookmark scholarship
- `POST /api/scholarships/:id/apply` - Apply for scholarship

### Admin Endpoints

- `GET /api/admin/dashboard` - Admin dashboard data
- `GET /api/admin/scholarships` - Manage scholarships
- `GET /api/admin/users` - Manage users
- `POST /api/admin/scraping/start` - Start scraping job

## 🧪 Testing

### Frontend Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

### Backend Testing

```bash
# Run Python tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 📊 Monitoring & Analytics

### Prometheus Metrics

- Application performance metrics
- Database query performance
- Scraping job statistics
- User engagement metrics

### Grafana Dashboards

- System overview
- Application performance
- User analytics
- Scholarship statistics

### Logging

- Structured logging with JSON format
- Centralized log aggregation
- Error tracking and alerting

## 🔒 Security

### Authentication & Authorization

- JWT-based authentication
- Role-based access control (RBAC)
- OAuth integration (Google, GitHub)
- Session management

### Data Protection

- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting

### Infrastructure Security

- HTTPS enforcement
- Security headers
- Environment variable protection
- Regular security updates

## 🚀 Deployment

### Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale celery-worker=3
```

### Cloud Deployment

- **AWS**: ECS, RDS, ElastiCache
- **Google Cloud**: Cloud Run, Cloud SQL, Memorystore
- **Azure**: Container Instances, PostgreSQL, Redis Cache

### CI/CD Pipeline

- Automated testing on pull requests
- Build and deploy on merge to main
- Environment-specific deployments
- Rollback capabilities

## 📈 Performance Optimization

### Caching Strategy

- Redis caching for frequently accessed data
- Database query optimization
- Static asset caching
- CDN integration

### Database Optimization

- Proper indexing strategy
- Query optimization
- Connection pooling
- Read replicas for scaling

### Frontend Optimization

- Code splitting and lazy loading
- Image optimization
- Bundle size optimization
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow TypeScript and Python coding standards
- Write tests for new features
- Update documentation
- Follow semantic versioning

## 📞 Support

- **Documentation**: [https://docs.shiksha-setu.com](https://docs.shiksha-setu.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/shiksha-setu/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shiksha-setu/discussions)
- **Email**: support@shiksha-setu.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **National Scholarship Portal** for providing scholarship data
- **Open source community** for amazing tools and libraries
- **Contributors** who help make this project better

---

**ShikshaSetu** - Empowering students with authentic scholarship opportunities 🎓✨
