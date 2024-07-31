from django.db import connection
from flask import Flask, jsonify

import sqlite3

##### True Positives #########
def fetch_name_0(request):
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute("SELECT * FROM users WHERE username = '%s'" % request.GET.get('baz'))
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute(f"SELECT foo FROM bar WHERE baz = {request.GET.get('baz')}")
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute("SELECT foo FROM bar WHERE baz = %s" % request.GET.get('baz'))
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute("SELECT foo FROM bar WHERE baz = %s".format(request.GET.get('baz')))
      bad = request.GET.get('baz')
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute(f"SELECT foo FROM bar WHERE baz = {bad}")
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.executemany(f"SELECT foo FROM bar WHERE baz = {bad}")
      stillbad = "SELECT foo FROM bar WHERE baz = " + request.GET.get('baz')
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute(stillbad)
      query = request.GET['q']
      sql = f"SELECT * FROM some_table WHERE title LIKE '%{query}%';"
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute(sql)
      # ok: taint-backend-sqli-generic-cursor
      cursor.execute(
        "SELECT * FROM some_table WHERE title LIKE '%?%'",
        [request.GET['q']]
      )
      row = cursor.fetchone()
  return row

def fetch_name_1(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute(f"UPDATE bar SET foo = 1 WHERE baz = {baz}")
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute(f"SELECT foo FROM bar WHERE baz = {baz}")
      row = cursor.fetchone()
  return row

def fetch_name_2(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute("SELECT foo FROM bar WHERE baz = %s" % baz)
      row = cursor.fetchall()
  return row

def fetch_name_3(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-generic-cursor
      cursor.execute("SELECT foo FROM bar WHERE baz = %s".format(baz))
      row = cursor.fetchone()
  return row

def execute_many(request):
  items = get_items(request)
  
  
  q = f""" select ignore into TABLE1 (
          Item_Name, Item_Price, Item_In_Stock, Item_Max, Observation_Date, Time ) 
          values (%s,%s,%s,%s,%s, {request.GET.get("time")})           
      """
  
  with connection.cursor() as cursor:
    try:
        # ruleid: taint-backend-sqli-generic-cursor
        cursor.executemany(q, items)
        connection.commit()
    except:
        connection.rollback()

def execute_many2(request):
  items = get_items(request)
  
  
  q = f""" select ignore into TABLE1 (
          Item_Name, Item_Price, Item_In_Stock, Item_Max, Observation_Date, Time ) 
          values (%s,%s,%s,%s,%s, {request.GET.get("time")})           
      """
  
  with connection.cursor() as cursor:
    try:
        # ruleid: taint-backend-sqli-generic-cursor
        cursor.executemany(q, items)
    except:
        connection.rollback()
    connection.commit()

def upload(request, project_id):

    if request.method == 'POST':

        proj = Project.objects.get(pk=project_id)
        form = ProjectFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = request.POST.get('name', False)
            upload_path = store_uploaded_file(name, request.FILES['file'])

            other_name = "{}".format(name)
            curs = connection.cursor()
            curs.execute(
                # todoruleid: taint-backend-sqli-generic-cursor
                "insert into taskManager_file ('name','path','project_id') values ('%s','%s',%s)" %
                (other_name, upload_path, project_id))

def fetch_name_4(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # tudoruleid: taint-backend-sqli-generic-cursor
      cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s" % baz)

def show_user(request):
  with connection.cursor() as cursor:
    # BAD -- Using string formatting
    # Issue with the taint rules it seems.
    # ruleid: taint-backend-sqli-generic-cursor
    cursor.execute("SELECT * FROM users WHERE username = '%s'" % request.POST["username"])
    user = cursor.fetchone()

    # GOOD -- Using parameters
    # ok: taint-backend-sqli-generic-cursor
    cursor.execute("SELECT * FROM users WHERE username = %s", request.POST["username"])
    user = cursor.fetchone()

    # BAD -- Manually quoting placeholder (%s)
    # todoruleid: taint-backend-sqli-generic-cursor
    cursor.execute("SELECT * FROM users WHERE username = '%s'", request.POST["username"])
    user = cursor.fetchone()

def other(request):
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST.get('name', False)
            upload_path = store_uploaded_file(name, request.FILES['file'])

            other_name = "{}".format(name)
            connection.cursor().execute(
                # ruleid: taint-backend-sqli-generic-cursor
                "insert into taskManager_file ('name','path','project_id') values ('%s','%s',%s)" %
                (other_name, upload_path, project_id))
            return connection.cursor().fetchall()



app = Flask(__name__)
# This test is from
# https://github.com/anil-yelken/Vulnerable-Flask-App/blob/main/vulnerable-flask-app.py#L16-L26
@app.route("/user/<string:name>")
def search_user(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    # ruleid: taint-backend-sqli-generic-cursor
    cur.execute("select * from test where username = '%s'" % name)
    data = str(cur.fetchall())
    con.close()
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data=data),200
