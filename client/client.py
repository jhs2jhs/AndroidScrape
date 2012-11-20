import os 
import sys
sys.path.insert(0, os.path.join('../slib/'))

import urllib
import urllib2
import socket
import c_app_review as app_review
import db_review as db_review
import err
import json

##### configure client id here
client_id = 'dtc'
##### configureation server ip here
url_root = 'http://localhost:8000/job/entry'

timeout = 10
socket.setdefaulttimeout(timeout)
headers = {'User-Agent': 'Mozilla/5.1 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/9.0.1'}


def page_get(client_id, job_type, job_table, params):
    url_params = urllib.urlencode({'client_id':client_id, 'job_type':job_type, 'job_table':job_table, 'job_params':params})
    url = '%s?%s'%(url_root, url_params)
    try:
        req = urllib2.Request(url=url, headers=headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
        return page
    except Exception as e:
        print e
        return None

def db_init():
    db_review.db_init()

def task_app_review_get():
    page = page_get(client_id, 'task', '', '')
    if page is None:
        err.except_p('page is none')
    try:
        j = json.loads(page)
        print 'TASK review:', len(j)
        app_review.c_task_review_read_main(j)
    except Exception as e:
        err.except_p(e)

def task_app_review_do():
    app_review.review_read_main()

def sync_app_review_read():
    j = app_review.c_sync_review_read_main()
    print 'SYNC review_read', len(j)
    rs = json.dumps(j)
    page = page_get(client_id, 'sync', 'review_read', rs)
    app_review.c_sync_review_read_drop()
    print page

def sync_app_review():
    j = app_review.c_sync_review_main()
    print 'SYNC review:', len(j)
    rs = json.dumps(j)
    page = page_get(client_id, 'sync', 'review', rs)
    app_review.c_sync_review_drop()
    print page
    
# do not need to call every time, maybe only on every day
def cron_app_review():
    page = page_get(client_id, 'cron', 'review_read', '')
    print page
    

def init_db_server():
    page = page_get(client_id, 'init', 'review_read', '')
    print page

if __name__ == '__main__':
    #init_db_server()
    while True:
        db_init()
        cron_app_review() ## be careful when use it, at begining or be at end
        db_init()
        task_app_review_get()
        task_app_review_do()
        db_init()
        sync_app_review_read()
        db_init()
        sync_app_review()
        db_init()
        print '===== next job ====='
