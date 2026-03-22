# Wasafi Beauty Salon — Online Appointment Booking System

A full-featured Django web application for **Wasafi Beauty Salon** in Bomet Town, Kenya.
Built with Django, Bootstrap 5, and PostgreSQL.

---

## 📁 Project Structure

```
wasafi_salon/
├── manage.py
├── requirements.txt
├── README.md
├── wasafi_salon/          # Project config (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── appointments/          # Main app
    ├── models.py           # Service, Appointment, Stylist, etc.
    ├── views.py            # All page views
    ├── forms.py            # Registration, booking, profile forms
    ├── urls.py             # URL routing
    ├── admin.py            # Admin panel config
    ├── mpesa.py           # mpesa payment
    ├── fixtures/
    
    │   └── initial_data.json   # Sample services & testimonials
    └── templates/appointments/
        ├── base.html
        ├── home.html
        ├── services.html
        ├── book_appointment.html
        ├── dashboard.html
        ├── login.html
        ├── register.html
        ├── about.html
        ├── contact.html
        ├── gallery.html
        └── profile.html
```

---

## 🚀 Quick Setup (SQLite — for development)

### 1. Clone / extract the project
```bash
cd wasafi_salon
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Load sample data (services, testimonials)
```bash
python manage.py loaddata appointments/fixtures/initial_data.json
```

### 6. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

Visit → **http://127.0.0.1:8000**  
Admin panel → **http://127.0.0.1:8000/admin**

---

## 🐘 Switching to PostgreSQL

1. Create the database:
```sql
CREATE DATABASE wasafi_salon_db;
CREATE USER wasafi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE wasafi_salon_db TO wasafi_user;
```

2. In `wasafi_salon/settings.py`, uncomment the PostgreSQL block and fill in your credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wasafi_salon_db',
        'USER': 'wasafi_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Run migrations again:
```bash
python manage.py migrate
python manage.py loaddata appointments/fixtures/initial_data.json
```

---

## 🌐 Features

| Feature | Description |
|---|---|
| 🏠 Home Page | Hero, services preview, how-it-works, team, testimonials |
| 💅 Services | Browse & filter services by category |
| 📅 Online Booking | Date/time slot selection, stylist choice, M-Pesa payment |
| 👤 Customer Portal | Dashboard with appointment history & stats |
| 🔐 Auth | Register, login, logout with profile management |
| 🖼️ Gallery | Photo gallery of salon work |
| ℹ️ About | Story, values, team profiles |
| 📞 Contact | Contact form with salon info |
| 🛠️ Admin Panel | Full management of services, appointments, stylists |

---

## 🛠️ Admin Panel Usage

Log into `/admin` to:
- Add/edit/delete **Services** (with categories, prices, duration)
- Manage **Stylists** and their specializations
- View and update **Appointments** (confirm, mark complete, mark paid)
- Upload **Gallery** images
- Add **Testimonials** and feature them on homepage
- Manage **Customer Profiles**

---

## 🔧 Technologies Used

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Django 4.2 |
| Frontend | HTML5, Bootstrap 5.3, Bootstrap Icons |
| Fonts | Google Fonts (Cormorant Garamond + DM Sans) |
| Database | SQLite (dev) / PostgreSQL (production) |
| Payments | M-Pesa (integrate via Daraja API) |
| Notifications | Django messages + Email backend |

---

## 📱 Responsive Design

The site is fully responsive on:
- 📱 Mobile (xs, sm)
- 📟 Tablet (md)
- 💻 Desktop (lg, xl)

---

## 📌 Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure email backend (SMTP)
- [ ] Integrate Daraja M-Pesa API for real payments
- [ ] Serve static files via WhiteNoise or Nginx
- [ ] Set up SSL certificate (HTTPS)

---

*Developed for Wasafi Beauty Salon, Bomet Town, Kenya.*
