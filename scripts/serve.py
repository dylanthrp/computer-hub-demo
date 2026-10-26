"""Serve only public preview files, on loopback, never project originals or docs."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse

ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def allowed(self):
        path=unquote(urlsplit(self.path).path)
        if path in ('/','/index.html'): return True
        return path.startswith('/assets/') and '..' not in path and not path.startswith('/assets/originals/') and not path.endswith('/')
    def do_GET(self):
        if not self.allowed(): self.send_error(404);return
        super().do_GET()
    def do_HEAD(self):
        if not self.allowed(): self.send_error(404);return
        super().do_HEAD()
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-Robots-Tag','noindex, nofollow')
        super().end_headers()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4208);args=parser.parse_args()
    print(f'Local preview: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
