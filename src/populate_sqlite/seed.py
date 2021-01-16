import github
import sqlite3
import argparse
import yaml
from github import RateLimitExceededException


def get_github_users(size: int, github_conf: dict = None) -> [tuple]:
    if not github_conf:
        github_client = github.Github()
    else:
        github_client = github.Github(**github_conf)

    users = github_client.get_users()

    github_users = []
    try:
        for user in users:
            if len(github_users) >= size:
                break

            github_users.append((
                user.id,
                user.login,
                user.type,
                user.avatar_url,
                user.html_url
            ))
    except RateLimitExceededException:
        return None

    return github_users


def save_github_users_sqlite(users: [tuple], database: str, table_name: str) -> None:
    if not users:
        return

    connection = sqlite3.connect(database, uri=True)
    cursor = connection.cursor()

    # Create the database in case if not exists
    table = cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name=?", (table_name, ))
    if table.fetchone():
        cursor.execute("DROP TABLE %s" % table_name)
    cursor.execute("CREATE TABLE %s (id real, username text, type text, avatar text, page text)" % table_name)

    for user in users:
        print("User to insert: {0}".format(user))
        cursor.execute(
            "INSERT INTO %s VALUES (?,?,?,?,?)" % table_name,
            user
        )

    connection.commit()
    connection.close()


if __name__ == '__main__':
    sqlite_database = None

    parser = argparse.ArgumentParser(
        description="Additional configuration to populate SQLite"
    )

    parser.add_argument(
        "-t", "--total",
        default="150",
        help="Total of users that will be added to the database"
    )

    parser.add_argument(
        "-c", "--config",
        default="config.yml",
        help="Configuration file where is saved the Github credentials"
    )

    args = parser.parse_args()
    sqlite_table = None
    try:
        with open(args.config, "r", encoding="utf-8") as config:
            config = yaml.load(config, Loader=yaml.FullLoader)
        if "credentials" in config["github"]:
            github_configuration = config["github"]["credentials"]
        elif "token" in config["github"]:
            github_configuration = config["github"]["token"]
        else:
            github_configuration = None

        sqlite_database = config["sqlite"]["database"]
        sqlite_table = config["sqlite"]["table"]
    except FileNotFoundError:
        github_configuration = None

    conf = None
    if github_configuration:
        if "username" in github_configuration and "password" in github_configuration:
            conf = {
                "login_or_token": github_configuration["username"],
                "password": github_configuration["password"]
            }
        elif "id" in github_configuration:
            conf = {
                "login_or_token": github_configuration["id"]
            }

    save_github_users_sqlite(
        users=get_github_users(github_conf=conf, size=int(args.total)),
        database=sqlite_database,
        table_name=sqlite_table
    )
