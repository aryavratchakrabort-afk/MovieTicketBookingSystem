# Movie Ticket Booking System

A Python command-line project that simulates booking seats at a theatre. Choose a movie and show, select seats, confirm the price including 18% GST, and receive a ticket with a booking ID.

## Run

Requires Python 3. Run from this folder:

```bash
python main.py
```

The project uses only Python's standard library. Confirmed bookings are saved to `bookings.json` in this folder and restored the next time the program starts. The file is created automatically.

## Test

```bash
python -m unittest discover -s tests
```

## Project files

- `main.py` — menu, input, seat selection, and ticket display.
- `booking.py` — movie data, seat parsing, price calculation, and JSON storage.
- `tests/` — small standard-library tests for seat labels, totals, and saved bookings.

## Python concepts

Functions, lists, dictionaries, sets, loops, conditionals, input validation, JSON files, and formatted strings.

## Team

- Simran Kumari — 46
- Aryavrat Chakraborty — 9
- Tanvi Sachin Chavan — 36
