from database import get_connection


def add_tag(name, tag_type=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tags (name, tag_type) VALUES (?, ?)",
            (name.strip().lower(), tag_type)
        )
        conn.commit()
        print(f"Tag '{name}' added.")
    except Exception as e:
        print(f"Tag '{name}' already exists.")
    finally:
        conn.close()

def get_all_tags():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM tags ORDER BY tag_type, name")
    tags = cursor.fetchall()
    conn.close()
    return tags

def get_or_create_tag(name, tag_type=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags WHERE name = ?", (name.strip().lower(), ))
    tag = cursor.fetchone()
    if tag:
        conn.close()
        return tag["id"]
    cursor.execute(
        "INSERT INTO tags (name, tag_type) VALUES (?, ?)",
        (name.strip().lower(), tag_type)
    )
    conn.commit()
    tag_id = cursor.lastrowid
    conn.close()
    return tag_id

if __name__ == "__main__":
    add_tag("sweep single", "move")
    add_tag("collar drag", "move")
    add_tag("turtle", "position")
    add_tag("half guard", "position")
    print("\nAll tags:")
    for tag in get_all_tags():
        print(f" [{tag['tag_type']}] {tag['name']}")