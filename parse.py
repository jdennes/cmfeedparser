# Give me a feed url, and I'll attempt to parse it for you and give you JSON
# Usage: /?url=http://example.com/feed
# Dependencies: python 2.6+, feedparser, and web.py
# Now runs on GAE, using web.py rather than webapp2 (so it can easily be run elsewhere)

from google.appengine.ext.webapp.util import run_wsgi_app
import web
import json
import feedparser
import time

def to_json(python_object):
  if isinstance(python_object, time.struct_time):
    return {'__class__': 'time.asctime',
            '__value__': time.asctime(python_object)}
  raise TypeError(repr(python_object) + ' is not JSON serializable')

urls = ('/', 'Parser')
app = web.application(urls, globals())

class Parser:
  def GET(self):
    web.header('Content-Type', 'application/json')
    try:
      url = web.input().url
      return json.dumps(feedparser.parse(url), default=to_json)
    except Exception as e:
      web.ctx.status = "400 Bad Request"
      return json.dumps({"message": "Sorry, i couldn't parse that feed. Usage: /?url=http://example.com/feed"})

if __name__ == "__main__":
  application = app.wsgifunc()
  run_wsgi_app(application)