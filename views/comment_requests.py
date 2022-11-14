import sqlite3
import json
from models import Comment, Post


COMMENTS = [
  {
        "id": 1,
        "post_id": 2,
        "author_id": 5,
        "content": "A New Book Release"
  }
]

def update_comment(id, new_comment):
    """PUT method to update comment"""
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

def delete_comment(id):
  """Delete Comment"""
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE from Comments
    WHERE id = ?                
    """, (id, ))

# def get_comments_by_post_id(post_id):

#     with sqlite3.connect("./db.sqlite3") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         # Write the SQL query to get the information you want
#         db_cursor.execute("""
#         select
#             c.id,
#             c.author_id,
#             c.post_id,
#             c.content
#             p.id,
          
#         FROM Comment c
#         JOIN Post p
#             ON p.id = c.post_id
#         """)

#         comments = []
#         dataset = db_cursor.fetchall()

#         for row in dataset:
#           comment = Comment(row['id'], row['author_id'], row['post_id'], row['content'])
          
#           post = Post(row['id'], row['user_id'], row['category_id'],
#                 row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])

#           comment.post = post.__dict__
#           comments.append(comment.__dict__)
          
          
          
#     return json.dumps(comments)


def get_comments_by_post_id(post_id):
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
        WHERE c.post_id = ?
        """, ( post_id, ))

        data = db_cursor.fetchone()

        comment = Comment(data['id'], data['author_id'], data['post_id'],
                          data['content'])

        return json.dumps(comment.__dict__)
