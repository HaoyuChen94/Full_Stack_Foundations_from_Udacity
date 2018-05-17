#__auther__= 'Richard Chen Haoyu'

from flask import Flask
app = Flask(__name__)

# if route ending with given name, run def
# '/' Give chance to lead the default url to the page, not 404
@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

# run this py only on the running py
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)