from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import (delete_post,
                   get_single_post, 
                   get_all_posts, 
                   update_post, 
                   create_post, 
                   create_comment, 
                   get_single_comment, 
                   get_all_comments, 
                   delete_comment,
                   update_comment,
                   get_single_category, 
                   get_all_categories, 
                   create_category, 
                   update_category,
                   delete_category,
                   create_user, 
                   login_user,
                   create_post_reaction,
                   get_all_post_reactions,
                   get_single_post_reaction,
                   update_post_reaction,
                   delete_post_reaction,
                   create_subscription,
                   get_all_subscriptions,
                   get_single_subscription,
                   update_subscription,
                   delete_subscription,
                   get_category_by_post
                   )
class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """GET Posts and comments"""
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)
        if '?' not in self.path:
            (resource, id) = parsed
            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == "comments":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"
            elif resource == "post_reactions":
                if id is not None:
                    response = f"{get_single_post_reaction(id)}"
                else:
                    response = f"{get_all_post_reactions()}"
            elif resource == "subscriptions":
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_all_subscriptions()}"
        else:  
            (resource, query) = parsed
            if query.get('category_id') and resource == 'posts':
                response = get_category_by_post(query['category_id'])
        self.wfile.write(response.encode())


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        response = ''
        (resource, id) = self.parse_url(self.path)
        
        if resource == "posts":
            response = create_post(post_body)
        elif resource == "comments":
            response = create_comment(post_body)
        elif resource == "categories":
            response = create_category(post_body)
        elif resource == "subscriptions":
            response = create_subscription(post_body)
        elif resource == 'login':
            response = login_user(post_body)
        elif resource == 'register':
            response = create_user(post_body)
        elif resource == "post_reactions":
            response = create_post_reaction(post_body)
        
        self.wfile.write(response.encode())

    def do_PUT(self):
        """to update a post, makes a put request to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False

        if resource == "posts":
            success = update_post(id, post_body)
            
        if resource == "comments":
            success = update_comment(id, post_body)
            
        if resource == "categories":
            success = update_category(id, post_body)
            
        if resource == "post_reactions":
            success = update_post_reaction(id, post_body)
        if resource == "subscriptions":
            success = update_subscription(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
            
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        if resource == "posts":
            delete_post(id)
        if resource == "categories":
            delete_category(id)
        if resource == "comments":
            delete_comment(id)
        if resource == "post_reactions":
            delete_post_reaction(id)
            delete_comment(id)  
        if resource == "subscriptions":
            delete_subscription(id)  
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
