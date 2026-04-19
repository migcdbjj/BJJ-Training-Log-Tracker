from database import get_connection
from tags import get_or_create_tag
from datetime import date


SESSION_TYPES = ["drilling", "sparring", "comp prep", "open mat"]
TAG_TYPES = ["move", "position", "submission", "concept"]
CONTEXTS = ["working_on", "landed", "got_you"]


def prompt_int(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Numbers only please.")


def prompt_choice(prompt, choices):
    print(prompt)
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    while True:
        try:
            val = int(input("Enter number: "))
            if 1 <= val <= len(choices):
                return choices[val - 1]
            print(f"Pick a number between 1 and {len(choices)}.")
        except ValueError:
            print("Numbers only please.")


def prompt_tags(context_label):
    print(f"\n-- {context_label.upper()} tags (leave blank to finish) --")
    tag_ids = []
    while True:
        name = input("Tag name: ").strip()
        if not name:
            break
        tag_type = prompt_choice("Tag type:", TAG_TYPES)
        tag_id = get_or_create_tag(name, tag_type)
        tag_ids.append(tag_id)
        print(f"  Added '{name}'")
    return tag_ids


def log_session():
    print("\n=== LOG BJJ SESSION ===\n")


    # Date
    today = date.today().isoformat()
    date_input = input(f"Date [{today}]: ").strip()
    session_date = date_input if date_input else today

    # Duration
    duration = prompt_int("Duration (minutes): ", 1, 480)

    # Session type
    session_type = prompt_choice("\nSession type:", SESSION_TYPES)

    # Rounds
    rounds = prompt_int("\nNumber of rounds: ", 0, 50)

    # Intensity
    intensity = prompt_int("\nIntensity RPE (1-10): ", 1, 10)

    # Feeling before/after
    feeling_before = prompt_int("\nFeeling BEFORE: (1-10): ", 1, 10)
    feeling_after = prompt_int("\nFeeling AFTER: (1-10): ", 1, 10)

    # Notes
    notes = input("\nNotes (optional): ").strip() or None

    # Tags
    working_on = prompt_tags("working_on")
    landed = prompt_tags("landed")
    got_you = prompt_tags("got_you")

    # Write to DB
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions
            (date, duration, session_type, rounds, intensity, feeling_before, feeling_after, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_date, duration, session_type, rounds, intensity, feeling_before, feeling_after, notes))

    session_id = cursor.lastrowid

    for tag_id in working_on:
        cursor.execute("INSERT INTO session_tags VALUES (?, ?, ?)", (session_id, tag_id, "working_on"))
    for tag_id in landed:
        cursor.execute("INSERT INTO session_tags VALUES (?, ?, ?)", (session_id, tag_id, "landed"))
    for tag_id in got_you:
        cursor.execute("INSERT INTO session_tags VALUES (?, ?, ?)", (session_id, tag_id, "got_you"))

    conn.commit()
    conn.close()

    print(f"\nSession logged! ID: {session_id}")

if __name__ == "__main__":
    log_session()
