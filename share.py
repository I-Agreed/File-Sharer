import http.server
import socketserver
import os
PORT = 8080


filepath = r"C:\Users\Brend\Desktop\download.png"

with open("template.html") as file:
    template = file.read()

with open("person_2.ico","rb") as file:
    icon = file.read()
    
index = template.replace("{file}", filepath.split("\\")[-1])


os.chdir("\\".join(filepath.split("\\")[:-1]))

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

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
