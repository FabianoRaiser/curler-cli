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


if __name__ == "__main__":
    unittest.main()
