# Movie Ticket Booking System

## About the project

This Python command-line project simulates booking seats at a theatre. A user chooses a movie and show, selects available seats, confirms the amount including 18% GST, and receives a formatted ticket with a booking ID.

Confirmed bookings are stored in `bookings.json` and restored when the program starts again. This is a local classroom project: it does not process online payments or coordinate reservations across multiple computers.

## Objectives

- Model the basic steps of booking a movie ticket.
- Display movies, show times, ticket prices, and a 10 × 10 seat layout.
- Validate choices and prevent duplicate or unavailable seat selections.
- Calculate ticket totals with GST and produce a booking ticket.
- Practise Python functions, collections, input validation, and file handling.

## Features

- Four movies with three show times each.
- Seat selection for up to ten tickets per booking.
- Validation for movie, show, and seat choices.
- Prevention of repeat and already-booked seat selections.
- Unique booking IDs and a ticket showing the base amount, GST, and total.
- JSON persistence so confirmed seats remain booked after restart.
- Atomic replacement when saving the bookings file.

## Technologies used

- Python 3
- Python standard library only: `json`, `pathlib`, and `secrets`
- `unittest` for tests; no external packages required

## Python concepts used

Functions, lists, dictionaries, sets, tuples, loops, conditionals, input validation, comprehensions, JSON file handling, exceptions, and formatted strings.

## How to run

Open this folder in VS Code or a terminal. Python 3 must be installed.

```bash
python main.py
```

To run the tests:

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
MovieTicketBookingSystem/
├── booking.py             # Movie data, seat logic, totals, and JSON storage
├── main.py                # Terminal menus and booking flow
├── tests/
│   └── test_booking.py    # Seat, price, and persistence tests
├── .gitignore
└── README.md
```

The generated `bookings.json` file is kept on the local computer and ignored by Git.

## Team

- Simran Kumari — 46
- Aryavrat Chakraborty — 9
- Tanvi Sachin Chavan — 36

## Repository

https://github.com/aryavratchakrabort-afk/MovieTicketBookingSystem
