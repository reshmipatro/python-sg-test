from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.http import HttpResponse
from django.template import loader

def insecure(request):
    template = loader.get_template('contents.html')
    # ruleid:taint-backend-xss-mark-safe
    insecure = mark_safe(
        """
        <div>
            <p>Contents! %s</p>
        </div>
        """ % request.POST.get("contents")
    )
    return HttpResponse(template.render({"html_example": insecure}, request))

def fine(request):
    template = loader.get_template('contents.html')
    # ok:taint-backend-xss-mark-safe
    fine = mark_safe(
        """
        <div>
            <p>Contents!</p>
        </div>
        """
    )
    return HttpResponse(template.render({"html_example": fine}, request))

def secure(request):
    template = loader.get_template('contents.html')
    # ok:taint-backend-xss-mark-safe
    this_is_ok = format_html(
        """
        <div>
            <p>Contents! {}</p>
        </div>
        """,
        request.POST.get("contents")
    )
    # ok:taint-backend-xss-mark-safe
    safestring.mark_safe('<b>{}</b>'.format('secure'))
    
    my_secure_str = 'secure'
    # ruleid:taint-backend-xss-mark-safe
    mark_safe(request.POST.get("contents"))
    # ok:taint-backend-xss-mark-safe
    mark_safe('<b>{}</b>'.format(my_secure_str))
    # ok:taint-backend-xss-mark-safe
    mark_safe('<b>{} {}</b>'.format(my_secure_str, 'a'))
    # ok:taint-backend-xss-mark-safe
    mark_safe('<b>{} {}</b>'.format(*[my_secure_str, 'a']))
    # ok:taint-backend-xss-mark-safe
    mark_safe('<b>{b}</b>'.format(**{'b': my_secure_str}))  # nosec TODO
    my_secure_str = '<b>{}</b>'.format(my_secure_str)
    # ok:taint-backend-xss-mark-safe
    mark_safe(my_secure_str)

    return HttpResponse(template.render({"html_example": this_is_ok}, request))
