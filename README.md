# 📦 CourierTrack — Full-Stack Courier Tracking System

A professional, production-ready courier tracking system built with **Python Flask**, **SQLite**, and a modern dark-themed frontend.

---

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

The app will start at: **http://127.0.0.1:5000**

---

## 🔐 Default Login Credentials

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

> Change these in `database.py` → `init_db()` before deploying.

---

## 🗺️ Application URLs

| URL                  | Description                        |
|----------------------|------------------------------------|
| `/`                  | Redirects to public tracking page  |
| `/track`             | **Public** — Track a shipment      |
| `/login`             | Admin login                        |
| `/dashboard`         | Admin dashboard with stats/charts  |
| `/add-shipment`      | Create a new shipment              |
| `/manage-shipments`  | View, filter, update, delete       |
| `/update-status/<id>`| Update status + add location notes |
| `/api/track/<id>`    | JSON API for tracking data         |

---

## 📁 Project Structure

```
courier_tracker/
├── app.py              # Main Flask application + all routes
├── database.py         # SQLite DB setup, schema, seed data
├── requirements.txt    # Python dependencies
├── courier.db          # SQLite database (auto-created on first run)
│
├── templates/
│   ├── base.html           # Base layout with sidebar
│   ├── login.html          # Admin login page
│   ├── dashboard.html      # Stats dashboard + chart
│   ├── add_shipment.html   # New shipment form
│   ├── manage_shipments.html  # Table with search/filter/actions
│   ├── update_status.html  # Status update + timeline
│   └── track.html          # Public tracking page
│
└── static/
    ├── css/
    │   └── style.css       # Full stylesheet (~600 lines)
    └── js/
        └── main.js         # Sidebar toggle, clock, flash auto-dismiss
```

---

## 🎯 Demo Tracking IDs

The database is pre-seeded with 5 sample shipments:

| Tracking ID   | Status            | Route                        |
|---------------|-------------------|------------------------------|
| TRK001DEMO    | Delivered         | New York → Los Angeles       |
| TRK002DEMO    | In Transit        | Chicago → Houston            |
| TRK003DEMO    | Pending           | Miami → Seattle              |
| TRK004DEMO    | Shipped           | Boston → Phoenix             |
| TRK005DEMO    | Out for Delivery  | Denver → Atlanta             |

---

## ✨ Features

- **Auto-generated Tracking IDs** (e.g. `TRK3F8A2C1D`)
- **Real-time status timeline** with location and notes
- **Shipment progress bar** showing delivery stages
- **Delayed shipment detection** (>5 days in transit)
- **Status donut chart** on dashboard
- **Search & filter** by ID, name, or status
- **Responsive sidebar layout** with mobile support
- **Flash messages** with auto-dismiss
- **JSON API** endpoint for external integrations
- **Session-based admin authentication**

---

## 🛡️ Security Notes

For production use:
1. Set a strong `app.secret_key` (not `os.urandom(24)` which changes on restart)
2. Use a proper password hashing library like `bcrypt`
3. Add CSRF protection (e.g. `flask-wtf`)
4. Use HTTPS

---

## 🔧 Customization

### Change admin password
Edit `database.py`, find:
```python
default_pw = hashlib.sha256('admin123'.encode()).hexdigest()
cursor.execute('INSERT OR IGNORE INTO admins ...', ('admin', default_pw))
```
Change `'admin123'` to your desired password, then delete `courier.db` and restart.

### Add more status types
Edit the status lists in `app.py`, `templates/update_status.html`, and `templates/manage_shipments.html`.
