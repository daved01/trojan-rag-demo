import json
import sys
import src.config as config


def load_queries():
    """
    Parses the JSON file containing the test queries.
    """

    if not config.QUERIES_FILE.exists():
        print(f"rror: queries.json not found at {config.QUERIES_FILE}")
        sys.exit(1)
        
    with open(config.QUERIES_FILE, "r") as f:
        return json.load(f)
