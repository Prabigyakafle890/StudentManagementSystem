# Student Management System (SMS)

A comprehensive Student Management System built with Django, Django REST Framework, and JWT authentication. This system allows admins, teachers, and students to manage academic data efficiently.

## 🚀 Features

- **User Authentication**: JWT-based authentication with role-based access control
- **Admin Dashboard**: Full control over students, teachers, courses, and academic records
- **Teacher Portal**: Manage courses, mark attendance, and assign grades
- **Student Portal**: View personal information, grades, and attendance records
- **REST API**: Complete API for all operations with proper permissions
- **Responsive UI**: Bootstrap-styled interface for all user types

## 🏗️ Architecture

### Models
- **Student**: Personal information and academic details
- **Teacher**: Teacher profiles and subject specializations
- **Course**: Course information with teacher assignments
- **Enrollment**: Student-course relationships
- **Attendance**: Daily attendance tracking
- **Grade**: Academic performance records

### User Roles
- **Admin**: Full system access and management
- **Teacher**: Course management, attendance, and grading
- **Student**: Read-only access to personal academic data

## 📚 Tech Stack

- **Backend**: Django 5.2.7, Django REST Framework 3.16.1
- **Authentication**: Django SimpleJWT 5.5.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates with Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0.0

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Clone and navigate to the project**:
   ```bash
   cd SMS
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Root: http://127.0.0.1:8000/api/

## 🔗 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Core Resources
- `GET/POST /api/students/` - List/Create students
- `GET/PUT/DELETE /api/students/{id}/` - Student detail operations
- `GET/POST /api/teachers/` - List/Create teachers
- `GET/PUT/DELETE /api/teachers/{id}/` - Teacher detail operations
- `GET/POST /api/courses/` - List/Create courses
- `GET /api/courses/{id}/students/` - Get students enrolled in course
- `GET/POST /api/enrollments/` - List/Create enrollments
- `GET/POST /api/attendance/` - List/Create attendance records
- `GET/POST /api/grades/` - List/Create grade records

## 🎯 Usage Examples

### Admin Tasks
1. **Login**: Use superuser credentials at `/login/`
2. **Add Teachers**: Navigate to Admin Panel → Teachers
3. **Create Courses**: Admin Panel → Courses
4. **Enroll Students**: Admin Panel → Enrollments

### Teacher Tasks
1. **Mark Attendance**: Use API or admin interface
2. **Assign Grades**: Submit grades for enrolled students
3. **View Course Students**: Access enrolled student lists

### Student Access
1. **View Grades**: Personal grade reports
2. **Check Attendance**: Personal attendance history
3. **Course Information**: Enrolled course details

## 🔐 Security Features

- JWT token authentication
- Role-based permissions
- CSRF protection
- Secure password validation
- Input sanitization

## 📱 Frontend Features

- **Responsive Design**: Works on desktop and mobile
- **Role-based Dashboards**: Different interfaces for each user type
- **Interactive UI**: Bootstrap components with Font Awesome icons
- **Real-time Updates**: Dynamic content loading

## 🚀 Production Deployment

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/sms_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database Migration (PostgreSQL)
```bash
pip install psycopg2-binary
python manage.py migrate
```

## 🔧 Advanced Features (Optional)

- **Chart.js Integration**: Attendance and grade visualizations
- **CSV/PDF Export**: Generate reports
- **Email Notifications**: Automated alerts for absences/grades
- **Search & Filtering**: Advanced data filtering
- **Pagination**: Large dataset handling

## 📄 Project Structure

```
SMS/
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API viewsets & template views
│   ├── serializers.py     # DRF serializers
│   ├── permissions.py     # Custom permissions
│   └── urls.py           # URL routing
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   └── core/             # App-specific templates
├── sms/                   # Project configuration
│   ├── settings.py       # Django settings
│   └── urls.py          # Root URL configuration
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check existing documentation
- Review API endpoints
- Test with different user roles
- Verify permissions are correctly configured

## 📃 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Django & Django REST Framework**