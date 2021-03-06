#guest2.py
#pip install flask-mysql
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
import pymysql

mysql = MySQL(cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config.from_object(__name__)

mysql.init_app(app)

@app.route('/')
def index():
    print('/ 경로로 요청됨!')
    return render_template('index.html')




@app.route('/write', methods=['GET','POST'])
def write():
    if request.method == 'POST':
         #넘어온 값들을 받아서 guest 테이블에 INSERT한다.
        writer = request.form['writer']
        title = request.form['title']
        content = request.form['content']
        vals = (writer, title, content)
        sql = "INSERT INTO guest(writer, title, content) VALUES(%s, %s, %s)"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, vals)
        conn.commit()
        conn.close()
        return redirect('/list')
    else:
        return render_template('writeform.html')

@app.route('/list')
def list():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM guest order by no desc"
    cursor.execute(sql)
    guests = cursor.fetchall()
    print('guests====', guests)
    return render_template('list.html', guests=guests)

if __name__ == '__main__':
    app.run(debug=True)

# CREATE TABLE guest(
# 	no INT PRIMARY KEY auto_increment,
# 	writer VARCHAR(10) NOT NULL,
# 	title VARCHAR(30) NOT NULL,
# 	content VARCHAR(2000) NOT NULL,
# 	regdate DATETIME DEFAULT CURRENT_TIMESTAMP
# );