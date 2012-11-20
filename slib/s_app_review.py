import httplib
import json
from bs4 import BeautifulSoup
import bs4
import urlparse
import urllib
from datetime import datetime
import http
import db_app
import db_sql
import err
import time
import util
#from cate_read_google_play import *
import c_app_review

def db_init():
    db_app.db_init()

def review_read_main_init():
    rows = db_app.db_get_g(db_sql.sql_review_read_app_get, ())
    for row in rows:
        app_id = row[0]
        db_app.db_execute_g(db_sql.sql_review_read_insert, (app_id,))
        
def s_task_review_read_main(client_id, limit=1):
    rows = db_app.db_get_g(db_sql.sql_review_read_get_server_task, (limit, ))
    i_t = len(rows)
    i = 0
    jobs = {}
    for row in rows:
        i = i + 1
        #print '%d of %d'%(i, i_t), 
        app_id = row[0]
        page_num = row[1]
        #page_num = 490
        review_type = row[2]
        review_sort_order = row[3]
        job = {
            'app_id':app_id,
            'pageNum':page_num,
            'review_type':review_type,
            'review_sort_order':review_sort_order
            }
        jobs[i] = job
    print jobs
    for job in jobs:
        j = jobs[job]
        app_id = j['app_id']
        db_app.db_execute_g(db_sql.sql_review_read_update_server_task, (client_id, str(datetime.now()), app_id, ))
    return jobs

def s_sync_review_read_main(client_id, results):
    #client_id = 'dtc'
    #results = c_app_review.c_sync_review_read_main()
    i = 0
    for result in results:
        i = i + 1
        r = results[result]
        app_id = r['app_id']
        page_num = r['pageNum']
        read_status = r['read_status']
        db_app.db_execute_g(db_sql.sql_review_read_update_server_sync, (page_num, read_status, str(datetime.now()), app_id, ))
    return i

def s_sync_review_main(client_id, results):
    #client_id = 'dtc'
    #results = c_app_review.c_sync_review_main()
    print client_id
    i = 0
    for result in results:
        i = i + 1
        r = results[result]
        review_id = r['review_id']
        app_id = r['app_id']
        reviewer = r['reviewer']
        date = r['date']
        device = r['device']
        version = r['version']
        title = r['title']
        comment = r['comment']
        review_star = r['review_star']
        db_app.db_execute_g(db_sql.sql_review_insert_server_sync, (review_id, app_id, reviewer, date, device, version, title, comment, review_star, ))
    return i


## for specific client, release locked job back to available
def s_cron_review_read(client_id):
    #client_id = 'dtc'
    rows = db_app.db_get_g(db_sql.sql_review_read_get_cron, (client_id, ))
    for row in rows:
        app_id = row[0]
        #print app_id
        db_app.db_execute_g(db_sql.sql_review_read_update_cron, (str(datetime.now()), app_id, ))
    return len(rows)

def s_cron_all_review_read():
    #client_id = 'dtc'
    rows = db_app.db_get_g(db_sql.sql_review_read_get_cron_all, (client_id, ))
    for row in rows:
        app_id = row[0]
        #print app_id
        db_app.db_execute_g(db_sql.sql_review_read_update_cron, (str(datetime.now()), app_id, ))
    return len(rows)
        

if __name__ == '__main__':
    db_init()
    review_read_main_init()
    #
    print 'sync review_read'
    #s_sync_review_read_main()
    print 'drop review_read'
    #c_app_review.c_sync_review_read_drop()
    print 'sync review'
    #s_sync_review_main()
    print 'drop review'
    #c_app_review.c_sync_review_drop()
    ## what happened if a project in client is not finished for a continued process
    #for a certian time need to check if it is done or
    cron()
