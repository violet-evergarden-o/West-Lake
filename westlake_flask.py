from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'



def get_db():
    db=getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#the home page
@app.route("/")
def home():
    cursor = get_db().cursor()
    #get the right homepage pics
    sql = "SELECT*FROM image where homepagePic = 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("index.html", images=results)

#the image page
@app.route('/image/<int:id>',methods = ['GET','POST'])
def image(id):
    cursor = get_db().cursor()
    #get all data in image table with id
    sql = 'SELECT*FROM image where id = ?'
    cursor.execute(sql,(id,))
    results = cursor.fetchone()
    cursor = get_db().cursor()
    #get the comments with location id
    sql = 'SElECT*FROM comment where location_id = ?'
    cursor.execute(sql,(id,))
    comments= cursor.fetchall()
    cursor = get_db().cursor()
    #get the images with location id 
    sql = 'SELECT*FROM image where location_id = ?'
    cursor.execute(sql,(id,))
    location = cursor.fetchall()
    return render_template('image.html', item=results, comments=comments, location=location)


if __name__=="__main__":
    app.run(debug=True)














