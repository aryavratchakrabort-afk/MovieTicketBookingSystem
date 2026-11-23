"""Core data and storage for the movie ticket booking project."""

import json
import secrets
from pathlib import Path

GST_RATE = 0.18
ROWS = 10
COLS = 10
ROW_LABELS = "ABCDEFGHIJ"
BOOKINGS_FILE = Path(__file__).with_name("bookings.json")

MOVIES = [
    {"name": "Inception", "shows": [
        {"time": "10:00 AM", "price": 180},
        {"time": "02:00 PM", "price": 220},
        {"time": "06:30 PM", "price": 280},
    ]},
    {"name": "The Dark Knight", "shows": [
        {"time": "11:15 AM", "price": 200},
        {"time": "03:00 PM", "price": 240},
        {"time": "07:45 PM", "price": 300},
    ]},
    {"name": "Interstellar", "shows": [
        {"time": "09:30 AM", "price": 190},
        {"time": "01:00 PM", "price": 230},
        {"time": "08:00 PM", "price": 320},
    ]},
    {"name": "Dune", "shows": [
        {"time": "12:00 PM", "price": 210},
        {"time": "04:30 PM", "price": 260},
        {"time": "09:15 PM", "price": 340},
    ]},
]

def parse_seat(token):
    """Return a seat's (row, column), or None when its label is invalid."""
    text = token.strip().upper()
    if len(text) < 2 or text[0] not in ROW_LABELS or not text[1:].isdigit():
        return None
    col = int(text[1:])
    if not 1 <= col <= COLS:
        return None
    return ROW_LABELS.index(text[0]), col - 1

def seat_label(row, col):
    return f"{ROW_LABELS[row]}{col + 1}"

def ticket_amount(price, count):
    """Return the base amount, GST, and total for a booking."""
    base = price * count
    gst = round(base * GST_RATE, 2)
    return base, gst, round(base + gst, 2)

def load_bookings(path=BOOKINGS_FILE):
    if not path.exists():
        return []
    bookings = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(bookings, list):
        raise ValueError("The bookings file must contain a list.")
    return bookings

def save_bookings(bookings, path=BOOKINGS_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(bookings, indent=2), encoding="utf-8")
    temporary.replace(path)

def build_auditoriums(bookings):
    """Create one seat grid per show and restore its saved bookings."""
    auditoriums = {
        (movie_index, show_index): [[False] * COLS for _ in range(ROWS)]
        for movie_index, movie in enumerate(MOVIES)
        for show_index, _ in enumerate(movie["shows"])
    }
    show_indexes = {
        (movie["name"], show["time"]): (movie_index, show_index)
        for movie_index, movie in enumerate(MOVIES)
        for show_index, show in enumerate(movie["shows"])
    }
    for booking in bookings:
        key = (booking["movie"], booking["show_time"])
        if key not in show_indexes:
            continue
        grid = auditoriums[show_indexes[key]]
        for label in booking["seats"]:
            seat = parse_seat(label)
            if seat is not None:
                grid[seat[0]][seat[1]] = True
    return auditoriums

def new_booking_id(used_ids):
    while True:
        booking_id = f"BK-{secrets.token_hex(3).upper()}"
        if booking_id not in used_ids:
            used_ids.add(booking_id)
            return booking_id
