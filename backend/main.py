from dotenv import load_dotenv
load_dotenv()

from app import create_app
import os
import sys

try:
    app = create_app(config_name='default')

    if __name__ == '__main__':
        # python main.py 5000才会走到这里，否则会走__init__.py
        app.run(debug=True, host="0.0.0.0", port=os.environ.get('PORT', 5000))
except Exception as e:
    print("Flask app failed to start:", e, file=sys.stderr)
    raise