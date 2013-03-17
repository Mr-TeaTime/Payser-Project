import webapp2
from google.appengine.api import users
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Dashboard(webapp2.RequestHandler):
    def get(self):
        
        user = users.get_current_user() 
        if user:
            
            #set stylesheets needed per page 
            specific_urls = """
                <link type="text/css" rel="stylesheet" href="/stylesheets/""" + self.__class__.__name__ + """.css" />
            """
            
            dashboard_template_values = {
                'nickname': user.nickname(),
                'email': user.email()
            }
            
            template = jinja_environment.get_template('Page_Content/dashboard.html')
            dashboard_template = template.render(dashboard_template_values)
            
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
                'content': dashboard_template
            }
           
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.response.out.write("works")

app = webapp2.WSGIApplication([('/dashboard', Dashboard)], debug=True)
