import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Charts_TenDollarData import create_app
# from flask_compress import Compress
import newrelic.agent
newrelic.agent.initialize('newrelic.ini', 'staging')
import logging
import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.contrib.profiler import ProfilerMiddleware

# or configure to use ELASTIC_APM in your application's settings
import elasticapm
from elasticapm.contrib.flask import ElasticAPM

# sentry_sdk.init(
#     dsn="https://ef2188dd9d284bb295241f1e22ad9b2d@o497156.ingest.sentry.io/5582464",
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )
app = create_app()

# app.config['ELASTIC_APM'] = {
# 	'SERVICE_NAME': 'chartsonlygoup_apm',
# 	'DEBUG': True,
# 	'SERVER_URL': 'http://localhost:8200',
# 	'TRACES_SEND_FREQ': 5,
# 	'FLUSH_INTERVAL': 1, # 2.x
# 	'MAX_QUEUE_SIZE': 1, # 2.x
# 	'TRANSACTIONS_IGNORE_PATTERNS': ['.*healthcheck']
# }
# apm = ElasticAPM(app, logging=True)

# @elasticapm.capture_span()
# def foo():
#     return "foo"


if __name__ == '__main__':
	# http.serve_forever()
	# app.config['PROFILE'] = True
	# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
	

    # app.run(debug=True, EXPLAIN_TEMPLATE_LOADING=true, port=5001, threaded=True)
    # app.run(debug=True)
    # app.run()
    app.run(debug=True,host='0.0.0.0')