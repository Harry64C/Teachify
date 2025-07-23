from flask import Flask, render_template, url_for
from socket import gethostname

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('example.html')


if __name__ == '__main__':
    ## db.create_all()
    if 'liveconsole' not in gethostname():
        app.run()