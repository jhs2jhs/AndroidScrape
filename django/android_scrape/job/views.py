# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
import test
import s_app_review as app_review

def entry(request):
    # TODO need to add job name, like review, developer, etc
    client_id = request.REQUEST.get('client_id', None)
    job_type = request.REQUEST.get('job_type', None)
    job_table = request.REQUEST.get('job_table', None)
    params = request.REQUEST.get('job_params', None)
    if (client_id == None or job_type == None):
        return HttpResponse ('Invalidate params')
    else:
        job_type = job_type.lower().strip()
        client_id = client_id.lower().strip()
        job_table = job_table.lower().strip()
        if job_type == 'task':
            context = task_app_review(client_id)
            return HttpResponse(context)
        if job_type == 'sync':
            if job_table == 'review_read':
                context = sync_app_review_read(client_id, params)
            if job_table == 'review':
                context = sync_app_review(client_id, params)
            return HttpResponse(context)
        if job_type == 'cron':
            context = cron_app_review(client_id)
            return HttpResponse(context)
        if job_type == 'test':
            return HttpResponse('TEST: %s test'%(test.a_test()))
        if job_type == 'init':
            db_init()
            return HttpResponse('DB_INIT')

def db_init():
    app_review.db_init()


def task_app_review(client_id):
    app_review.review_read_main_init()
    j = app_review.s_task_review_read_main(client_id)
    rs = json.dumps(j)
    return rs

def sync_app_review_read(client_id, params):
    results = json.loads(params)
    i = app_review.s_sync_review_read_main(client_id, results)
    j = {'SYNC':'review_read', 'SUM':str(i)}
    rs = json.dumps(j)
    return rs

def sync_app_review(client_id, params):
    results = json.loads(params)
    i = app_review.s_sync_review_main(client_id, results)
    j = {'SYNC':'review', 'SUM':str(i)}
    rs = json.dumps(j)
    return rs

def cron_app_review(client_id):
    i = app_review.s_cron_review_read(client_id)
    j = {'CRON':'review', 'SUM':str(i)}
    rs = json.dumps(j)
    return rs

    
    
