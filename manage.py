from pathlib import Path
import argparse

from app import data, db

SCRIPT_DIR = Path(__file__).parent


def init(args):
    db.init_db()
    print(f"Database initialized at {db.get_db_path()}")


def seed(args):
    db.init_db()
    db.seed_sample_shipments(data.SAMPLE_SHIPMENTS)
    print("Sample shipments seeded.")


def reset(args):
    db_path = db.get_db_path()
    if db_path != ":memory" and Path(db_path).exists():
        Path(db_path).unlink()
    db.init_db()
    print("Database reset.")


def main():
    parser = argparse.ArgumentParser(description="Manage the AI Logistics Platform database.")
    subparsers = parser.add_subparsers(dest="command")

    parser_init = subparsers.add_parser("init", help="Initialize the database")
    parser_init.set_defaults(func=init)

    parser_seed = subparsers.add_parser("seed", help="Seed the database with sample shipments")
    parser_seed.set_defaults(func=seed)

    parser_reset = subparsers.add_parser("reset", help="Reset the database")
    parser_reset.set_defaults(func=reset)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
