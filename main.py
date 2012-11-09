#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
from urls import routes
from util.template import jinja_environment

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

app = webapp2.WSGIApplication(routes,
                              debug=True)

def handle_404(request, response, exception):
    logging.error(exception)
    template = jinja_environment.get_template('404Page.html')
    response.out.write(template.render({}))
    response.set_status(404)
    
def handle_500(request, response, exception):
    logging.error(exception)
    template = jinja_environment.get_template('500Page.html')
    response.out.write(template.render({}))
    response.set_status(500)

if (app.debug==False) :    
    app.error_handlers[404]= handle_404
    app.error_handlers[500]= handle_500