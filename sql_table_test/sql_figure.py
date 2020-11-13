import os
import sqlite3 as sql
import re
import datetime
import shutil

table_name = 'emp'
outputdir  = '/Users/grigorijtolkacev/test_sql_table/'
dir_new_photo = outputdir + '/new_photo/'
table_path = 'myTest_0.db'
list_new_photos = os.listdir(outputdir + '/new_photo/')
if not len(list_new_photos):
    print('There are no new photos ')
    exit()
# define date
now = datetime.datetime.now()
CREATE_DATE = '%s-%s-%s '%(now.day,now.month,now.year)
# connect to our table
flagExistFile = os.path.exists(table_path)
con = sql.connect(table_path)
cur = con.cursor()

# create table if file was not exist
sql_command = """CREATE TABLE IF NOT EXISTS %s (PHOTO_ID INTEGER,
                                                    PERSON_ID INTEGER,
                                                    ACTION TEXT,
                                                    EMP_PHOTO BLOB,
                                                    CREATE_DATE DATE,
                                                    STATUS INTEGER,
                                                    MODIFY_DATE DATE,
                                                    ERROR_TEXT TEXT );"""%(table_name)
cur.execute(sql_command)
con.commit()



def readImage(filename):
    fin = open(filename, "rb")
    img = fin.read()
    return img

def search_PERSIN_ID(PERSON_ID):
    ask = 'SELECT PHOTO_ID FROM %s WHERE PERSON_ID=?'%(table_name)
    param = (PERSON_ID,)
    cur.execute(ask,param)
    tup = cur.fetchone()
    return tup

def update_photo(EMP_PHOTO, PHOTO_ID,CREATE_DATE,PERSON_ID):
    query = 'UPDATE %s SET ACTION=?, EMP_PHOTO=?,CREATE_DATE=?,STATUS=? WHERE PHOTO_ID=?'%(table_name)
    param = (str("LOAD"),EMP_PHOTO,CREATE_DATE,0,PHOTO_ID,)
    cur.execute(query,param)
    print("UPDATE PHOTO FOR PERSON_ID = %s"%PERSON_ID)

def create_new_PERSON(PHOTO_ID,PERSON_ID,EMP_PHOTO,CREATE_DATE):
    sql_command = """INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ? );"""%(table_name)
    data = (PHOTO_ID, PERSON_ID ,'LOAD', EMP_PHOTO, CREATE_DATE, 0, '','' )
    print('Added: PHOTO_ID-%s PERSON_ID-%s ACTION-%s EMP_PHOTO-new_photo CREATE_DATE-%s STATUS-%s'%(PHOTO_ID, PERSON_ID ,'LOAD', CREATE_DATE, 0))
    cur.execute(sql_command,data)


def moveOldPhoto(path,list_new_photos):
    old_photo_dir = path + 'old_photo/'
    new_photo_dir = path + 'new_photo/'
    if not os.path.exists(old_photo_dir):
        os.makedirs(old_photo_dir)
    for i in list_new_photos:
        shutil.move(new_photo_dir+i,old_photo_dir)
        print('Move photo %s to old_photo_dir'%i)


def main():
    # define last PHOTO_ID in table 
    cur.execute("SELECT * FROM  %s  WHERE ROWID IN ( SELECT max( ROWID ) FROM emp );"%(table_name))
    one_result = cur.fetchone()
    
    if one_result:
        PHOTO_ID = one_result[0]+1
    else:
        PHOTO_ID = 1
    #push new data in table 
    for i in list_new_photos:
        full_path_photo = dir_new_photo + '/' + i
        EMP_PHOTO = readImage(full_path_photo)
        PERSON_ID = int(re.findall(r'\d+', i)[0])
        #research PERSON_ID in table
        UP = search_PERSIN_ID(PERSON_ID)
        if UP:
            update_photo(EMP_PHOTO,UP[0],CREATE_DATE,PERSON_ID)
        else:
            create_new_PERSON(PHOTO_ID,PERSON_ID,EMP_PHOTO,CREATE_DATE)
        con.commit()
        PHOTO_ID+=1
    cur.close()
    con.close()
    moveOldPhoto(outputdir,list_new_photos)

main()



