import sqlite3
import json
from models import Subscription

SUBSCRIPTIONS = [
  {
        "id": 1,
        "follower_id": 2,
        "author_id": 5,
        "created_on": "11/9/2022"
    },
]

def create_subscription(new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ?);
        """, (new_subscription['follower_id'], new_subscription['author_id'],
              new_subscription['created_on']))
        
        id = db_cursor.lastrowid

        new_subscription['id'] = id

    return json.dumps(new_subscription)
  
def get_all_subscriptions():
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    db_cursor.execute("""
      SELECT
          s.id,
          s.follower_id,
          s.author_id,
          s.created_on
      FROM Subscriptions s             
                      """)
    subscriptions = []
    dataset = db_cursor.fetchall()
  for row in dataset:
    subscription = Subscription(row['id'], row['follower_id'], row['author_id'],
                row['created_on'] )
    subscriptions.append(subscription.__dict__)
  return json.dumps(subscriptions)

def get_single_subscription(id):
  with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
          s.id,
          s.follower_id,
          s.author_id,
          s.created_on
        FROM Subscriptions s
        WHERE s.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        subscription = Subscription(data['id'], data['follower_id'], data['author_id'],
                            data['created_on'] )

        return json.dumps(subscription.__dict__)

  
def update_subscription(id, new_subscription):
    """disable error"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Subscriptions
            SET
                follower_id = ?,
                author_id = ?,
                created_on = ?
        WHERE id = ?
        """, (new_subscription['follower_id'], new_subscription['author_id'],
              new_subscription['created_on'], id, ))
        
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
    
def delete_subscription(id):
  """Delete Subscription"""
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE from Subscriptions
    WHERE id = ?                
    """, (id, ))
