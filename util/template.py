import jinja2
import os
from urllib import quote_plus

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("views"))
jinja_environment.globals['urlencode']= quote_plus