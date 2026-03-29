"""
Database module - SQLite setup and connection helper
"""

import sqlite3
import hashlib
from flask import g
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'courier.db')

def get_db():
    """Get database connection; uses Flask's app context for connection reuse."""
    from app import app
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return dict-like rows
    return g.db

def init_db():
    """Initialize the database schema and seed default admin."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ── Admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # ── Shipments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id      TEXT UNIQUE NOT NULL,
            sender_name      TEXT NOT NULL,
            receiver_name    TEXT NOT NULL,
            origin           TEXT NOT NULL,
            destination      TEXT NOT NULL,
            sender_contact   TEXT,
            receiver_contact TEXT,
            weight           TEXT,
            description      TEXT,
            status           TEXT DEFAULT 'Pending',
            created_at       TEXT DEFAULT (datetime('now'))
        )
    ''')

    # ── Tracking history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id INTEGER NOT NULL,
            status      TEXT NOT NULL,
            location    TEXT,
            notes       TEXT,
            timestamp   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (shipment_id) REFERENCES shipments(id)
        )
    ''')

    # ── Seed default admin account (admin / admin123)
    default_pw = hashlib.sha256('admin123'.encode()).hexdigest()
    cursor.execute(
        'INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)',
        ('admin', default_pw)
    )

    # ── Seed sample shipments for demo purposes
    sample_shipments = [
        ('TRK001DEMO', 'Alice Johnson', 'Bob Smith', 'New York, NY', 'Los Angeles, CA',
         '+1-555-0101', '+1-555-0202', '2.5 kg', 'Electronics', 'Delivered'),
        ('TRK002DEMO', 'Carol White', 'Dave Brown', 'Chicago, IL', 'Houston, TX',
         '+1-555-0303', '+1-555-0404', '1.2 kg', 'Documents', 'In Transit'),
        ('TRK003DEMO', 'Eve Davis', 'Frank Miller', 'Miami, FL', 'Seattle, WA',
         '+1-555-0505', '+1-555-0606', '5.0 kg', 'Clothing', 'Pending'),
        ('TRK004DEMO', 'Grace Lee', 'Hank Wilson', 'Boston, MA', 'Phoenix, AZ',
         '+1-555-0707', '+1-555-0808', '0.8 kg', 'Books', 'Shipped'),
        ('TRK005DEMO', 'Ivy Clark', 'Jack Taylor', 'Denver, CO', 'Atlanta, GA',
         '+1-555-0909', '+1-555-1010', '3.3 kg', 'Medical Supplies', 'Out for Delivery'),
    ]

    for s in sample_shipments:
        # s indexes: 0=tracking_id,1=sender,2=receiver,3=origin,4=destination,5=s_contact,6=r_contact,7=weight,8=desc,9=status
        tracking_id, sender, receiver, origin, destination = s[0], s[1], s[2], s[3], s[4]
        status = s[9]
        cursor.execute('SELECT id FROM shipments WHERE tracking_id=?', (tracking_id,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO shipments
                (tracking_id, sender_name, receiver_name, origin, destination,
                 sender_contact, receiver_contact, weight, description, status, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,datetime('now','-'||(abs(random())%7)||' days'))
            ''', s)
            sid = cursor.lastrowid
            # Seed tracking history for sample shipments
            history_map = {
                'Pending': [
                    ('Pending', origin, 'Shipment registered')
                ],
                'Shipped': [
                    ('Pending', origin, 'Shipment registered'),
                    ('Shipped', origin, 'Package picked up by courier')
                ],
                'In Transit': [
                    ('Pending', origin, 'Shipment registered'),
                    ('Shipped', origin, 'Package picked up'),
                    ('In Transit', 'Kansas City, MO', 'Package in transit hub')
                ],
                'Out for Delivery': [
                    ('Pending', origin, 'Shipment registered'),
                    ('Shipped', origin, 'Package picked up'),
                    ('In Transit', 'Midway Hub', 'In transit'),
                    ('Out for Delivery', destination, 'Out for delivery today')
                ],
                'Delivered': [
                    ('Pending', origin, 'Shipment registered'),
                    ('Shipped', origin, 'Picked up by courier'),
                    ('In Transit', 'Midway Hub', 'At sorting facility'),
                    ('Out for Delivery', destination, 'Out for final delivery'),
                    ('Delivered', destination, 'Delivered to recipient')
                ],
            }
            for h in history_map.get(status, []):
                cursor.execute('''
                    INSERT INTO tracking_history (shipment_id, status, location, notes, timestamp)
                    VALUES (?, ?, ?, ?, datetime('now','-'||(abs(random())%5)||' days'))
                ''', (sid, h[0], h[1], h[2]))

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")
