# ShikshaSetu Authentication Guide

## 🔐 Authentication Status

Currently, the ShikshaSetu platform is in **development mode** with simplified authentication.

## 🚀 Development Access

### Frontend Access

- **URL**: `http://localhost:3000`
- **Admin Panel**: `http://localhost:3000/admin`
- **Scraping Jobs**: `http://localhost:3000/admin/scraping-jobs`
- **Test Scraping**: `http://localhost:3000/test-scraping`

### Backend API Access

- **URL**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Admin API**: `http://localhost:8000/api/admin/*`

## 🔑 Authentication Credentials

### Current Setup

- **Authentication**: NextAuth.js with JWT tokens
- **Admin Access**: Role-based access control enabled
- **API Protection**: Admin endpoints require authentication
- **Auto-Redirect**: Users redirected based on role after login

### Default Admin Credentials

```
Email: admin@shikshasetu.com
Password: admin123
Role: admin
Redirect: /admin (Admin Dashboard)
```

### Default Test User Credentials

```
Email: test@shikshasetu.com
Password: test123
Role: student
Redirect: /dashboard (Student Dashboard)
```

## 🚀 **New Authentication Flow**

### **1. Role-Based Redirection**

- **Admin users** → Automatically redirected to `/admin`
- **Student users** → Automatically redirected to `/dashboard`
- **Unauthorized access** → Redirected to signin with callback URL

### **2. Quick Test Authentication**

- **Test Auth Page**: `http://localhost:3000/test-auth`
- **One-click login** for both admin and student roles
- **Automatic redirection** to appropriate dashboard

### **3. Protected Routes**

- **Admin routes** (`/admin/*`, `/test-scraping`) → Admin role required
- **Student routes** (`/dashboard/*`) → Any authenticated user
- **Public routes** → No authentication required

## 🛠️ How to Enable Full Authentication

### 1. Backend Authentication

To enable JWT-based authentication:

1. **Set Environment Variables**:

   ```bash
   JWT_SECRET=your-super-secret-jwt-key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

2. **Create Admin User** (Run this script):

   ```python
   from app.core.auth import AuthService
   from app.models.models import User
   from app.core.database import get_db

   # Create admin user
   admin_user = User(
       email="admin@shikshasetu.com",
       password_hash=AuthService.get_password_hash("admin123"),
       name="Admin User",
       role="admin",
       is_active=True,
       is_verified=True
   )
   ```

3. **Enable Authentication Middleware**:
   - Uncomment authentication dependencies in `main.py`
   - Enable `get_current_admin` in admin routes

### 2. Frontend Authentication

To enable NextAuth.js authentication:

1. **Install NextAuth.js**:

   ```bash
   npm install next-auth
   ```

2. **Configure NextAuth** in `src/app/api/auth/[...nextauth]/route.ts`

3. **Update Navigation** to use real authentication

## 🔧 Current Navigation Features

### ✅ Working Features

- **Clean Navigation**: Simplified, responsive navbar
- **Admin Links**: Direct access to admin panels
- **Mobile Support**: Responsive design for all devices
- **Visual Indicators**: Different colors for admin sections

### 🎯 Admin Panel Access

1. **Direct URLs**: Navigate directly to admin URLs
2. **Navigation Menu**: Use the admin links in the navbar
3. **Homepage Buttons**: Use the development access buttons

### 🔄 Development Mode Benefits

- **No Login Required**: Direct access to all features
- **Mock Data**: Pre-populated with test data
- **Instant Testing**: Test all features immediately
- **Real-time Development**: See changes instantly

## 🚨 Security Note

**Important**: This is a development setup. In production:

- Enable proper JWT authentication
- Use strong passwords and secrets
- Implement rate limiting
- Add CORS restrictions
- Enable HTTPS
- Use environment variables for secrets

## 📝 Next Steps

1. **Test Admin Panel**: Access all admin features
2. **Review Mock Data**: Understand the data structure
3. **API Integration**: Connect frontend to backend APIs
4. **Authentication**: Implement full authentication when ready
5. **Database Setup**: Configure PostgreSQL for production

## 🆘 Troubleshooting

### Navigation Issues

- **Refresh Page**: Clear browser cache
- **Check Console**: Look for JavaScript errors
- **Verify URLs**: Ensure correct port numbers

### API Connection Issues

- **Backend Running**: Ensure FastAPI server is running
- **CORS Settings**: Check CORS configuration
- **Network**: Verify localhost connectivity

### Database Issues

- **Connection**: Check database connection strings
- **Models**: Verify database models are created
- **Seeds**: Run database seeds if needed
