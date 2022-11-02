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

def get_single_post(id):
  with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM post p
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'],
                            data['title'], data['publication_date'],
                            data['image_url'],data['content'],data['approved'])

        return json.dumps(post.__dict__)
