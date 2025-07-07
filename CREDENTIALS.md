# ShikshaSetu - Default Credentials

## 🔑 Admin Credentials

```
Email: admin@shikshasetu.com
Password: admin123
Role: admin
After Login: Redirected to /admin
```

## 👤 Test User Credentials

```
Email: test@shikshasetu.com
Password: test123
Role: student
After Login: Redirected to /dashboard
```

## 🌐 Access URLs

### Frontend

- **Homepage**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3000/admin
- **Student Dashboard**: http://localhost:3000/dashboard
- **Test Auth Page**: http://localhost:3000/test-auth
- **Sign In**: http://localhost:3000/auth/signin
- **Scraping Jobs**: http://localhost:3000/admin/scraping-jobs
- **Test Scraping**: http://localhost:3000/test-scraping

### Backend API

- **API Base**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Endpoints**: http://localhost:8000/api/admin/\*

## 📝 Notes

- **Authentication**: NextAuth.js with JWT tokens enabled
- **Role-Based Access**: Admin/Student roles with automatic redirection
- **Protected Routes**: Admin routes require admin role
- **Quick Testing**: Use `/test-auth` for one-click login

## 🔧 How to Create Admin User

If you need to create the admin user in the database, run:

```bash
cd backend
python create_admin_user.py
```

This will create both admin and test users with the credentials above.

## 🚨 Security Note

**Important**: These are development credentials only.
In production:

- Use strong, unique passwords
- Enable proper JWT authentication
- Use environment variables for secrets
- Implement rate limiting and security measures
