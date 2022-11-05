import sqlite3
import json
from models import Comment


COMMENTS = [
  {
        "id": 1,
        "author_id": 2,
        "post_id": 5,
        "content": "The article is good"
    }
]

def get_all_comments():
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    db_cursor.execute("""
      SELECT
          c.id,
          c.author_id,
          c.post_id,
          c.content
      FROM Comments c              
                      """)
    comments = []
    dataset = db_cursor.fetchall()
  for row in dataset:
    comment = Comment(row['id'], row['author_id'], row['post_id'],
                 row['content'])
    comments.append(comment.__dict__)
  return json.dumps(comments)

def get_single_comment(id):
  with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
          c.id,
          c.author_id,
          c.post_id,
          c.content
        FROM Comments c 
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        comment = Comment(data['id'], data['author_id'], data['post_id'],
                          data['content'])

        return json.dumps(comment.__dict__)

def delete_comment(id):
  """Delete Comment"""
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE from Comments
    WHERE id = ?                
    """, (id, ))
