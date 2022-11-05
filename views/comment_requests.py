import sqlite3
import json
from models import Comment


def create_comment(new_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Comments
            ( author_id, post_id, content )
        VALUES
            (?, ?, ?);
        """, (new_comment['author_id'], new_comment['post_id'],
              new_comment['content'], ))
        id = db_cursor.lastrowid
        new_comment['id'] = id
    return json.dumps(new_comment)
