import socket
import webbrowser
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from config import MAP_DIR, PORT


class ReusableTCPServer(TCPServer):
    allow_reuse_address = True


def is_server_running(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def start_server():
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(
        *args,
        directory=MAP_DIR,
        **kwargs
    )

    with ReusableTCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def launch():
    if not is_server_running(PORT):
        webbrowser.open(f"http://localhost:{PORT}/map.html", new=0)
        start_server()