import http.server
import socketserver
import os
import sys
port = 8080

args = sys.argv[1:]
if len(args) == 0:
    print("Correct usage: \n    share <filepath> [port]")
if len(args) >= 1:
    if os.path.isfile(args[0]):
        filepath = args[0]
    else:
        print("ERROR: invalid filepath")
        exit()
if len(args) == 2:
    try:
        port = int(args[1])
    except ValueError:
        print("ERROR: port must be an integer")
        exit()


with open("template.html") as file:
    template = file.read()

with open("person_2.ico","rb") as file:
    icon = file.read()
    
index = template.replace("{file}", filepath.split("\\")[-1])

path = "\\".join(filepath.split("\\")[:-1])
if path:
    os.chdir(path)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path == "/":
            self.wfile.write(bytes(index,"UTF-8"))
        elif self.path == "/favicon.ico":
            self.wfile.write(icon)
        elif self.path == "/"+filepath.split("\\")[-1]:
            with open(filepath.split("\\")[-1],"rb") as data:
                self.wfile.write(data.read())

with socketserver.TCPServer(("", port), Handler) as httpd:
    print("Running server at", port, "\nPress Ctrl+C to close")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Closing Server")
        exit()
