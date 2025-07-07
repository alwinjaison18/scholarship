# Admin Panel & Scraping Monitoring System

## Overview

I've implemented a comprehensive admin panel and scraping monitoring system for ShikshaSetu. This system allows administrators to monitor scraping operations, view system health, and manage scholarship data in real-time.

## Backend Components

### 1. Admin API Routes (`/app/api/admin/admin_routes.py`)

**Main Endpoints:**

- `GET /api/admin/dashboard/stats` - System statistics dashboard
- `GET /api/admin/scraping-jobs` - List and filter scraping jobs
- `POST /api/admin/scraping-jobs/start` - Start new scraping jobs
- `POST /api/admin/scraping-jobs/{id}/cancel` - Cancel running jobs
- `POST /api/admin/scraping-jobs/{id}/retry` - Retry failed jobs
- `GET /api/admin/system-health` - System health metrics
- `GET /api/admin/sources` - Available scraping sources
- `GET /api/admin/logs` - System logs

### 2. Monitoring Service (`/app/services/monitoring_service.py`)

**Features:**

- Database health checks
- Celery/Redis connectivity monitoring
- Resource usage tracking (CPU, Memory, Disk)
- Scraping job performance metrics
- Success rate calculations
- Stuck job detection

### 3. Authentication & Authorization (`/app/core/auth.py`)

**Security Features:**

- JWT token validation
- Admin role verification
- User session management
- Role-based access control

### 4. Enhanced Database Models

**ScrapingJob Model includes:**

- Job status tracking (pending, running, completed, failed)
- Performance metrics (items scraped, saved, rejected)
- Error and warning logs
- Retry logic and scheduling
- Resource usage tracking

## Frontend Components

### 1. Admin Dashboard (`/admin/page.tsx`)

**Features:**

- Real-time system status indicators
- Key performance metrics
- Resource usage monitoring
- Quick action buttons
- Health status visualization

**Metrics Displayed:**

- Total scholarships (active, verified)
- Total users
- Jobs today (running, failed)
- Success rate
- System resource usage

### 2. Scraping Jobs Management (`/admin/scraping-jobs/page.tsx`)

**Features:**

- Job listing with filters (status, source, date range)
- Real-time status updates
- Job control actions (start, cancel, retry)
- Performance metrics per job
- Error log viewing
- Quick start buttons for different sources

### 3. Test Scraping Interface (`/test-scraping/page.tsx`)

**Features:**

- Simple testing interface for scraping functions
- Real-time job status monitoring
- Error handling and display
- Job history tracking

## How to Monitor Scraping Operations

### 1. **System Health Monitoring**

Access the admin dashboard at `/admin` to view:

- Overall system status (healthy/warning/unhealthy)
- Database connectivity and response times
- Celery worker status and queue sizes
- System resource usage (CPU, Memory, Disk)

### 2. **Scraping Job Monitoring**

Visit `/admin/scraping-jobs` to:

- View all scraping jobs with real-time status
- Filter jobs by status, source, or date range
- See detailed metrics for each job
- Monitor progress and performance
- View error logs and warnings

### 3. **Starting New Scraping Jobs**

You can start scraping jobs in several ways:

**Through Admin Panel:**

- Use quick start buttons for NSP, UGC, AICTE
- Configure job parameters and priority
- Set force update options

**Through API:**

```bash
curl -X POST "http://localhost:8000/api/admin/scraping-jobs/start" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_url": "https://scholarships.gov.in/",
    "source_name": "NSP",
    "force_update": false,
    "priority": "high"
  }'
```

**Through Test Interface:**

- Visit `/test-scraping` for simple testing
- Click source buttons to start test jobs
- Monitor results in real-time

### 4. **Job Status Meanings**

- **Pending**: Job created but not yet started
- **Running**: Job is currently executing
- **Completed**: Job finished successfully
- **Failed**: Job encountered errors and stopped
- **Cancelled**: Job was manually cancelled

### 5. **Performance Metrics**

Each job tracks:

- **Items Scraped**: Total URLs/pages processed
- **Items Validated**: Successfully validated scholarships
- **Items Saved**: New scholarships added to database
- **Items Rejected**: Invalid or duplicate scholarships
- **Duration**: Total job execution time
- **Success Rate**: Percentage of successful operations

### 6. **Error Handling**

The system provides:

- Detailed error logs for each job
- Automatic retry logic for failed jobs
- Stuck job detection (jobs running > 2 hours)
- Resource monitoring to prevent system overload

## API Authentication

To access admin endpoints, you need:

1. **Admin Role**: User must have `role: "admin"`
2. **Valid JWT Token**: Include in Authorization header
3. **Active Session**: User must be active and verified

Example request:

```javascript
const response = await fetch("/api/admin/dashboard/stats", {
  headers: {
    Authorization: `Bearer ${adminToken}`,
    "Content-Type": "application/json",
  },
});
```

## System Requirements

### Backend Dependencies

- FastAPI for API framework
- Celery for background job processing
- Redis for job queue and caching
- PostgreSQL for data storage
- SQLAlchemy for ORM
- Playwright for web scraping

### Frontend Dependencies

- Next.js 14 with App Router
- React components with TypeScript
- Tailwind CSS for styling
- shadcn/ui component library

## Deployment Notes

1. **Environment Variables**: Set proper JWT secrets and database URLs
2. **Redis Setup**: Ensure Redis is running for Celery
3. **Background Workers**: Start Celery workers for job processing
4. **Admin User**: Create initial admin user in database
5. **Monitoring**: Set up log aggregation and alerting

## Usage Examples

### Start a Scraping Job

```typescript
const startJob = async () => {
  const response = await fetch("/api/admin/scraping-jobs/start", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      source_url: "https://scholarships.gov.in/",
      source_name: "NSP",
      force_update: false,
    }),
  });

  const result = await response.json();
  console.log("Job started:", result.job_id);
};
```

### Monitor Job Status

```typescript
const checkStatus = async (jobId: string) => {
  const response = await fetch(`/api/admin/scraping-jobs/${jobId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const job = await response.json();
  console.log("Job status:", job.status);
  console.log("Items processed:", job.items_scraped);
};
```

This comprehensive system provides full visibility into the scraping operations and allows for efficient monitoring and management of the scholarship data collection process.
