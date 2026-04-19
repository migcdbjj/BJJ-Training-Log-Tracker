from database import get_connection
from rich.console import Console
from rich.table import Table

console = Console()

def get_recent_sessions(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM sessions
        ORDER BY date DESC
        LIMIT ?
    """, (limit,))
    sessions = cursor.fetchall()
    conn.close()
    return sessions


def get_session_tags(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.name, t.tag_type, st.context
        FROM session_tags st
        JOIN tags t ON st.tag_id = t.id
        WHERE st.session_id = ?
        ORDER BY st.context, t.name
    """, (session_id,))
    tags = cursor.fetchall()
    conn.close()
    return tags


def show_recent_sessions(limit=10):
    sessions = get_recent_sessions(limit)

    if not sessions:
        console.print("[yellow]No sessions logged yet.[/yelllow]")
        return

    table = Table(title="Recent Sessions", show_lines=True)
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Type")
    table.add_column("Duration", justify="right")
    table.add_column("Rounds", justify="right")
    table.add_column("RPE", justify="right")
    table.add_column("Before", justify="right")
    table.add_column("After", justify="right")
    table.add_column("Notes")

    for s in sessions:
        table.add_row(
            str(s["id"]),
            s["date"],
            s["session_type"],
            f"{s['duration']}min",
            str(s["rounds"]),
            str(s["intensity"]),
            str(s["feeling_before"]),
            str(s["feeling_after"]),
            s["notes"] or ""
        )

    console.print(table)


def show_session_detail(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    conn.close()

    if not session:
        console.print(f"[red]Session {session_id} not found.[/red]")
        return

    console.print(f"\n[bold]Session {session_id} - {session['date']}[/bold]")
    console.print(f"Type: {session['session_type']} | Duration: {session ['duration']}min | Rounds: {session['rounds']}")
    console.print(f"RPE: {session['intensity']} | Feeling before: {session['feeling_before']} | after: {session['feeling_after']}")
    if session['notes']:
        console.print(f"Notes: {session['notes']}")

    tags = get_session_tags(session_id)
    if tags:
        working_on = [t["name"] for t in tags if t["context"] == "working_on"]
        landed = [t["name"] for t in tags if t["context"] == "landed"]
        got_you = [t["name"] for t in tags if t["context"] == "got_you"]

    if working_on:
        console.print(f"\n[cyan]Working on:[/cyan] {','.join(working_on)}")
    if landed:
        console.print(f"[green]Landed:[/green] {','.join(landed)}")
    if got_you:
        console.print(f"[red]Got you:[/red] {','.join(got_you)}")



def show_weekly_load():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            strftime('%Y-W%W', date) as week,
            COUNT(*) as sessions,
            SUM(duration) as total_minutes,
            ROUND(AVG(intensity), 1) as avg_rpe,
            ROUND(AVG(feeling_before), 1) as avg_before,
            ROUND(AVG(feeling_after), 1) as avg_after
        FROM sessions
        GROUP BY week
        ORDER BY week DESC
        LIMIT 8
    """)
    weeks = cursor.fetchall()
    conn.close()

    if not weeks:
        console.print("[yellow]No data yet.[/yellow]")
        return

    if not weeks:
        console.print("[yellow]No data yet.[/yellow]")
        return

    table = Table(title="Weekly Load", show_lines=True)
    table.add_column("Week")
    table.add_column("Sessions", justify="right")
    table.add_column("Total Time", justify="right")
    table.add_column("Avg RPE", justify="right")
    table.add_column("Avg Before", justify="right")
    table.add_column("Avg After", justify="right")

    for w in weeks:
        table.add_row(
            w["week"],
            str(w["sessions"]),
            f"{w['total_minutes']} min",
            str(w["avg_rpe"]),
            str(w["avg_before"]),
            str(w["avg_after"])
        )

    console.print(table)

if __name__ == "__main__":
    show_recent_sessions()
    print()
    show_session_detail(1)
    print()
    show_weekly_load()