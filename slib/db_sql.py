import sqlite3
from db_sql_init import *

### zoom 
sql_zoom_cate_insert = '''
INSERT OR IGNORE INTO android_zoom_category (cate_group, cate_name, cate_path, task_create_date) VALUES (?,?,?,?)
'''
sql_zoom_cate_read_get_server_task = '''
SELECT cate_path, cate_param FROM android_zoom_category WHERE read_status = 0 AND task_status = 0 LIMIT ?
'''
sql_zoom_cate_read_update_server_task = '''
UPDATE android_zoom_category SET task_status = 1, task_assign = ? WHERE cate_path = ?
'''
sql_zoom_cate_read_get_client = '''
SELECT cate_path, cate_param FROM android_zoom_category WHERE read_status = 0 AND task_status = 0
'''
sql_zoom_cate_read_param_update = '''
UPDATE android_zoom_category SET cate_param = ? WHERE cate_path = ?
'''
sql_zoom_cate_read_update = '''
UPDATE android_zoom_category SET read_status = 1 WHERE cate_path = ? 
'''
sql_zoom_app_insert = '''
INSERT OR IGNORE INTO android_zoom_app_read (app_name, app_path) VALUES (?,?)
'''


#### review 
### this statement will be replace in real code 
sql_review_read_app_get = '''
SELECT app_id FROM app WHERE developer_href IS NOT NULL
'''
sql_review_read_insert = '''
INSERT OR IGNORE INTO review_read (app_id) VALUES (?)
'''
sql_review_read_get_server_task = '''
SELECT app_id, pageNum, review_type, review_sort_order FROM review_read WHERE read_status = 0 AND task_status = 0 LIMIT ?
'''
sql_review_read_update_server_task = '''
UPDATE review_read SET task_status = 1, task_assign = ?, task_create_date = ? WHERE app_id = ?
'''
sql_review_read_insert_server_task = '''
INSERT OR REPLACE INTO review_read (app_id, pageNum, review_type, review_sort_order) VALUES (?,?,?,?)
'''
sql_review_read_get = '''
SELECT app_id, pageNum, review_type, review_sort_order FROM review_read WHERE read_status = 0
'''
sql_review_read_status_update = '''
UPDATE review_read SET read_status = 1 WHERE app_id = ?
'''
sql_review_read_update = '''
UPDATE review_read SET pageNum = ? WHERE app_id = ?
'''
sql_review_insert = '''
INSERT OR IGNORE INTO review (review_id, app_id, reviewer, date, device, version, title, comment, review_star) VALUES (?,?,?,?,?,?,?,?,?)
'''
sql_review_read_get_client_sync = '''
SELECT app_id, pageNum, read_status FROM review_read
'''
sql_review_get_client_sync = '''
SELECT review_id, app_id, reviewer, date, device, version, title, comment, review_star FROM review
'''
sql_review_read_drop_client_sync = '''
drop table if exists review_read;
'''
sql_review_drop_client_sync = '''
drop table if exists review;
'''
sql_review_read_update_server_sync = '''
UPDATE review_read SET pageNum = ?, read_status = ?, task_update_date = ? WHERE app_id = ?
'''
sql_review_insert_server_sync = '''
INSERT OR IGNORE INTO review (review_id, app_id, reviewer, date, device, version, title, comment, review_star) VALUES (?,?,?,?,?,?,?,?,?)
'''
sql_review_read_get_cron = '''
SELECT app_id FROM review_read WHERE read_status = 0 AND task_status = 1 AND task_assign = ?
'''
sql_review_read_update_cron = '''
UPDATE review_read SET task_status = 0, task_assign = 0, task_create_date =? WHERE app_id = ?
'''
sql_review_read_get_cron_all = '''
SELECT app_id FROM review_read WHERE read_status = 0 AND task_status = 1
'''
