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
# mysql 초기화
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write', methods=['GET','POST'])
def write():
    if request.method == 'POST':
        # 넘어온 값을 받아서 insert
        title = request.form['title']
        content = request.form['content']
        writer = request.form['writer']
        pwd = request.form['pwd']
        sql = "insert into board(title, content, writer, pwd) values(%s, %s, %s, %s)"
        data = (title, content, writer, pwd)
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        conn.close()
        # return '저장성공'
        return redirect('/list')
    else:
        return render_template('writeform.html')

@app.route('/list')
def list():
    conn = mysql.connect()
    cur = conn.cursor()
    sql = "select * from board order by num desc"
    cur.execute(sql)
    lists = cur.fetchall()
    print('lists ==', lists)
    return render_template('list.html', lists=lists)

@app.route('/read/<int:num>')
def read(num):
    #조회수 증가코드
    sql_update = "UPDATE board SET hit=hit+1 where num=%s"
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql_update, num)
    conn.commit()
    sql = "SELECT * FROM board WHERE num=%s"
    cur.execute(sql, num)
    b = cur.fetchone()
    conn.close()
    return render_template('read.html', b=b)

@app.route('/update/<int:num>')
def updateform(num):
    print('update num===', num)
    # 업데이트 할 글을 읽어서 updateform.html에 넘긴다.
    sql = "SELECT * FROM board WHERE num=%s"
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql, num)
    b = cur.fetchone()
    conn.close()
    return render_template('updateform.html', b=b)

@app.route('/update', methods=['POST'])
def update():
    num = request.form['num']
    title = request.form['title']
    content = request.form['content']
    writer = request.form['writer']
    pwd = request.form['pwd']
    sql = '''
        UPDATE board SET title=%s, content=%s, writer=%s
        WHERE num=%s AND pwd=%s
    '''
    datas = (title, content, writer, num, pwd)
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql, datas)
    conn.commit()
    conn.close()
    return redirect('/list')

@app.route('/delete/<int:num>')
def deleteform(num):
    return render_template('deleteform.html',num=num)

@app.route('/delete', methods=['POST'])
def delete():
    # 글번호와 비밀번호를 받아서 삭제(DELETE) 후 리스트로 간다
    num = request.form['num']
    pwd = request.form['pwd']
    sql = "DELETE FROM board WHERE num=%s AND pwd=%s"
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql, (num, pwd))
    
    conn.commit()
    conn.close()
    return redirect('/list')

if __name__ == '__main__':
    app.run(debug=True)