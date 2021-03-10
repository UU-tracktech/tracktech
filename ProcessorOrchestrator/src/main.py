import json
import swagger_ui
from apispec.exceptions import APISpecError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado.web import RequestHandler
from client import ClientSocket, ClientTracking
from processor import ProcessorSocket, ProcessorFeatureMap
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.tornado import TornadoPlugin

define('port', default=8000, help='port to listen on')


def main():
    handlers = [
        ('/', HelloWorld),
        ('/client', ClientSocket),
        ('/client/tracking', ClientTracking),
        ('/processor', ProcessorSocket),
        ('/processor/features', ProcessorFeatureMap)
    ]

    # Construct and serve the tornado application.
    app = Application(handlers)

    gen_swagger(handlers, app)

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


def gen_swagger(handlers, app):
    # Configure swagger spec
    spec = APISpec(
        title="Processor Orchestrator Api",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="Documentation Processor Orchestrator API"),
        plugins=[TornadoPlugin(), MarshmallowPlugin()],
        servers=[
            {"url": "http://localhost:8000/", "description": "Local environment", },
        ],
    )

    # Interpret handler docfiles
    for handler in handlers:
        try:
            if hasattr(handler[1], "tagDescription"):
                spec.tag(handler[1].tagDescription)
            spec.path(urlspec=handler)
        except APISpecError:
            pass

    # Write the Swagger file into specified location.
    with open("swagger.json", "w", encoding="utf-8") as file:
        json.dump(spec.to_dict(), file, ensure_ascii=False, indent=4)

    # Start the Swagger UI
    swagger_ui.tornado_api_doc(
        app,
        config_path="./swagger.json",
        url_prefix="/swagger/spec.html",
        title="Processor Orchestrator API",
    )


class HelloWorld(RequestHandler):
    tagDescription = dict(name="Hello world", description="Landing page for the app")

    def get(self):
        """Simple Hello world example"
        ---
        tags: [Hello world]
        summary: Simple hello world landing page
        description: Echoes hello world to the user
        responses:
            200:
                description: OK
                content:
                    text/plain:
                        schema:
                            type: string
                            example: pong
        """
        self.write("Hello World")


if __name__ == "__main__":
    main()
