import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Charts_TenDollarData import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, EXPLAIN_TEMPLATE_LOADING=true, port=5001)