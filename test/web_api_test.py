import sqlite3
import unittest
import os
from populate_sqlite.seed import save_github_users_sqlite
from web.__main__ import create_app
from web.__main__ import get_total_users

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


class TestWebApi(unittest.TestCase):
    def setUp(self) -> None:
        save_github_users_sqlite(github_users, "test.db", "test")

        self.app = create_app(database_configuration={
            "database": "test.db",
            "table": "test"
        })

        self.client = self.app.test_client()

    def test_get_total_users(self):
        count = get_total_users(database="test.db", table="test")

        self.assertEqual(len(github_users), count)

    def test_profiles(self):
        response = self.client.get("/profiles")

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(github_users), len(response.get_json()["result"]))

    def test_limit_profiles(self):
        response = self.client.get("/profiles?size=10")

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.get_json()["result"]))

    def test_username_profiles(self):
        response = self.client.get("/profiles?username=mojombo")

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.get_json()["result"]))
        self.assertEqual({
                "id": 1.0,
                "username": "mojombo",
                "type": "User",
                "avatar": "https://avatars0.githubusercontent.com/u/1?v=4",
                "page": "https://github.com/mojombo"
            }, response.get_json()["result"][0]
        )

    def test_sort_username_profiles(self):
        response = self.client.get("/profiles?order_by=username")

        self.assertEqual(200, response.status_code)
        self.assertEqual({
                "id": 27.0,
                "username": "anotherjesse",
                "type": "User",
                "avatar": "https://avatars3.githubusercontent.com/u/27?v=4",
                "page": "https://github.com/anotherjesse"
            }, response.get_json()["result"][0]
        )

    def test_pagination_profiles(self):
        response = self.client.get("/profiles?size=1&page=2&order_by=username")

        print(response.get_json())

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            "id": 19.0,
            "username": "brynary",
            "type": "User",
            "avatar": "https://avatars0.githubusercontent.com/u/19?v=4",
            "page": "https://github.com/brynary"
        }, response.get_json()["result"][0]
        )

    def tearDown(self) -> None:
        connection = sqlite3.connect("test.db", uri=True)
        cursor = connection.cursor()

        cursor.execute("DROP TABLE test")

        connection.commit()
        connection.close()

        os.remove("test.db")


if __name__ == "__main__":
    unittest.main()
