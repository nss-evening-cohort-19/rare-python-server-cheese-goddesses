import sqlite3
import json
from models import Post

POSTS = [
  {
        "id": 1,
        "user_id": 2,
        "category_id": 5,
        "title": "Inflation in 2022",
        "publication_date": "11/9/2022",
        "image_url": "https://advisor.visualcapitalist.com/wp-content/uploads/2022/02/mapping-forecasted-inflation-2022.jpg",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
        "approved": True
    },
    {
        "id": 2,
        "user_id": 1,
        "category_id": 6,
        "title": "Bootcamps",
        "publication_date": "10/11/2022",
        "image_url": "https://www.northeastern.edu/graduate/blog/wp-content/uploads/2019/05/coding-bootcamp.jpg",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing",
        "approved": True
    },
    {
        "id": 3,
        "user_id": 8,
        "category_id": 9,
        "title": "Boot",
        "publication_date": "10/11/2022",
        "image_url": "https://img.freepik.com/free-vector/book-with-lighbulb-cartoon-vector-icon-illustration-object-education-icon-concept-isolated-premium-vector-flat-cartoon-style_138676-4009.jpg",
        "content": "occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "approved": False
    }
]


def update_post(id, new_post):
    """disable error"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Post
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['content'],new_post['approved'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
