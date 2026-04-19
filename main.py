import argparse
from database import initialize_db
from logger import log_session
from reports import show_recent_sessions, show_session_detail, show_weekly_load


def main():
    initialize_db()

    parser = argparse.ArgumentParser(
        prog="bjjlog",
        description="BJJ Training Log Tracker"
    )

    subparsers = parser.add_subparsers(dest="command")

    # log command
    subparsers.add_parser("log", help="Log a new session")

    # report commands
    subparsers.add_parser("recent", help="Show recent sessions")
    subparsers.add_parser("weekly", help="Show weekly load")

    detail_parser = subparsers.add_parser("detail", help="Show detail about session")
    detail_parser.add_argument("id", type=int, help="Session ID")

    args = parser.parse_args()

    if args.command == "log":
        log_session()
    elif args.command == "recent":
        show_recent_sessions()
    elif args.command == "weekly":
        show_weekly_load()
    elif args.command == "detail":
        show_session_detail(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()