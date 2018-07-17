class RestApi(object):
    def __init__(self, app=None):
        self._routes = {}
        self._schemas = {}

        self.app = None
        self.blueprint = None

        if app is not None:
            self.app = app
            self.init_app(app)

    # -----------------------------------------------------------------------------------
    # Flask Extension Initialization
    # -----------------------------------------------------------------------------------

    def init_app(self, app):
        # If app is a blueprint, defer initialization
        try:
            app.record(self._deferred_blueprint_init)
        # Flask.Blueprint has a 'record' attribute, Flask.Api does not
        except AttributeError:
            self._init_app(app)
        else:
            self.blueprint = app

    def _init_app(self, app):
        pass

    def _deferred_blueprint_init(self):
        pass

    # -----------------------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------------------

    @property
    def routes(self):
        return self._routes.values()

    @property
    def schemas(self):
        return self._schemas.values()

    # -----------------------------------------------------------------------------------
    # Class Methods
    # -----------------------------------------------------------------------------------

    def add_route(self, callback, url):
        if self._routes[url]:
            raise KeyError('Trying to Map Two Route Handlers to One Path')

        self._routes[url] = callback

    def add_schema(self, schema, name):
        if self._schemas[name]:
            raise KeyError('Trying to Map Two Route Handlers to One Path')

        self._schemas[name] = schema

    # -----------------------------------------------------------------------------------
    # API Decorators (wrapping class methods)
    # -----------------------------------------------------------------------------------

    def route(self, url):
        def wrapper(callback):
            self.add_route(callback, url)
            return callback

        return wrapper

    def schema(self, name=None):
        def wrapper(cls):
            self.add_schema(cls, cls.__name__ if name else name)
            return cls

        return wrapper
