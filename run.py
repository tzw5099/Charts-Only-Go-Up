import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Charts_TenDollarData import create_app
# from flask_compress import Compress


import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.contrib.profiler import ProfilerMiddleware
sentry_sdk.init(
    dsn="https://ef2188dd9d284bb295241f1e22ad9b2d@o497156.ingest.sentry.io/5582464",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
app = create_app()
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

# flask sometimes gets stuck
# https://stackoverflow.com/questions/13333684/flask-app-occasionally-hanging
# https://stackoverflow.com/questions/11150343/slow-requests-on-local-flask-server

# use gevent WSGI server instead of the Flask
# instead of 5000, you can define whatever port you want.
# http = WSGIServer(('', 5001), app.wsgi_app)



if __name__ == '__main__':
	# http.serve_forever()
    # app.run(debug=True, EXPLAIN_TEMPLATE_LOADING=true, port=5001, threaded=True)
    # app.run(debug=True)
    # app.run()
    app.run(debug=True,host='0.0.0.0')