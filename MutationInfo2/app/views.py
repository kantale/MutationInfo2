from django.shortcuts import render
from django.http import HttpResponse

import simplejson


def index(request):
    context = {}
    return render(request, 'app/index.html', {})

def has_data(f):
    '''
    Decorator that passes AJAX data to a function parameters
    '''
    def wrapper(*args, **kwargs):
            request = args[0]
            if request.method == 'POST':
                    if len(request.POST):
                            for k in request.POST:
                                    kwargs[k] = request.POST[k]
                    else:
                            POST = simplejson.loads(request.body)
                            for k in POST:
                                    kwargs[k] = POST[k]
            elif request.method == 'GET':
                    for k in request.GET:
                            kwargs[k] = request.GET[k]
                            print ("GET: {} == {}".format(k, kwargs[k]))

            return f(*args, **kwargs)

    return wrapper


@has_data
def answer(request, **kwargs):
    question = kwargs['question']

    json = simplejson.dumps({"reply": 'test'})
    return HttpResponse(json, content_type='application/json')
