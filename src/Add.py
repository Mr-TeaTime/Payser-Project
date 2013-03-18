import webapp2
import jinja2
import os
import string
import datetime

from google.appengine.api import users
from google.appengine.ext import db


import Models


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Add(webapp2.RequestHandler):
    def get(self):
        
        user = users.get_current_user() 
        if user:
            #set stylesheets needed per page 
            specific_urls = """
                <link type="text/css" rel="stylesheet" href="/stylesheets/""" + self.__class__.__name__ + """.css" />
                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
                <script>
                    $(document).ready(function()
                    {
                        $("#file-info").hide();
                    });
                    $(document).ready(function()
                    {
                        $("#type-selector").change(function() {
                            if ($(this).val() == "payslip"){
                                $("#payslip-info").show();
                                $("#file-info").hide();
                            }
                            if( $(this).val() == "other"){
                                $("#payslip-info").hide();
                                $("#file-info").show();
                            }
                        });
                    });
                </script>

            """
            
            
            #add the page query to the html
            url = self.request.url
            url = string.split(url, '/')
            Add_template_values = {
                'page': url[len(url) - 1]
            }
            
            template = jinja_environment.get_template('Page_Content/add.html')
            Add_template = template.render(Add_template_values)
            
            url = users.create_logout_url(self.request.uri)
            nav = """
            <nav>
                <ul>
                    <li><a href="/dashboard">Dashboard</a></li>
                    <li><a href="#">Design</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="%s">Logout</a></li>
                </ul>
            </nav>
            """ % url
           
                
            template_values = {
                'specific_urls':specific_urls,
                'nav': nav,
                'content': Add_template
            }
           
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        data = AForm(data=self.request.POST)
        if data.is_valid():
            self.response.out.write("added <br />")
            user = get_current_user()
        
            if self.request.POST['type'] == "payslip":
                 self.response.out.write("payslip <br />")
                
            else:
                 self.response.out.write("other <br />")
        else:
             self.response.out.write("not added <br />")

app = webapp2.WSGIApplication([('/add', Add)], debug=True)