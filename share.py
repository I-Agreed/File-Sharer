import http.server
import socketserver
import os
import sys
import socket

ip = socket.gethostbyname(socket.gethostname())
port = 8080

args = sys.argv[1:]
if len(args) == 0:
    print("Correct usage: \n    share <filepath> [port]")
    exit()
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
            print("File downloaded from: "+self.client_address[0])
            with open(filepath.split("\\")[-1],"rb") as data:
                self.wfile.write(data.read())
                
    def log_message(self, format, *args):
        pass
    
try:
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("Running server at", ip+":"+str(port), "\nPress Ctrl+C to close")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Closing Server")
            httpd.server_close()
            exit()
except OSError:
    print("Port already in use")
