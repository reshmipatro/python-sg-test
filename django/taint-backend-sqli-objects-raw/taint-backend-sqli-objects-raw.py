from django.http import HttpResponse
from django.db import models

class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)

### SEMGREP

##### raw() True Positives #########
def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-objects-raw
  user_age = Person.objects.raw('SELECT user_age FROM myapp_person where user_name = %s' % user_name)
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-objects-raw
  user_age = Person.objects.raw(f"SELECT user_age FROM myapp_person where user_name = {user_name}")
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-objects-raw
  user_age = Person.objects.raw('SELECT user_age FROM myapp_person where user_name = %s'.format(user_name))
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_users(request):
  client_id = request.headers.get('client_id')
  # ruleid: taint-backend-sqli-objects-raw
  users = Person.objects.raw('SELECT * FROM myapp_person where client_id = %s' % client_id)
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

def get_users(request):
  client_id = request.headers.get('client_id')
  # ruleid: taint-backend-sqli-objects-raw
  users = Person.objects.raw(f'SELECT * FROM myapp_person where client_id = {client_id}')
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

##### raw() True Negatives #########
def get_user_age(request):
  user_name = request.GET.get('user_name')
  # django queryset is good
  user_age = Person.objects.filter(user_name=user_name).first()
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_users(request):
  client_id = request.headers.get('client_id')
  # using param list is ok
  # ok: taint-backend-sqli-objects-raw
  users = Person.objects.raw('SELECT * FROM myapp_person where client_id = %s', (client_id,))
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

# Code QL
def get_users(request):
  client_id = request.headers.get('client_id')
  # using param list is ok
  # ok: taint-backend-sqli-objects-raw
  users = User.objects.raw("SELECT * FROM users WHERE username = %s", (client_id,))
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)

def get_userss(request):
  username = request.headers.get('client_id')
  # ruleid: taint-backend-sqli-objects-raw
  users = User.objects.raw("insert into names_file ('name') values ('%s')" % username)
  html = "<html><body>Users %s.</body></html>" % users
  return HttpResponse(html)