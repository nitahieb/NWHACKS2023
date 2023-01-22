from flask import Flask, render_template, request, url_for, redirect, session
from .project import print_directions, gmaps, returninfo, level1, level2, level3
from datetime import datetime
import pickle
import sys


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        length = request.form.get("length")
        difficulty = request.form.get("difficulty")
        location = request.form.get("location")
        session['length'] = length
        session['difficulty'] = difficulty
        session['location'] = location
        return redirect(url_for('directions'))

        
       

    return render_template('index.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        length = request.form.get("time")
        difficulty = request.form.get("difficulty")
        location = request.form.get("location")
        coords = gmaps.geocode(location)[0]['geometry']['viewport']['northeast']
        data = (coords["lat"],coords["lng"],length)
        if difficulty=="Relaxed":
            level1.append(data)
            file1 = open('level1', 'wb')
            pickle.dump(level1, file1)
            file1.close()
        elif difficulty == "Active":
            level2.append(data)
            file2 = open('level2', 'wb')
            pickle.dump(level2, file2)
            file2.close()
        elif difficulty == "Intense":
            level3.append(data)
            file3 = open('level3', 'wb')
            pickle.dump(level3, file3)
            file3.close()

        
        
    

    return render_template('signup.html')

@app.route("/directions")
def directions():
    data = returninfo(session['difficulty'],session['location'], session['length'])

    return render_template('directions.html',dataToRender=data)

@app.route("/about")
def about():
    return render_template('about.html')




# @app.route("/directions")
# def directions():



# @app.route('/hello',methods=['GET','POST'])
# def main():
#     if request.method == 'POST':
#         if request.form['fname']:
#             now = datetime.now()
#             directions_result = gmaps.directions("UBC bus loop",
#                                      "1333 E.55th ave, vancouver BC, canada",
#                                      mode="transit",
#                                      departure_time=now)
#             session['directions'] = print_directions(directions_result,[])
#             return redirect(url_for('maps',num=1))
#             #return profile(request.form['fname'])
#         print(request.form['fname']) 

    return render_template('main.html')
@app.route('/maps')
def maps():
    num = request.args['num']
    directions = session['directions']
    #print(url_for('maps', num=2))
    return f'{directions}\'s profile'


