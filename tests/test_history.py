import unittest

from curler.history import History, HistoryEntry


class HistoryTest(unittest.TestCase):
    def test_push_and_current(self):
        history = History()
        entry = HistoryEntry(url="https://a.com", headers="", body="A")

        history.push(entry)

        self.assertEqual(history.current, entry)

    def test_back_and_forward(self):
        history = History()
        a = HistoryEntry(url="https://a.com", headers="", body="A")
        b = HistoryEntry(url="https://b.com", headers="", body="B")
        c = HistoryEntry(url="https://c.com", headers="", body="C")

        history.push(a)
        history.push(b)
        history.push(c)

        self.assertEqual(history.back(), b)
        self.assertEqual(history.back(), a)
        self.assertFalse(history.can_go_back())

        self.assertEqual(history.forward(), b)
        self.assertEqual(history.forward(), c)
        self.assertFalse(history.can_go_forward())

    def test_push_clears_forward_stack(self):
        history = History()
        a = HistoryEntry(url="https://a.com", headers="", body="A")
        b = HistoryEntry(url="https://b.com", headers="", body="B")
        alt = HistoryEntry(url="https://alt.com", headers="", body="Alt")

        history.push(a)
        history.push(b)
        history.back()
        history.push(alt)

        self.assertEqual(history.current, alt)
        self.assertFalse(history.can_go_forward())

    def test_back_at_start_returns_current(self):
        history = History()
        entry = HistoryEntry(url="https://a.com", headers="", body="A")
        history.push(entry)

        self.assertEqual(history.back(), entry)
        self.assertFalse(history.can_go_back())

    def test_forward_at_end_returns_current(self):
        history = History()
        a = HistoryEntry(url="https://a.com", headers="", body="A")
        b = HistoryEntry(url="https://b.com", headers="", body="B")

        history.push(a)
        history.push(b)

        self.assertEqual(history.forward(), b)
        self.assertFalse(history.can_go_forward())

    def test_empty_history_has_no_current(self):
        history = History()

        self.assertIsNone(history.current)
        self.assertFalse(history.can_go_back())
        self.assertFalse(history.can_go_forward())

    def test_stores_final_url_and_body_after_push(self):
        history = History()
        entry = HistoryEntry(
            url="https://example.com/final",
            headers="HTTP/2 200\n\n",
            body="<html><body>Cached</body></html>",
        )

        history.push(entry)

        self.assertEqual(history.current.url, "https://example.com/final")
        self.assertEqual(history.current.body, entry.body)
        self.assertEqual(history.current.headers, entry.headers)


if __name__ == "__main__":
    unittest.main()
