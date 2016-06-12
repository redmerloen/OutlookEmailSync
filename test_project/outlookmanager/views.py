from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .authhelper import (get_signin_url,
                         get_token_from_code,
                         get_user_email_from_id_token)
from .outlookservice import get_my_messages


def home(request):
    redirect_uri = request.build_absolute_uri(reverse('outlookmanager:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url + '">Click here to sign in and view your email</a>')


def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('outlookmanager:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user_email = get_user_email_from_id_token(token['id_token'])

    request.session['access_token'] = access_token
    request.session['user_email'] = user_email
    return HttpResponseRedirect(reverse('outlookmanager:mail'))


def mail(request):
    access_token = request.session['access_token']
    user_email = request.session['user_email']

    if not access_token:
        return HttpResponseRedirect(reverse('outlookmanager:home'))
    else:
        messages = get_my_messages(access_token, user_email)
        return HttpResponse('Messages: %s' % messages)
        # context = {
        #     'messages': messages['value'],
        # }
        # return render(request, 'outlookmanager/mail.html', context)
