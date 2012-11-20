import httplib
import json
from bs4 import BeautifulSoup
import bs4
import urlparse
import urllib
from datetime import datetime
import http
import db_review
import db_sql
import err
import time
import util
from cate_read_google_play import *
import s_app_review

client_id = 'dtc'

def c_task_review_read_main(jobs):
    #jobs = s_app_review.s_task_review_read_main(client_id)
    for job in jobs:
        j = jobs[job]
        app_id = j['app_id']
        page_num = j['pageNum']
        review_type = j['review_type']
        review_sort_order = j['review_sort_order']
        db_review.db_execute_g(db_sql.sql_review_read_insert_server_task, (app_id, page_num, review_type, review_sort_order, ))

def c_sync_review_read_main():
    rows = db_review.db_get_g(db_sql.sql_review_read_get_client_sync, ())
    i_t = len(rows)
    i = 0
    results = {}
    for row in rows:
        i = i + 1
        #print '%s of %d'%(i, i_t)
        app_id = row[0]
        page_num = row[1]
        read_status = row[2]
        result = {
            'app_id':app_id,
            'pageNum': page_num,
            'read_status': read_status
            }
        results[i] = result
    return results

def c_sync_review_read_drop():
    db_review.db_drop_g('review_read')

def c_sync_review_main():
    rows = db_review.db_get_g(db_sql.sql_review_get_client_sync, ())
    i_t = len(rows)
    i = 0
    results = {}
    for row in rows:
        i = i + 1
        review_id = row[0]
        app_id = row[1]
        reviewer = row[2]
        date = row[3]
        device = row[4]
        version = row[5]
        title = row[6]
        comment = row[7]
        review_star = row[8]
        result = {
            'review_id':review_id, 
            'app_id':app_id,
            'reviewer':reviewer,
            'date':date,
            'device':device,
            'version':version,
            'title':title,
            'comment':comment,
            'review_star':review_star,
            }
        results[i] = result
    return results

def c_sync_review_drop():
    db_review.db_drop_g('review')

#####     
        
def review_read_main():
    rows = db_review.db_get_g(db_sql.sql_review_read_get, ())
    i_t = len(rows)
    i = 0
    for row in rows:
        i = i + 1
        print '%d of %d'%(i, i_t), 
        app_id = row[0]
        page_num = row[1]
        review_type = row[2]
        review_sort_order = row[3]
        status = 200
        while status == 200:
            status, page_num = review_read_loop(app_id, page_num, review_type, review_sort_order)
            time.sleep(10)
        #break

def review_read_loop(app_id, page_num, review_type, review_sort_order):
    params = {
        'id':app_id, 
        'reviewSortOrder':review_sort_order,
        'reviewType':review_type,
        'pageNum':page_num
        }
    param = urllib.urlencode(params)
    url = '/store/getreviews'
    print param, url
    ### only for test, this part
    #if int(page_num)>2:
    #    db_review.db_execute_g(db_sql.sql_review_read_status_update, (app_id, ))
    #    return 404, page_num
    ###
    status, body = android_https_post(url, param)
    if status == 404:
        print '==: 404'
        db_review.db_execute_g(db_sql.sql_review_read_status_update, (app_id, ))
        return status, page_num
    if status != 200:
        print 'app review https connection error: %s'%(str(status))
        return status, page_num
        #raise Exception('app getreview ajax status != 200')
    body = body.lstrip(")]}'").strip()
    try:
        review_read(app_id, body)
        db_review.db_execute_g(db_sql.sql_review_read_update, (page_num, app_id, ))
        page_num = int(page_num) + 1
    except Exception as e:
        err.except_p(e)
    return status, page_num
        
    
def review_read(app_id, body):
    j = json.loads(body)
    if j.has_key('htmlContent'):
        contents = j['htmlContent'].strip()
        soup = BeautifulSoup(contents)
        review_fa = soup.find_all(name='div', attrs={'class':'doc-review'})
        for review_f in review_fa:
            review_author = ''
            review_date = ''
            review_device = ''
            review_version = ''
            review_id = ''
            review_rating = ''
            review_title = ''
            review_text = ''
            author_fa = review_f.find_all(name='span', attrs={'class':'doc-review-author'})
            for author_f in author_fa:
                review_author = author_f.strong.text.strip()
            date_fa = review_f.find_all(name='span', attrs={'class':'doc-review-date'})
            for date_f in date_fa:
                review_date = date_f.text.replace('-', '').strip()
                if date_f.next_sibling != None:
                    if type(date_f.next_sibling) != bs4.element.NavigableString:
                        continue
                    device_version = date_f.next_sibling.replace('-', '').strip()
                    device_version = device_version.split('with version')
                    if len(device_version) == 2:
                        review_device = device_version[0].strip()
                        review_version = device_version[1].strip()
                    if len(device_version) == 1:
                        review_device = device_version[0].strip()
            id_fa = review_f.find_all(name='div', attrs={'class':'goog-inline-block review-permalink'})
            for id_f in id_fa:
                if id_f.parent.has_key('href'):
                    review_id = id_f.parent['href'].strip()
                    review_id = urlparse.urlparse(review_id).query
                    review_id = urlparse.parse_qs(review_id)
                    if review_id.has_key('reviewId') and len(review_id['reviewId'])>0:
                        review_id = review_id['reviewId'][0]
                    else:
                        review_id = ''
            rating_fa = review_f.find_all(name='div', attrs={'class':'ratings goog-inline-block'})
            for rating_f in rating_fa:
                if rating_f.has_key('title'):
                    review_rating = rating_f['title'].strip()
                    review_rating = review_rating.split(' ')
                    if len(review_rating) >= 2:
                        review_rating = review_rating[1].strip()
            title_fa = review_f.find_all(name='h4', attrs={'class':'review-title'})
            for title_f in title_fa:
                review_title = title_f.text.strip()
            text_fa = review_f.find_all(name='p', attrs={'class':'review-text'})
            for text_f in text_fa:
                review_text = review_text + text_f.text.strip() + ' '
            if review_id != '':
                db_review.db_execute_g(db_sql.sql_review_insert, (review_id, app_id, review_author, review_date, review_device, review_version, review_title, review_text, review_rating, ))

  

if __name__ == '__main__':
    # need to check whether it should push the data first
    # need to get data first
    db_review.db_init()
    c_task_review_read_main()
    review_read_main()
    
