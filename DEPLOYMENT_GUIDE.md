# EduManager - Production Deployment Guide

## Railway Deployment Instructions

### Step 1: Prepare Repository
✅ Production settings configured
✅ Requirements.txt updated
✅ Procfile created
✅ Runtime.txt specified

### Step 2: Deploy on Railway

1. **Go to Railway.app**
   - Visit: https://railway.app
   - Sign up with GitHub account

2. **Connect Repository**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `Prabigyakafle890/StudentManagementSystem`

3. **Environment Variables**
   Set these in Railway dashboard:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ```

4. **Deploy**
   - Railway will automatically deploy
   - Wait 3-5 minutes for build

### Step 3: Access Your Live Website
- Railway will provide a URL like: `https://your-app-name.railway.app`
- Your EduManager will be live!

### Login Credentials for Live Site:
- **Admin**: admin / admin123
- **Teacher**: ram_math / teacher123 (Ram Bahadur Sharma)
- **Student**: priya_001 / student123 (Priya Shrestha)

### Features Available:
✅ Nepali names for all users
✅ Nepali grading system (A+, A, B+, B, C+, C, D+, D, E)
✅ Course management
✅ Student enrollment
✅ Grade entry and GPA calculation
✅ Attendance tracking
✅ Teacher and student dashboards
✅ Premium UI with animations

### Post-Deployment:
1. Test all functionality
2. Add custom domain (optional)
3. Monitor performance

Your EduManager is ready to go live! 🚀