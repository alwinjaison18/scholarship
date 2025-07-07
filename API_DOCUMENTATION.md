# ShikshaSetu API Documentation

## Overview

ShikshaSetu provides a comprehensive REST API for scholarship management, built with FastAPI and PostgreSQL.

**Base URL**: `http://localhost:8000/api`

## Authentication

Most endpoints require authentication. Use JWT tokens obtained from the auth endpoints.

```bash
# Include in request headers
Authorization: Bearer <jwt_token>
```

## Endpoints

### Public Endpoints

#### GET /scholarships
Get list of scholarships with filtering and pagination.

**Query Parameters:**
- `category` (optional): Filter by category
- `search` (optional): Search in title/description
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Results offset (default: 0)
- `sort` (optional): Sort order (latest, deadline, amount)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Merit Scholarship 2024",
      "description": "Scholarship for meritorious students",
      "amount": 50000,
      "category": "Merit Based",
      "provider": "Government of India",
      "deadline": "2024-12-31",
      "eligibility": "12th pass with 80% marks",
      "verified": true,
      "trending": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20
}
```

#### GET /scholarships/trending
Get trending scholarships.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "National Merit Scholarship",
      "amount": 100000,
      "category": "Merit Based",
      "applications": 2500,
      "trending_score": 95
    }
  ]
}
```

#### GET /scholarships/{id}
Get specific scholarship details.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Merit Scholarship 2024",
    "description": "Detailed scholarship description...",
    "amount": 50000,
    "category": "Merit Based",
    "provider": "Government of India",
    "deadline": "2024-12-31",
    "eligibility": "12th pass with 80% marks",
    "application_process": "Online application through portal",
    "required_documents": ["Mark sheet", "Income certificate"],
    "verified": true,
    "source_url": "https://example.gov.in/scholarship"
  }
}
```

### Admin Endpoints (Protected)

#### GET /admin/stats
Get system statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_scholarships": 2500,
    "active_scholarships": 1800,
    "total_applications": 50000,
    "success_rate": 85.5,
    "scraping_jobs": {
      "total": 150,
      "successful": 142,
      "failed": 8
    }
  }
}
```

#### GET /admin/health
Get system health status.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "redis": "connected",
    "scraping_service": "operational",
    "last_scrape": "2024-01-15T10:30:00Z"
  }
}
```

#### GET /admin/scraping-jobs
Get scraping jobs status.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "job_123",
      "source": "scholarship.gov.in",
      "status": "completed",
      "started_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T10:30:00Z",
      "scholarships_found": 25,
      "errors": []
    }
  ]
}
```

#### POST /admin/scraping/trigger
Trigger manual scraping job.

**Request:**
```json
{
  "source": "scholarship.gov.in",
  "force": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "job_id": "job_456",
    "message": "Scraping job started successfully"
  }
}
```

### Dynamic Discovery Endpoints

#### POST /admin/discovery/trigger
Trigger dynamic discovery of new scholarship sources.

**Request:**
```json
{
  "search_terms": ["scholarship", "student aid", "education grant"],
  "max_sources": 10
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "discovery_job_id": "discovery_789",
    "message": "Discovery job started successfully"
  }
}
```

#### GET /admin/discovery/status/{job_id}
Check discovery job status.

**Response:**
```json
{
  "success": true,
  "data": {
    "job_id": "discovery_789",
    "status": "in_progress",
    "sources_found": 5,
    "sources_validated": 3,
    "estimated_completion": "2024-01-15T11:00:00Z"
  }
}
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "category",
      "reason": "Invalid category value"
    }
  }
}
```

### Error Codes

- `VALIDATION_ERROR`: Invalid request parameters
- `NOT_FOUND`: Resource not found
- `UNAUTHORIZED`: Authentication required
- `FORBIDDEN`: Insufficient permissions
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

## Rate Limiting

API endpoints have rate limits:
- Public endpoints: 100 requests per minute
- Admin endpoints: 50 requests per minute
- Scraping endpoints: 10 requests per minute

## Data Models

### Scholarship
```typescript
interface Scholarship {
  id: number;
  title: string;
  description: string;
  amount: number;
  category: string;
  provider: string;
  deadline: string;
  eligibility: string;
  application_process?: string;
  required_documents?: string[];
  verified: boolean;
  trending: boolean;
  source_url?: string;
  created_at: string;
  updated_at: string;
}
```

### ScrapingJob
```typescript
interface ScrapingJob {
  id: string;
  source: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  scholarships_found: number;
  errors: string[];
  metadata: Record<string, any>;
}
```

## SDK Usage Examples

### JavaScript/TypeScript
```javascript
const api = {
  baseUrl: 'http://localhost:8000/api',
  
  async getScholarships(params = {}) {
    const query = new URLSearchParams(params);
    const response = await fetch(`${this.baseUrl}/scholarships?${query}`);
    return response.json();
  },
  
  async getScholarship(id) {
    const response = await fetch(`${this.baseUrl}/scholarships/${id}`);
    return response.json();
  }
};

// Usage
const scholarships = await api.getScholarships({
  category: 'Merit Based',
  limit: 10
});
```

### Python
```python
import requests

class ScholarshipAPI:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_scholarships(self, **params):
        response = self.session.get(f"{self.base_url}/scholarships", params=params)
        return response.json()
    
    def get_scholarship(self, scholarship_id):
        response = self.session.get(f"{self.base_url}/scholarships/{scholarship_id}")
        return response.json()

# Usage
api = ScholarshipAPI()
scholarships = api.get_scholarships(category="Merit Based", limit=10)
```

## Testing

### Health Check
```bash
curl -X GET http://localhost:8000/health
```

### Get Scholarships
```bash
curl -X GET "http://localhost:8000/api/scholarships?category=Merit%20Based&limit=5"
```

### Trigger Scraping (Admin)
```bash
curl -X POST http://localhost:8000/api/admin/scraping/trigger \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"source": "scholarship.gov.in"}'
```

## Webhooks

The system supports webhooks for real-time notifications:

### Scholarship Updates
```json
{
  "event": "scholarship.created",
  "data": {
    "scholarship_id": 123,
    "title": "New Scholarship Available",
    "category": "Merit Based"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Scraping Events
```json
{
  "event": "scraping.completed",
  "data": {
    "job_id": "job_456",
    "source": "scholarship.gov.in",
    "scholarships_found": 25
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Support

For API support and questions:
- Documentation: http://localhost:8000/docs
- GitHub Issues: https://github.com/alwinjaison18/scholarship/issues
- Email: support@shiksha-setu.com
