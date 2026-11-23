import tempfile
import unittest
from pathlib import Path

from booking import build_auditoriums, load_bookings, parse_seat, save_bookings, ticket_amount


class BookingTests(unittest.TestCase):
    def test_parse_seat(self):
        self.assertEqual(parse_seat("b10"), (1, 9))
        for label in ("A0", "K1", "A11", "bad"):
            with self.subTest(label=label):
                self.assertIsNone(parse_seat(label))

    def test_ticket_amount_includes_gst(self):
        self.assertEqual(ticket_amount(200, 2), (400, 72.0, 472.0))

    def test_saved_bookings_restore_seats(self):
        booking = {
            "id": "BK-123456",
            "movie": "Inception",
            "show_time": "10:00 AM",
            "seats": ["A1", "B10"],
            "price": 180,
        }
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bookings.json"
            save_bookings([booking], path)
            saved = load_bookings(path)

        self.assertEqual(saved, [booking])
        grid = build_auditoriums(saved)[(0, 0)]
        self.assertTrue(grid[0][0])
        self.assertTrue(grid[1][9])
        self.assertFalse(grid[0][1])


if __name__ == "__main__":
    unittest.main()
