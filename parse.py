# Give me a feed url, and I'll attempt to parse it for you and give you JSON
# usage: /parse?url=http://example.com/feed
# dependencies: python 2.6+, feedparser, and web.py

import time
import web
import json
import feedparser

def to_json(python_object):
  if isinstance(python_object, time.struct_time):
    return {'__class__': 'time.asctime',
            '__value__': time.asctime(python_object)}
  raise TypeError(repr(python_object) + ' is not JSON serializable')

urls = (
  '/parse', 'Parser'
)
app = web.application(urls, globals())

class Parser:
  def GET(self):
    web.header('Content-Type', 'application/json')
    try:
      url = web.input().url
      print "Attempting to parse: %s" % url
      return json.dumps(feedparser.parse(url), default=to_json)
    except Exception as e:
      print e
      web.ctx.status = "400 Bad Request"
      return json.dumps({"message": "Sorry, i couldn't parse that feed."})

if __name__ == "__main__":
  app.run()