import argparse
import yaml

parser = argparse.ArgumentParser(
    description="Additional configuration to populate SQLite"
)

parser.add_argument(
    "-p", "--port",
    default=500,
    help="Port where the server will be exposed"
)

parser.add_argument(
    "-s", "--size",
    default=25,
    help="Default value for pagination size"
)

parser.add_argument(
    "-c", "--config",
    default="config.yml",
    help="Configuration file where is saved the Github credentials"
)

args = parser.parse_args()

try:
    with open(args.config, "r", encoding="utf-8") as config:
        config = yaml.load(config, Loader=yaml.FullLoader)
except FileNotFoundError:
    # Default values of database name and table name if config doesn't exist
    config = {
        "database": "prueba.db",
        "table": "users"
    }
