import webapp2
import jinja2
import os
import Models

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def generate_files_html(self):
    files = db.GqlQuery("SELECT * "
                            "FROM File ")

    
    html = ""
    for file in files:
        html += """
            <tr>
                <td>"""+str(file.upload_date)+"""</td>
                <td>"""+file.title+"""</td>
                <td>"""+file.description+"""</td>
                <td>View</td>
            </tr>
        """
    return html

class Files(webapp2.RequestHandler):
    def get(self):
        
        #set stylesheets needed per page 
        specific_urls = """
            <link type="text/css" rel="stylesheet" href="/stylesheets/""" + self.__class__.__name__ + """.css" />
            <script type="text/javascript" src="https://www.google.com/jsapi"></script>
            <script type="text/javascript">
              google.load("visualization", "1", {packages:["corechart"]});
              google.setOnLoadCallback(drawChart);
              function drawChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Year', 'Net', 'Tax'],
                  ['2004', 360, 40],
                  ['2005', 200, 20],
                  ['2006', 360, 40],
                  ['2007', 400, 33]
                ]);
        
                var options = {
                  title: 'Income Breakdown'
                };
        
                var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
                chart.draw(data, options);
              }
            </script>
        """
        
        files_template_values = {
            'files': generate_files_html(self)
        }
            
        template = jinja_environment.get_template('Page_Content/files.html')
        files_template = template.render(files_template_values)
        
        
        if users.get_current_user():
            myFile = open('Page_Content/files.html', 'r')
            
            
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
                'content':files_template
            }
           
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.response.out.write("works")

app = webapp2.WSGIApplication([('/files', Files)], debug=True)