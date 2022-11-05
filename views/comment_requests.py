import sqlite3
import json
from models import Comment

COMMENTS = [
  {
        "id": 1,
        "post_id": 2,
        "author_id": 5,
        "content": "A New Book Release"
  }
]

def update_comment(id, new_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE Comments
            SET
                post_id = ?,
                author_id = ?,
                content = ?
        WHERE id = ?
        """, (new_comment['post_id'], new_comment['author_id'],
              new_comment['content'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
  
