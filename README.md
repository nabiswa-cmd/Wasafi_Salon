# Wasafi Beauty Salon(Online Appointment Booking System)

A full-featured Django web application for **Wasafi Beauty Salon** in Bomet Town, Kenya.
Built with Django, Bootstrap 5, and PostgreSQL.

---

## 📁 Project Structure)

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
python manage.py runserver
```

Visit → **http://127.0.0.1:8000**  
Admin panel → **http://127.0.0.1:8000/admin**

---


### 4. Run migrations again:
```bash
python manage.py migrate
python manage.py loaddata appointments/fixtures/initial_data.json
```

---

##  Features

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
| Google Auth | continue with google Email backend |
---
visit the site https://wasafi-salon.vercel.app/ 
