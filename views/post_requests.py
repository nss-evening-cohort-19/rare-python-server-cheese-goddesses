import sqlite3
import json
from models import Post

def delete_post(id):
  """Delete Post"""
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE from post
    WHERE id = ?                
    """, (id, ))
