from flask import Flask,render_template,request,jsonify,url_for,redirect
import sqlite3 

app=Flask(__name__)

@app.route("/")
def home():

    return "this is home page let changes revert"




connect = sqlite3.connect('database.db') 
connect.execute('''
    CREATE TABLE IF NOT EXISTS PARTICIPANTS (
        name TEXT, 
        email TEXT, 
        city TEXT, 
        country TEXT, 
        phone TEXT
    )
''')


@app.route("/index")
def index():
    return render_template('index.html')
@app.route('/form', methods=['GET', 'POST'])
def form():
    # if request.method == 'POST':
    #     # print(request.form)  # Debugging: print form data to the console
    #     name = request.form.get('name')  # Safely access form data
    #     email = request.form.get('email')
    #     return f"Hi {name}, defined till here! your email is {email}"
        
    return render_template('form.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # print(request.form)  # Debugging: print form data to the console
        name = request.form.get('name')  # Safely access form data
        email = request.form.get('email')
        return f"Hi {name}, defined till here! your email is {email}"
        
    return render_template('form.html')
@app.route('/mark/<int:mark>')
def mark(mark):
    res=""
    if mark>=50:
        passed="YES"
        res="you pass with " + str(mark)
    else:
        passed="NO"
        res="you fail with " + str(mark)
    return render_template('resul.html',results=res)
@app.route('/marked/<int:marked>')

def marked(marked):
    res=""
    passed=""
    if marked>=50:
        # passed="YES"
        res="you pass with " + str(marked)
    else:
        # passed="NO"
        res="you fail with " + str(marked)
    exp={'scr':marked, "res":res}
    return render_template('result.html', result=exp)
@app.route('/resultif/<int:result>')
def result(result):
    return render_template('resultif.html', res=result)
marks_dic={}
@app.route('/restab')
def restab():
    return render_template('/restab.html', marks=marks_dic)
@app.route('/submit1', methods=['GET', 'POST'])
def submit1():
    if request.method=='POST':
        
        name = request.form.get('name')  # Safely access form data
        Maths = request.form.get('Science')  # Safely access form data
        DS = request.form.get('ds')  # Safely access form data
        Stat = request.form.get('stat')  # Safely access form data
        total_marks= int(Maths) + int(DS) + int(Stat)
        Avg=total_marks / 3
        per= total_marks/300
        marks_dic['name']=name
        marks_dic['Maths']=Maths
        marks_dic['DS']=DS
        marks_dic['Stat']=Stat
        marks_dic['total_marks']=total_marks
        marks_dic['Avg']=Avg
        marks_dic['per']=per

        return redirect(url_for('restab'))
    
    return render_template('submit.html')
tasks =[
    {"id":1, "name":"Mani", "disc":"this is id 1"},
    {"id":2, "name":"kaval", "disc":"this is id 2"},
    {"id":3, "name":"Madip", "disc":"this is id 3"}


]
@app.route('/taskid/<int:id>',methods=['GET'])
def taskid(id):
    empl=next((empl for empl in tasks if empl["id"]==id),None)

    if empl is None:
        return jsonify({"error":"Employ Not Found"})
    return jsonify(empl)
@app.route('/taskid',methods=['POST'])
def taskid1():

    if not request.json or not 'name' in request.json:
        return jsonify({"error":"Employ Not Found"})
    new_empl={
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "name":request.json['name'],
        "disc":request.json['disc']
        }
    tasks.append(new_empl)
    return jsonify(tasks)
@app.route('/taskid/<int:id>',methods=['PUT'])
def taskid2(id):

    empl=next((empl for empl in tasks if empl["id"]==id),None)

    if empl is None:
        return jsonify({"error":"Employ Not Found"})
    empl['name']=request.json.get('name', empl['name'])
    empl['disc']=request.json.get('disc', empl['disc'])
    return jsonify(tasks)
@app.route('/taskid/<int:id>',methods=['DELETE'])
def taskid3(id):
    global tasks

    tasks=[task for task in tasks if task["id"] != id]

    return jsonify(tasks)


# @app.route('/participants') 
# def participants(): 
#     connect = sqlite3.connect('database.db') 
#     cursor = connect.cursor() 
#     cursor.execute('SELECT * FROM PARTICIPANTS') 
  
#     data = cursor.fetchall() 
#     return render_template("participants.html", data=data)
@app.route('/participants', methods=['GET', 'POST'])
def delete_participant():
    if request.method == 'POST':
        email = request.form['email']
        print(type(email))

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PARTICIPANTS WHERE email = ?", (email,))
            conn.commit()
        connect = sqlite3.connect('database.db') 
        cursor = connect.cursor() 
        cursor.execute('SELECT * FROM PARTICIPANTS') 
  
        data = cursor.fetchall() 
        # return render_template("participants.html", data=data)
        return render_template('participants.html',data=data, message="Participant deleted successfully.")
    else:
        connect = sqlite3.connect('database.db') 
        cursor = connect.cursor() 
        cursor.execute('SELECT * FROM PARTICIPANTS') 
  
        data = cursor.fetchall() 
        return render_template("participants.html", data=data)
@app.route('/deltest', methods=['POST'])
def delete_participant1():
    email = request.form['email']
    print(type(email))

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PARTICIPANTS WHERE email = ?", (email,))
        conn.commit()
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM PARTICIPANTS') 

    data = cursor.fetchall() 
    # return render_template("participants.html", data=data)
    return render_template('participants.html',data=data, message="Participant deleted successfully.")
    # if request.method == 'POST':
    #     data = request.get_json()
    #     email = data.get('email')
    #     print(type(email))

    #     with sqlite3.connect("database.db") as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("DELETE FROM PARTICIPANTS WHERE email = ?", (email,))
    #         conn.commit()
    #     connect = sqlite3.connect('database.db') 
    #     cursor = connect.cursor() 
    #     cursor.execute('SELECT * FROM PARTICIPANTS') 
  
    #     data = cursor.fetchall() 
    #     # return render_template("participants.html", data=data)
    #     return render_template('deltes.html',data=data, message="Participant deleted successfully.")
    # else:
    #     connect = sqlite3.connect('database.db') 
    #     cursor = connect.cursor() 
    #     cursor.execute('SELECT * FROM PARTICIPANTS') 
  
    #     data = cursor.fetchall() 
    #     return render_template("deltes.html", data=data)

@app.route('/join', methods=['POST']) 
def join(): 
    
    name = request.form['name'] 
    email = request.form['email'] 
    city = request.form['city'] 
    country = request.form['country'] 
    phone = request.form['phone'] 

    with sqlite3.connect("database.db") as users: 
        cursor = users.cursor() 
        cursor.execute(
            "INSERT INTO PARTICIPANTS (name, email, city, country, phone) VALUES (?, ?, ?, ?, ?)",
            (name, email, city, country, phone)
        )
        users.commit()
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM PARTICIPANTS') 

    data = cursor.fetchall()
    return redirect("/participants")
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
