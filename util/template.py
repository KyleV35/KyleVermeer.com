import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("views"))