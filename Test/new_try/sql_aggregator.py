import mysql.connector as msc
from config import user_name, mysql_password, db

connection = msc.connect(host = "localhost", user = user_name, passwd = mysql_password, database=db, auth_plugin='mysql_native_password')
cursor = connection.cursor()

def mysql_data_insert(uid, timestamp,os,node,release,version,machine,processor,ram_usage,err_class, gpu_name):
    command = "INSERT INTO logs_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
    vals = (uid,timestamp,os,node,release,version ,machine,processor,ram_usage,err_class,gpu_name,)
    try:
        cursor.execute(command, vals)
        connection.commit()
    except:
        print("SQL ERROR")
    cursor.close()
    connection.close()