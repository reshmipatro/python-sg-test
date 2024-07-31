from django.db import connection
import django.http import HttpResponse

##### True Positives #########
def fetch_name_0(request):
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute("SELECT * FROM users WHERE username = '%s'" % request.GET.get('baz'))
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute(f"SELECT foo FROM bar WHERE baz = {request.GET.get('baz')}")
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute("SELECT foo FROM bar WHERE baz = %s" % request.GET.get('baz'))
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute("SELECT foo FROM bar WHERE baz = %s".format(request.GET.get('baz')))
      bad = request.GET.get('baz')
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute(f"SELECT foo FROM bar WHERE baz = {bad}")
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.executemany(f"SELECT foo FROM bar WHERE baz = {bad}", lol)
      stillbad = "SELECT foo FROM bar WHERE baz = " + request.GET.get('baz')
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute(stillbad)
      query = request.GET['q']
      sql = f"SELECT * FROM some_table WHERE title LIKE '%{query}%';"
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute(sql)
      # ok: taint-backend-sqli-cursor-execute
      cursor.execute(
        "SELECT * FROM some_table WHERE title LIKE '%?%'",
        [request.GET['q']]
      )
      row = cursor.fetchone()
  return row

def fetch_name_1(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute(f"UPDATE bar SET foo = 1 WHERE baz = {baz}")
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute(f"SELECT foo FROM bar WHERE baz = {baz}")
      row = cursor.fetchone()
  return row

def fetch_name_2(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute("SELECT foo FROM bar WHERE baz = %s" % baz)
      row = cursor.fetchone()
  return row

def fetch_name_3(request):
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ruleid: taint-backend-sqli-cursor-execute
      cursor.execute("SELECT foo FROM bar WHERE baz = %s".format(baz))
      row = cursor.fetchone()
  return row

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
                # ruleid: taint-backend-sqli-cursor-execute
                "insert into taskManager_file ('name','path','project_id') values ('%s','%s',%s)" %
                (other_name, upload_path, project_id))


##### True Negatives #########
def fetch_name_4(request):
  # using param list is ok
  baz = request.GET.get("baz")
  with connection.cursor() as cursor:
      # ok: taint-backend-sqli-cursor-execute
      cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [baz])
      # ok: taint-backend-sqli-cursor-execute
      cursor.execute("SELECT foo FROM bar WHERE baz = %s", [baz])
      row = cursor.fetchone()

  return row

def show_user(request):
  with connection.cursor() as cursor:
    # BAD -- Using string formatting
    # Issue with the taint rules it seems.
    # todoruleid: taint-backend-sqli-cursor-execute
    cursor.execute("SELECT * FROM users WHERE username = '%s'" % request.POST["username"])
    user = cursor.fetchone()

    # GOOD -- Using parameters
    # ok: taint-backend-sqli-cursor-execute
    cursor.execute("SELECT * FROM users WHERE username = %s", request.POST["username"])
    user = cursor.fetchone()

    # BAD -- Manually quoting placeholder (%s)
    # todoruleid: taint-backend-sqli-cursor-execute
    cursor.execute("SELECT * FROM users WHERE username = '%s'", request.POST["username"])
    user = cursor.fetchone()

def other(request):
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST.get('name', False)
            upload_path = store_uploaded_file(name, request.FILES['file'])

            other_name = "{}".format(name)
            curs = connection.cursor().execute(
                # ruleid: taint-backend-sqli-cursor-execute
                "insert into taskManager_file ('name','path','project_id') values ('%s','%s',%s)" %
                (other_name, upload_path, project_id))