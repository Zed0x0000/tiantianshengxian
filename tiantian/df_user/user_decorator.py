# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect


def login(func):
    def inner(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())
            return red

    return inner