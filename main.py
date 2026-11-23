"""Command-line interface for the movie ticket booking system."""

from booking import (
    BOOKINGS_FILE,
    COLS,
    MOVIES,
    ROWS,
    ROW_LABELS,
    build_auditoriums,
    load_bookings,
    new_booking_id,
    parse_seat,
    save_bookings,
    seat_label,
    ticket_amount,
)


def prompt_int(message, low, high):
    while True:
        raw = input(message).strip()
        if raw.isdigit() and low <= int(raw) <= high:
            return int(raw)
        print(f"Enter a number from {low} to {high}.")


def confirm(message):
    while True:
        answer = input(message).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def choose_seats(grid, count):
    chosen = []
    while len(chosen) < count:
        raw = input(f"Select {count - len(chosen)} seat(s), e.g. A1, B2: ")
        for token in (part.strip() for part in raw.split(",")):
            seat = parse_seat(token)
            if seat is None:
                print(f"'{token}' is not a valid seat label.")
            elif grid[seat[0]][seat[1]]:
                print(f"Seat {seat_label(*seat)} is already booked.")
            elif seat in chosen:
                print(f"You already selected seat {seat_label(*seat)}.")
            else:
                chosen.append(seat)
                if len(chosen) == count:
                    break
    return chosen


def display_movies():
    print("\nNOW SHOWING")
    for index, movie in enumerate(MOVIES, start=1):
        prices = [show["price"] for show in movie["shows"]]
        print(f"{index}. {movie['name']} — Rs {min(prices)}–{max(prices)}")


def display_seats(grid):
    print("\nSeat layout: [ ] available  [X] booked")
    print("    " + " ".join(f"{number:>3}" for number in range(1, COLS + 1)))
    for row in range(ROWS):
        cells = " ".join("[X]" if seat else "[ ]" for seat in grid[row])
        print(f" {ROW_LABELS[row]}  {cells}")


def print_ticket(booking):
    base, gst, total = ticket_amount(booking["price"], len(booking["seats"]))
    print("\n" + "=" * 44)
    print(f"{'MOVIE TICKET':^44}")
    print("=" * 44)
    print(f"Booking ID    : {booking['id']}")
    print(f"Movie         : {booking['movie']}")
    print(f"Show          : {booking['show_time']}")
    print(f"Seats         : {', '.join(booking['seats'])}")
    print(f"Tickets       : {len(booking['seats'])} x Rs {booking['price']:.2f}")
    print(f"Base amount   : Rs {base:.2f}")
    print(f"GST (18%)     : Rs {gst:.2f}")
    print(f"Total         : Rs {total:.2f}")
    print("=" * 44)


def book_show(auditoriums, bookings, used_ids):
    display_movies()
    movie_index = prompt_int("Select a movie: ", 1, len(MOVIES)) - 1
    movie = MOVIES[movie_index]
    print(f"\nShows for {movie['name']}")
    for index, show in enumerate(movie["shows"], start=1):
        print(f"{index}. {show['time']} — Rs {show['price']}")
    show_index = prompt_int("Select a show: ", 1, len(movie["shows"])) - 1
    show = movie["shows"][show_index]
    grid = auditoriums[(movie_index, show_index)]
    free = sum(not seat for row in grid for seat in row)
    if free == 0:
        print("This show is full.")
        return

    display_seats(grid)
    count = prompt_int("Number of tickets: ", 1, min(10, free))
    seats = choose_seats(grid, count)
    labels = [seat_label(*seat) for seat in seats]
    _, _, total = ticket_amount(show["price"], count)
    print(f"\n{movie['name']} at {show['time']}")
    print(f"Seats: {', '.join(labels)}")
    print(f"Payable (including GST): Rs {total:.2f}")
    if not confirm("Confirm booking? (y/n): "):
        print("Booking cancelled. Seats were not reserved.")
        return

    booking = {
        "id": new_booking_id(used_ids),
        "movie": movie["name"],
        "show_time": show["time"],
        "seats": labels,
        "price": show["price"],
    }
    try:
        save_bookings([*bookings, booking])
    except OSError as error:
        print(f"Could not save the booking: {error}")
        return
    bookings.append(booking)
    for row, col in seats:
        grid[row][col] = True
    print_ticket(booking)


def main():
    print("Welcome to the theatre booking counter.")
    try:
        bookings = load_bookings()
    except (OSError, ValueError) as error:
        print(f"Could not read {BOOKINGS_FILE.name}: {error}")
        return
    auditoriums = build_auditoriums(bookings)
    used_ids = {booking["id"] for booking in bookings}
    while True:
        book_show(auditoriums, bookings, used_ids)
        if not confirm("\nBook another ticket? (y/n): "):
            print("Thank you. Counter closed.")
            break


if __name__ == "__main__":
    main()
