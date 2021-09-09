import datetime
import os
import sqlite3
import traceback

SAVE_PATH = os.path.dirname(__file__)
db = os.path.abspath(os.path.join(SAVE_PATH,'xp.db'))
def insert_xp(qq,tags):
    try:
        data_list=[]
        for tag in tags:
            data = (qq,str(tag), str(datetime.datetime.now()))
            data_list.append(data)
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT exists XP
                   (UserQQ varchar(15)  NOT NULL,
                   TAG     varchar(50)  NOT NULL,
                   RECORD_DATE   DATETIME  NOT NULL);''')
        conn.commit()
        sql="INSERT INTO XP (UserQQ,TAG,RECORD_DATE) \
              VALUES (?,?,?)"
        c.executemany(sql,data_list)
        print(sql)
        conn.commit()
        print("插入成功")
    except:
        traceback.print_exc()
    finally:
        conn.close()

def insert_xp_keyword(qq,keyword):
    try:
        data_list=[(str(qq),str(keyword),str(datetime.datetime.now()))]
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT exists XP_KEYWORD
                   (UserQQ varchar(15)  NOT NULL,
                   KEYWORD varchar(50)  NOT NULL,
                   RECORD_DATE   DATETIME  NOT NULL);''')
        conn.commit()
        sql="INSERT INTO XP_KEYWORD (UserQQ,KEYWORD,RECORD_DATE) \
              VALUES (?,?,?)"
        c.executemany(sql,data_list)
        print(sql)
        conn.commit()
        print("插入成功")
    except:
        traceback.print_exc()
    finally:
        conn.close()


def get_xp_keyword(qq):
    try:
        sql = "SELECT UserQQ,KEYWORD ,COUNT(keyword)FROM XP_KEYWORD where UserQQ = '"+qq+"'GROUP BY UserQQ , KEYWORD ORDER BY COUNT(keyword) desc LIMIT 10"
        conn = sqlite3.connect(db)
        c = conn.cursor()
        result_set = c.execute(sql)
        text= ''
        for result in result_set:
            for times in range(0,result[2]):
                text += (str(result[1])+" ")

        print(text)
        return text
    except Exception:
        traceback.print_exc()
    finally:
        conn.close()



def get_xp_tag(qq):
    try:
        sql = "SELECT UserQQ,tag ,COUNT(tag)FROM XP where UserQQ = '"+qq+"'GROUP BY UserQQ , tag ORDER BY COUNT(tag) desc LIMIT 10"
        conn = sqlite3.connect(db)
        c = conn.cursor()
        result_set = c.execute(sql)
        text= ''
        for result in result_set:
            for times in range(0,result[2]):
                text += (str(result[1])+" ")

        print(text)
        return text
    except Exception:
        traceback.print_exc()
    finally:
        conn.close()