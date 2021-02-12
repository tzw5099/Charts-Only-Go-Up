import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Charts_TenDollarData import create_app
# from flask_compress import Compress

import logging
import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.contrib.profiler import ProfilerMiddleware
sentry_sdk.init(
    dsn="https://ef2188dd9d284bb295241f1e22ad9b2d@o497156.ingest.sentry.io/5582464",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
# import elasticapm
# from elasticapm.contrib.flask import ElasticAPM


app = create_app()

# app.config['ELASTIC_APM'] = {
# 	# Set required service name. Allowed characters:
# 	# a-z, A-Z, 0-9, -, _, and space
# 	'SERVICE_NAME': 'chartsonlygoup_apm',

# 	# Use if APM Server requires a token
# 	# 'SECRET_TOKEN': '',

# 	# https://gist.github.com/graphaelli/d9cb1c59bc1a78459650c9882382c2fb
# 	# Set custom APM Server URL (default: http://localhost:8200)
# 	# 'SERVER_URL': '',
# 	'DEBUG': True,
# 	'SERVER_URL': 'http://localhost:8200',
# 	'TRACES_SEND_FREQ': 5,
# 	# 'SERVICE_NAME': 'flaskapp',
# 	'FLUSH_INTERVAL': 1, # 2.x
# 	'MAX_QUEUE_SIZE': 1, # 2.x
# 	'TRANSACTIONS_IGNORE_PATTERNS': ['.*healthcheck']
# }

# # apm = ElasticAPM(app, logging=logging.ERROR)
# apm = ElasticAPM(app, logging=True)

# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

# flask sometimes gets stuck
# https://stackoverflow.com/questions/13333684/flask-app-occasionally-hanging
# https://stackoverflow.com/questions/11150343/slow-requests-on-local-flask-server

# use gevent WSGI server instead of the Flask
# instead of 5000, you can define whatever port you want.
# http = WSGIServer(('', 5001), app.wsgi_app)
# @elasticapm.capture_span()
def foo():
    return "foo"
# print("http://dddataverse:8420/aapl#/")
if __name__ == '__main__':
	# http.serve_forever()
    # app.run(debug=True, EXPLAIN_TEMPLATE_LOADING=true, port=5001, threaded=True)
    # app.run(debug=True)
    # app.run()
    # apm = ElasticAPM(app)
	# server = Server(app.run(debug=True,host='0.0.0.0', port=8420))
    # server.serve()
    app.run(debug=True,host='0.0.0.0', port=8420, threaded=True)