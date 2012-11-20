import sqlite3
import db_sql
import util

db_path = './db_app.db'

def get_db():
    db = sqlite3.connect(db_path, check_same_thread=False)
    return db

db = get_db()

def db_init():
    global db
    if db == None:
        db = get_db()
    c = db.cursor()
    c.executescript(db_sql.sql_init)
    db.commit()
    c.execute('SELECT * FROM SQLITE_MASTER')
    tables = c.fetchall()
    print '** tables: %s **'%(str(len(tables)))
    c.close()

def db_execute_g(sql, params): # in general
    global db
    if db == None:
        db = get_db()
    c = db.cursor()
    c.execute(sql, params)
    db.commit()
    c.close()

def db_get_g(sql, params):
    global db
    if db == None:
        db = get_db()
    c = db.cursor()
    c.execute(sql, params)
    r = c.fetchall()
    c.close()
    return r



def db_merge(db1, db2):
    print '* merge from %s to %s *'%(db1, db2)
    conn_db1 = sqlite3.connect(db1)
    conn_db2 = sqlite3.connect(db2)
    c1 = conn_db1.cursor()
    c2 = conn_db2.cursor()
    sql1 = '''SELECT app_id, rank FROM app'''
    c1.execute(sql1, ())
    rows = c1.fetchall()
    i_t = len(rows)
    i = 0
    p = 0
    for row in rows:
        app_id = row[0]
        rank = row[1]
        sql2 = db_sql.sql_app_insert_with_rank
        c2.execute(sql2, (app_id, rank, ))
        p, i = util.p_percent_copy(p, i, i_t, 1, conn_db2)
    conn_db2.commit()
    c1.close()
    c2.close()



if __name__ == '__main__':
    db_init()
