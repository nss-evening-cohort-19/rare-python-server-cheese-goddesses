import sqlite3
import json
from models import Comment


def delete_comment(id):
  """Delete Comment"""
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE from Comments
    WHERE id = ?                
    """, (id, ))
