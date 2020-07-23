from flask import *
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    r = subprocess.check_output(["gcloud", "auth", "application-default", "print-access-token"]).decode()
    return make_response(r, 200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
