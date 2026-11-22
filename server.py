from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, os
from urllib.parse import urlparse, parse_qs
BASE=os.path.dirname(os.path.abspath(__file__))
STATE=os.path.join(BASE,'state.json')
VIDS={'gemini_generated_video_e96564d0.mp4','gemini_generated_video_e2ee4896.mp4'}
def rd():
 if os.path.exists(STATE):
  try:
   d=json.load(open(STATE,'r',encoding='utf-8'))
   if d.get('video') in VIDS: return d
  except Exception: pass
 return {'video':'gemini_generated_video_e96564d0.mp4'}
def wr(v): json.dump({'video':v},open(STATE,'w',encoding='utf-8'))
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw): super().__init__(*a,directory=BASE,**kw)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=='/api/state':
   b=json.dumps(rd()).encode()
   self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  if p.path=='/api/set-video':
   v=parse_qs(p.query).get('file',[''])[0]
   if v in VIDS:
    wr(v); b=json.dumps({'ok':True,'video':v}).encode(); self.send_response(200)
   else:
    b=json.dumps({'ok':False}).encode(); self.send_response(400)
   self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  super().do_GET()
wr(rd()['video'])
ThreadingHTTPServer(('127.0.0.1',8080),H).serve_forever()
