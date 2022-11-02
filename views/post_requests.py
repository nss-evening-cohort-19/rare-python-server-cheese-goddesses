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
    
def create_post(new_post):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Post
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id


    return json.dumps(new_post)
