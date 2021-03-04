from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.router import Router
from pyramid.view import view_config
from wsgiref.simple_server import make_server

import os

# data models ######################################
class Project:
    """ Project object stored in the database"""
    def __init__(self, name, creator, industries):
        self.name = name
        self.creator = creator
        self.industries = industries

class Industry: 
    """ Industry object stored in database"""
    def __init__(self, name):
        self.name = name

# examples that could be in the database ########
project_object = Project(
    "Test 01", "Elizabeth Johnson", [
        vars(Industry("Cosmetics")), vars(Industry("Technology"))
        ]
    )

PROJECT_LIST = [
  vars(project_object)
]

# views ########################################
@view_config(route_name="projects", renderer="json", request_method="GET", openapi=True)
def get(request):
    """ Returns the Projects List (should be from database)"""
    print("Trying to get projects...")
    return PROJECT_LIST


@view_config(route_name="projects", renderer="json", request_method="POST", openapi=True)
def post(request):
    """ Adds a new Project (should be to the database)"""
    project_object = Project(
        request.openapi_validated.body["name"], 
        request.openapi_validated.body["creator"], 
        request.openapi_validated.body["industries"]
        )
    PROJECT_LIST.append(project_object)
    return "Project added."


# create main Pyramid application #############
def main_app():
    config = Configurator()
    config.include("pyramid_openapi3")
    config.add_static_view(name="spec", path="spec")
    config.pyramid_openapi3_spec_directory(
        os.path.join(os.path.dirname(__file__), 
        "SimpleOpenAPISpecificationv3.yaml"),
    )
    config.pyramid_openapi3_add_explorer()
    config.add_route("projects", "/projects") # you can specify lots of routes in the routes.py file
    config.scan(".")

    return config.make_wsgi_app()

# make a little server #########################
if __name__ == "__main__":
    """If app.py is called directly, start up the app."""
    print("Swagger UI available at http://0.0.0.0:6543/docs/")  # noqa: T001
    server = make_server("0.0.0.0", 6543, main_app())
    server.serve_forever()