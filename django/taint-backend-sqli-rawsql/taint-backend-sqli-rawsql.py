from django.db.models.expressions import RawSQL
from django.contrib.auth.models import User
from django.http import HttpResponse

### Sonarqube

def sonarqube(request):
    user_name = request.GET.get('user_name')
    # ruleid: taint-backend-sqli-rawsql
    RawSQL("select col from %s where mycol = %s and othercol = " + user_name, ("test",))  # Sensitive

### Semgrep

##### RawSQL() True Positives #########
def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-rawsql
  user_age = RawSQL('SELECT user_age FROM myapp_person where user_name = %s' % user_name)
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-rawsql
  user_age = RawSQL(f'SELECT user_age FROM myapp_person where user_name = {user_name}')
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-rawsql
  user_age = RawSQL('SELECT user_age FROM myapp_person where user_name = %s'.format(user_name))
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_users(request):
  client_id = request.headers.get('client_id')
  # ruleid: taint-backend-sqli-rawsql
  users = RawSQL('SELECT * FROM myapp_person where client_id = %s'.format(client_id))
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

def get_users(request):
  client_id = request.headers.get('client_id')
  # ruleid: taint-backend-sqli-rawsql
  users = RawSQL(f'SELECT * FROM myapp_person where client_id = {client_id}')
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

##### raw() True Negatives #########
def get_users(request):
  client_id = request.headers.get('client_id')
  # using param list is ok
  # ok: taint-backend-sqli-rawsql
  users = RawSQL('SELECT * FROM myapp_person where client_id = %s', (client_id,))
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

### CodeQL

def test_model(request):
    client_id = request.headers.get('client_id')
    client_name = request.headers.get('client_name')
    # ruleid: taint-backend-sqli-rawsql
    User.objects.annotate(RawSQL(client_id))
    # ruleid: taint-backend-sqli-rawsql
    User.objects.annotate(RawSQL("client_id"), RawSQL(client_name))
    # ruleid: taint-backend-sqli-rawsql
    User.objects.annotate(val=RawSQL(client_id))

    # ruleid: taint-backend-sqli-rawsql
    User.objects.alias(RawSQL("client_id"), RawSQL(client_name))
    # ruleid: taint-backend-sqli-rawsql
    User.objects.alias(val=RawSQL(client_id))

    # ruleid: taint-backend-sqli-rawsql
    raw = RawSQL(client_id)
