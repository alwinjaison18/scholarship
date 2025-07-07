# 🔐 Admin & User Credentials - Quick Reference

## 📍 **Where to Find Credentials**

The admin and test user credentials are documented in multiple files for easy access:

### **1. CREDENTIALS.md** (Main Reference)

- Quick access to all login credentials
- URLs for frontend and backend
- Development notes

### **2. AUTH_GUIDE.md** (Detailed Guide)

- Complete authentication setup guide
- Step-by-step instructions
- Production security notes

### **3. backend/create_admin_user.py** (Setup Script)

- Python script to create users in database
- Automatically sets up credentials
- Prints credentials when script runs

### **4. backend/.env.example** (Environment Template)

- Environment variable configuration
- Admin credentials in ADMIN_EMAIL/ADMIN_PASSWORD

## 🔑 **Current Credentials**

### **Admin User**

```
Email: admin@shikshasetu.com
Password: admin123
Role: admin
Access: Full admin panel access
```

### **Test User**

```
Email: test@shikshasetu.com
Password: test123
Role: student
Access: Student features only
```

## 🌐 **Access Methods**

### **Development Mode (Current)**

- **No login required** - Direct URL access
- Admin panel: `http://localhost:3000/admin`
- All features accessible without authentication

### **When Authentication is Enabled**

- Use the credentials above to log in
- JWT tokens will be required for API access
- Role-based access control will be enforced

## 🛠️ **Setup Instructions**

### **1. Create Users in Database**

```bash
cd backend
python create_admin_user.py
```

### **2. Start Development Servers**

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd ..
npm run dev
```

### **3. Access Admin Panel**

- Go to: `http://localhost:3000/admin`
- Click on admin tools cards to access features

## 📝 **Files with Credentials Info**

1. **`/CREDENTIALS.md`** - Quick reference (this file)
2. **`/AUTH_GUIDE.md`** - Complete authentication guide
3. **`/backend/create_admin_user.py`** - User creation script
4. **`/backend/.env.example`** - Environment template
5. **`/ADMIN_PANEL_GUIDE.md`** - Admin panel usage guide

## 🚨 **Security Notes**

- **Development Only**: These are development credentials
- **Production**: Use strong, unique passwords in production
- **Environment Variables**: Store secrets in environment variables
- **JWT Secrets**: Change JWT_SECRET in production
- **Database**: Secure database with proper authentication

## 🎯 **Quick Start**

1. **Clone/Download** the project
2. **Run** `python backend/create_admin_user.py` to set up users
3. **Start** both backend and frontend servers
4. **Access** admin panel at `http://localhost:3000/admin`
5. **Use** the credentials above when authentication is enabled

---

**Need Help?** Check the AUTH_GUIDE.md for detailed setup instructions!
