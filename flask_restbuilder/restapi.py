from flask import Blueprint, render_template, jsonify
from apispec import APISpec
from apispec.ext.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin


class RestApi(object):
    def __init__(self, app=None, title='Sample API', version='0.1.0'):
        self._spec = APISpec(title=title, version=version,
                             openapi_version='2.0',
                             plugins=(FlaskPlugin(), MarshmallowPlugin()))
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

    def swagger_json(self):
        return jsonify(self.generate_spec().to_dict())

    def swagger_ui(self):
        """ Render a SwaggerUI for a given API """
        return render_template('swagger-ui.html')

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
        spec_blueprint = Blueprint(
            'flask-restbuilder', __name__,
            static_folder='./static',
            template_folder='./templates',
            static_url_path='/flask-restbuilder/static',
        )

        json_url = self.app.config.get('APISPEC_SWAGGER_URL', '/swagger/')
        if json_url:
            spec_blueprint.add_url_rule(json_url, 'swagger-json', self.swagger_json)

        ui_url = self.app.config.get('APISPEC_SWAGGER_UI_URL', '/swagger-ui/')
        if ui_url:
            spec_blueprint.add_url_rule(ui_url, 'swagger-ui', self.swagger_ui)

        app.register_blueprint(spec_blueprint)

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
        if getattr(self._routes, url, None):
            raise KeyError('Trying to Map Two Route Handlers to One Path')
        self._routes[url] = callback

    def add_schema(self, schema, name):
        if getattr(self._schemas, name, None):
            raise KeyError('Trying to Map Two Route Handlers to One Path')
        self._schemas[name] = schema

    def generate_spec(self):
        for name, schema in self._schemas.items():
            self._spec.definition(name, schema=schema)

        with self.app.test_request_context():
            for _, callback in self._routes.items():
                self._spec.add_path(view=callback)

        return self._spec

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
            self.add_schema(cls, cls.__name__ if not name else name)
            return cls
        return wrapper
