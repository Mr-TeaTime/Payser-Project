import webapp2
import jinja2
import os
import Models

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def generate_payslip_html(self):
    payslips = db.GqlQuery("SELECT * "
                            "FROM Payslip "
                            "WHERE ANCESTOR IS :1 ",
                            Models.payslip_key(users.get_current_user().user_id()))
    
    html = ""
    for payslip in payslips:
        html += """
            <tr>
                <td>"""+str(payslip.upload_date)+"""</td>
                <td>"""+payslip.company+"""</td>
                <td>"""+str(payslip.beginning)+"""</td>
                <td>"""+str(payslip.ending)+"""</td>
                <td>"""+str(payslip.income)+"""</td>
                <td>"""+str(payslip.tax)+"""</td>
                <td>"""+str(payslip.net)+"""</td>
                <td>View</td>
            </tr>
        """
    return html

class Payslips(webapp2.RequestHandler):
    def get(self):
        
        payslips = db.GqlQuery("SELECT * "
                            "FROM Payslip "
                            "WHERE ANCESTOR IS :1 ",
                            Models.payslip_key(users.get_current_user().user_id()))
        
        list1 = [0,0,0,0]
        list2 = [0,0,0,0]
        
        index = 0
        for payslip in payslips:
            
            list1[index] = payslip.income
            list2[index] = payslip.tax
            index += 1
        
        #set stylesheets needed per page 
        specific_urls = """
            <link type="text/css" rel="stylesheet" href="/stylesheets/""" + self.__class__.__name__ + """.css" />
            <script type="text/javascript" src="https://www.google.com/jsapi"></script>
           <script type="text/javascript">
              google.load("visualization", "1", {packages:["corechart"]});
              google.setOnLoadCallback(drawChart);
              function drawChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Payslip', 'Income', 'Tax'],
                  ['1',  """+str(list1[0])+""",      """+str(list2[0])+"""],
                  ['2',  """+str(list1[1])+""",      """+str(list2[1])+"""],
                  ['3',  """+str(list1[2])+""",      """+str(list2[2])+"""],
                  ['4',  """+str(list1[3])+""",      """+str(list2[3])+"""]
                ]);
        
                var options = {
                  title: 'Income Breakdown',

                };
        
                var chart = new google.visualization.AreaChart(document.getElementById('chart-div'));
                chart.draw(data, options);
              }
            </script>
        """
        payslip_template_values = {
            'payslips': generate_payslip_html(self)
        }
            
        template = jinja_environment.get_template('Page_Content/payslips.html')
        payslip_template = template.render(payslip_template_values)
        
        if users.get_current_user():
            myFile = open('Page_Content/payslips.html', 'r')
            
            
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
                'content': payslip_template
            }
           
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.response.out.write("works")
        
app = webapp2.WSGIApplication([('/payslips', Payslips)], debug=True)