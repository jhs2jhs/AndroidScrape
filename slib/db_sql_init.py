import sqlite3

sql_init = '''
--
-- read_status : 0 = default, 1 = done
-- task_status : 0 = default, 1 = done, 2 = assign a, 3 = a release
-- task_assign : 0 = default, xxx = user's real id
-- task_date_create : 
-- task_date_update : 
--
---- android_zoom start ----
CREATE TABLE IF NOT EXISTS android_zoom_category (
  cate_group TEXT NOT NULL, 
  cate_name TEXT NOT NULL,
  cate_path TEXT NOT NULL UNIQUE,
  cate_param TEXT NOT NULL DEFAULT 0, -- last successful 
  --
  read_status TEXT NOT NULL DEFAULT 0, 
  task_status TEXT NOT NULL DEFAULT 0, 
  task_assign TEXT NOT NULL DEFAULT 0, 
  task_create_date TEXT,
  task_update_date TEXT
);
CREATE TABLE IF NOT EXISTS android_zoom_app_read (
  app_name TEXT, 
  app_path TEXT NOT NULL UNIQUE,
  app_id TEXT,
  --
  read_status TEXT NOT NULL DEFAULT 0, 
  task_status TEXT NOT NULL DEFAULT 0, 
  task_assign TEXT NOT NULL DEFAULT 0, 
  task_create_date TEXT,
  task_update_date TEXT
);
---- android_zoom end ---- 
---- app start ----
CREATE TABLE IF NOT EXISTS app (
  app_id TEXT NOT NULL UNIQUE, 
  title TEXT,
  icon TEXT, 
  developer_name TEXT,
  developer_href TEXT, 
  developer_website TEXT, 
  developer_email TEXT, 
  developer_privacy TEXT, 
  desc TEXT, 
  update_date TEXT, 
  current_version TEXT, 
  requires_android TEXT, 
  category TEXT,
  installs TEXT, 
  file_size TEXT, 
  price TEXT, 
  content_rating TEXT, 
  rating_total TEXT,
  rating_average TEXT DEFAULT 0,
  rating_0 TEXT DEFAULT 0,
  rating_1 TEXT DEFAULT 0,
  rating_2 TEXT DEFAULT 0,
  rating_3 TEXT DEFAULT 0,
  rating_4 TEXT DEFAULT 0,
  rating_5 TEXT DEFAULT 0,
  rank TEXT DEFAULT -1,  
  -- 
  read_status TEXT NOT NULL DEFAULT 0, 
  task_status TEXT NOT NULL DEFAULT 0, 
  task_assign TEXT NOT NULL DEFAULT 0, 
  task_create_date TEXT,
  task_update_date TEXT
);
---- app end ----
---- app review ----
CREATE TABLE IF NOT EXISTS review_read (
  app_id TEXT NOT NULL UNIQUE,
  pageNum TEXT NOT NULL DEFAULT 0,
  review_type TEXT DEFAULT 1, 
  review_sort_order TEXT DEFAULT 0,
  --
  read_status TEXT NOT NULL DEFAULT 0, 
  task_status TEXT NOT NULL DEFAULT 0, 
  task_assign TEXT NOT NULL DEFAULT 0, 
  task_create_date TEXT,
  task_update_date TEXT
);
CREATE TABLE IF NOT EXISTS review (
  review_id TEXT NOT NULL UNIQUE,
  app_id TEXT NOT NULL,
  reviewer TEXT, 
  date TEXT, 
  device TEXT, 
  version TEXT,
  title TEXT,
  comment TEXT, 
  review_star TEXT
);
---- app review ----
'''



