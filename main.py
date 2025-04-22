from flask import Flask


app = Flask(__name__)
with open('secret_key/secret_key.txt', 'r') as f:
    app.config['SECRET_KEY'] = f.read()


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'Home'


if __name__ == '__main__':
    app.run(port='8080', host='127.0.0.1')