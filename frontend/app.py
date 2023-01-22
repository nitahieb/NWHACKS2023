from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World?!</p>"

@app.route('/hello',methods=['GET','POST'])
def main():
    if request.method == 'POST':
        print("AAAAAAAAAAAAAA")
        print(request.form['fname']) 
    return render_template('main.html')

