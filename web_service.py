from tg import AppConfig, TGController
from tg import expose

TIMELINE_FILE = "data/timeline.json"
CLUSTERS_FILE = "data/clusters.json"
FORCE_FILE = "data/force.json"


class RootController(TGController):
    @expose('jinja:index.html')
    def index(self, **kw):
        return dict()

    #Here we tell to TurboGears to get the result provided
    #by our controller method and encode it as JSON so
    #that we can load it back using d3.json from javascript
    @expose('json:', content_type='application/json')
    def timeline(self, **kw):
        f = open(TIMELINE_FILE)
        yield f.read()

    @expose('json:', content_type='application/json')
    def clusters(self, **kw):
        f = open(CLUSTERS_FILE)
        yield f.read()

    @expose('json:', content_type='application/json')
    def force(self, **kw):
        f = open(FORCE_FILE)
        yield f.read()

config = AppConfig(minimal=True, root_controller=RootController())

#Only change since before is that we register the 'json' renderer
#into our list of available renderers, so that we are able to
#encode our responses as JSON
config.renderers = ['json', 'jinja']
config.default_renderer = 'jinja'

config.serve_static = True
config['paths']['static_files'] = './'

from wsgiref.simple_server import make_server
print "Serving on port 8080..."
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()
