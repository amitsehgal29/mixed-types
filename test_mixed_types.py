import os, tempfile, unittest
from mixed_types import kind, scan

class T(unittest.TestCase):
    def test_kind(self):
        self.assertEqual([kind(x) for x in ["1", "1.5", "2026-01-01", "true", "abc", "NULL"]],
                         ["int", "float", "date", "bool", "text", None])
    def test_scan(self):
        p = os.path.join(tempfile.mkdtemp(), "a.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("id,amt,dt\n1,10,2026-01-01\n2,10.5,2026-01-02\n3,,oops\n")
        rep = scan(p)
        self.assertNotIn("amt", rep)   # int+float is fine
        self.assertNotIn("id", rep)
        self.assertEqual(rep["dt"]["counts"], {"date": 2, "text": 1})
        self.assertEqual(rep["dt"]["examples"]["text"], ["oops"])

if __name__ == "__main__":
    unittest.main()
