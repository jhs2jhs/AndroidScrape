import httplib
import json
from bs4 import BeautifulSoup
import bs4
import urlparse
import urllib
from datetime import datetime
import db_sql
import http
import db_app
import err
import time
import util
from c_list_android_zoom.py import *


def db_init():
    db_app.db_init()

##########
def categories_read_main():
    url = '/'
    print '** categories main %s **'%(url)
    status, body = zoom_http_get(url)
    if status != 200:
        raise Exception('zoom app home http connection errir:%s'%(str(status)))
    soup = BeautifulSoup(body)
    if soup.body.text.strip().find('Access not allowed. If you think this is an error, please contact us at hello@androidzoom.com') > 0:
        raise Exception('Access not allowed. If you think this is an error, please contact us at hello@androidzoom.com')
    divs = soup.body.find_all(name='div', attrs={'id':'categories-list'})
    for div in divs:
        for d in div:
            if d.name.strip() != 'div':
                continue
            cate_group_name = d.h3.text.strip()
            ul = d.ul
            for li in ul:
                if li.a != None and li.a.has_key('href'):
                    cate_name = li.a.text.strip()
                    cate_path = li.a['href'].strip()
                    print cate_group_name, cate_name, cate_path
                    db_app.db_execute_g(db_sql.sql_zoom_cate_insert, (cate_group_name, cate_name, cate_path, str(datetime.now())))

# task : give job from server to client
def s_task_category_read_main():
    client_id = 'dtc'
    limit = 10
    rows = db_zoom.db_get_g(db_sql.sql_zoom_cate_read_get_server, (limit, ))
    i_t = len(rows)
    i = 0
    jobs = {}
    for row in rows:
        i = i + 1
        print '%d of %d'%(i, i_t)
        cate_path = row[0]
        cate_param = row[1]
        print cate_path, cate_param
        job = {'cate_path':cate_path, 'cate_param':cate_path}
        jobs[i] = job
    for j in jobs:
        job = jobs[j]
        cate_path = job['cate_path']
        db_app.db_execute_g(db_sql.sql_zoom_cate_read_update_server_task, (client_id, cate_path, ))
    return jobs



if __name__ == '__main__':
    db_app.db_init()
    categories_read_main()
    #task_category_read_main()
    assign_category_read_main()
