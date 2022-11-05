import sqlite3
import json
from models import Category

CATEGORY = [
  {
    "id": 1,
    "label": "Economy"
  },
  {
      "id": 2,
      "label": "Education"
  },
  {
      "id": 3,
      "label": "Hobbies"
  },
  {
      "id": 4,
      "label": "Other"
  }
]


def update_category(id, new_category):
    """disable error"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_category(id):
  """Delete Post"""
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE from Categories
    WHERE id = ?                
    """, (id, ))


def create_category(new_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO categories
            (label)
        VALUES
            (?);
        """, (new_category['label'], ))

        id = db_cursor.lastrowid

        new_category['id'] = id

    return json.dumps(new_category)


def get_all_categories():
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    db_cursor.execute("""
      SELECT
          c.id,
          c.label
      FROM Categories c               
                      """)
    categories = []
    dataset = db_cursor.fetchall()
  for row in dataset:
    category = Category(row['id'], row['label'])
    categories.append(category.__dict__)
  return json.dumps(categories)


def get_single_category(id):
  with sqlite3.connect("./db.sqlite3") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()
      db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        WHERE c.id = ?
        """, (id, ))

      data = db_cursor.fetchone()

      category = Category(data['id'], data['category'])

      return json.dumps(category.__dict__)
