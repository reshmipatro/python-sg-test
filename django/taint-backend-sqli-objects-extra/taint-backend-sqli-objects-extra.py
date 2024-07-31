from django.http import HttpResponse
from django.db import models

### Semgrep

class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)

class Entry(models.Model):
    name = models.CharField(...)
    description = models.CharField(...)

##### extra() True Positives #########
def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-objects-extra
  user_age = Person.objects.extra(where=["name = %s" % user_name])
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  user_name = request.GET.get('user_name')
  # ruleid: taint-backend-sqli-objects-extra
  user_age = Person.objects.extra(where=["name = %s" % user_name, "id not NULL"])
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  path = request.path
  # ruleid: taint-backend-sqli-objects-extra
  user_age = Person.objects.extra(where=["path = %s" % path])
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

def get_user_age(request):
  path = request.path
  # ruleid: taint-backend-sqli-objects-extra
  user_age = Person.objects.extra(where=[f"path ={path}"])
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)


##### extra() True Negative #########
def get_user_age(request):
  # no dataflow
  user_name = request.GET.get('user_name')
  # ok: taint-backend-sqli-objects-extra
  user_age = Person.objects.extra(where=["name = 'user_name'"])
  html = "<html><body>User Age %s.</body></html>" % user_age
  return HttpResponse(html)

### CodeQL
def raw3(request):
    user_name = request.GET.get('user_name')
    # ruleid: taint-backend-sqli-objects-extra
    User.objects.extra("insert into names_file ('name') values ('%s')" % user_name)


def raw4(request):
    user_name = request.GET.get('user_name')
    m = User.objects.filter('foo')
    # ruleid: taint-backend-sqli-objects-extra
    m.extra("select foo from bar where baz = %s" % user_name)



# Guardrails DOCS

def raw5(request):
    baz = request.GET.get('user_name')
    # ruleid: taint-backend-sqli-objects-extra
    Entry.objects.extra(where=["headline=%s" % baz])

def raw6(request):
    baz = request.GET.get('baz')
    # ok: taint-backend-sqli-objects-extra
    Entry.objects.extra(where=['headline=%s'], params=[baz])

# Django DOCS

def raw7(request):
    baz = request.GET.get('user_name')
    # ok: taint-backend-sqli-objects-extra
    Entry.objects.extra( 
        select={'val': "select col from sometable where othercol = %s"},
        select_params=(baz,),
    )

def raw8(request):
    baz = request.GET.get('user_name')
    Entry.objects.extra( 
        # ruleid: taint-backend-sqli-objects-extra
        select={'val': "select col from sometable where othercol = %s" % baz}
    )