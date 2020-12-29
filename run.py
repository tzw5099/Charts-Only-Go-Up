import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Charts_TenDollarData import create_app
# from flask_compress import Compress

app = create_app()
# flask sometimes gets stuck
# https://stackoverflow.com/questions/13333684/flask-app-occasionally-hanging
# https://stackoverflow.com/questions/11150343/slow-requests-on-local-flask-server

# use gevent WSGI server instead of the Flask
# instead of 5000, you can define whatever port you want.
# http = WSGIServer(('', 5001), app.wsgi_app) 



if __name__ == '__main__':
	# http.serve_forever()
    app.run(debug=True, EXPLAIN_TEMPLATE_LOADING=true, port=5001, threaded=True)