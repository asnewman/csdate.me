import BaseHTTPServer
import sys

HOST_NAME = ''
PORT_NUMBER = 
REDIRECTIONS = {"/banana/": "http://csdate.me/"}
LAST_RESORT = "http://google.com/"

class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(301)
		s.send_header("Location", REDIRECTIONS).get(s.path, LAST_RESORT)
		s.end_headers()
	def do_GET(s):
		s.do_HEAD()

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), myHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
