import sqlite3
import unittest
from populate_sqlite.seed import get_github_users
from populate_sqlite.seed import save_github_users_sqlite

github_users = [
    ("1", "mojombo", "User", "https://avatars0.githubusercontent.com/u/1?v=4", "https://github.com/mojombo"),
    ("2", "defunkt", "User", "https://avatars0.githubusercontent.com/u/2?v=4", "https://github.com/defunkt"),
    ("3", "pjhyett", "User", "https://avatars0.githubusercontent.com/u/3?v=4", "https://github.com/pjhyett"),
    ("4", "wycats", "User", "https://avatars0.githubusercontent.com/u/4?v=4", "https://github.com/wycats"),
    ("5", "ezmobius", "User", "https://avatars0.githubusercontent.com/u/5?v=4", "https://github.com/ezmobius"),
    ("6", "ivey", "User", "https://avatars0.githubusercontent.com/u/6?v=4", "https://github.com/ivey"),
    ("7", "evanphx", "User", "https://avatars0.githubusercontent.com/u/7?v=4", "https://github.com/evanphx"),
    ("17", "vanpelt", "User", "https://avatars1.githubusercontent.com/u/17?v=4", "https://github.com/vanpelt"),
    ("18", "wayneeseguin", "User", "https://avatars0.githubusercontent.com/u/18?v=4",
     "https://github.com/wayneeseguin"),
    ("19", "brynary", "User", "https://avatars0.githubusercontent.com/u/19?v=4", "https://github.com/brynary"),
    ("20", "kevinclark", "User", "https://avatars3.githubusercontent.com/u/20?v=4",
     "https://github.com/kevinclark"),
    ("21", "technoweenie", "User", "https://avatars3.githubusercontent.com/u/21?v=4",
     "https://github.com/technoweenie"),
    ("22", "macournoyer", "User", "https://avatars3.githubusercontent.com/u/22?v=4",
     "https://github.com/macournoyer"),
    ("23", "takeo", "User", "https://avatars3.githubusercontent.com/u/23?v=4", "https://github.com/takeo"),
    ("25", "caged", "User", "https://avatars3.githubusercontent.com/u/25?v=4", "https://github.com/caged"),
    ("26", "topfunky", "User", "https://avatars3.githubusercontent.com/u/26?v=4", "https://github.com/topfunky"),
    ("27", "anotherjesse", "User", "https://avatars3.githubusercontent.com/u/27?v=4",
     "https://github.com/anotherjesse"),
    ("28", "roland", "User", "https://avatars2.githubusercontent.com/u/28?v=4", "https://github.com/roland"),
    ("29", "lukas", "User", "https://avatars2.githubusercontent.com/u/29?v=4", "https://github.com/lukas")
]


class TestPopulateSqlite(unittest.TestCase):

    def test_get_github_users_without_count(self):
        users = get_github_users(150, None)

        self.assertIsNotNone(users)
        self.assertEqual(len(users), 150)

    def test_get_a_lot_github_users_without_count(self):
        users = get_github_users(10000, None)

        self.assertIsNone(users)

    def test_save_users_to_db(self):
        save_github_users_sqlite(users=github_users, database="test.db", table_name="test")

        connection = sqlite3.connect("test.db", uri=True)
        cursor = connection.cursor()

        count = cursor.execute("SELECT COUNT() FROM test").fetchone()[0]

        connection.close()

        self.assertEqual(count, len(github_users))


if __name__ == "__main__":
    unittest.main()
