import unittest
from fabric_excel_demo.transform import newest_records, parse_utc, validate_columns


class TestTransform(unittest.TestCase):
    def test_overlap_keeps_latest_record(self):
        earlier = {"record_id": "A01", "activity_date": "2026-01-01", "amount": 10,
                   "updated_at": "2026-01-02T10:00:00Z"}
        later = dict(earlier, amount=15, updated_at="2026-01-03T10:00:00+00:00")
        self.assertEqual(newest_records([later, earlier])[0]["amount"], 15)

    def test_missing_field(self):
        with self.assertRaises(ValueError):
            validate_columns(["record_id"])

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            parse_utc("2026-01-02T10:00:00")

    def test_repeated_batch_is_stable(self):
        row = {"record_id": "B02", "activity_date": "2026-01-01", "amount": 5,
               "updated_at": "2026-01-02T10:00:00Z"}
        self.assertEqual(newest_records([row, row]), [row])


if __name__ == "__main__":
    unittest.main()
