import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, file_key):
        
        if not blobstore.get(file_key):
            self.error(404)
        else:
            self.send_blob(file_key)

app = webapp2.WSGIApplication([('/view_file/([^/]+)?', ServeHandler)
                                     ], debug=True)

