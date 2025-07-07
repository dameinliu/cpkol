from dotenv import load_dotenv
load_dotenv()

from app import create_app
import os
import sys

try:
    app = create_app()

    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(debug=True, host="0.0.0.0", port=port)
except Exception as e:
    print("Flask app failed to start:", e, file=sys.stderr)
    raise