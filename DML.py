
import mysql.connector
from config import *
database="VS_SQL"

def insert_customer_data(ID,full_name,phone,sex):
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor()
    SQL_QUERY="INSERT INTO customer  (ID,FULL_NAME,PHONE,SEX) VALUES(%s,%s,%s,%s)"
    cursor.execute(SQL_QUERY,(ID,full_name,phone,sex))
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_provider_data(ID,full_name,address,city,phone,longitude,latitude):
    
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor()
    SQL_QUERY="INSERT INTO provider (ID,full_name,address,city,phone,longitude,latitude) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(SQL_QUERY,(ID,full_name,address,city,phone,longitude,latitude))
    cnx.commit()
    cursor.close()
    cnx.close() 

def insert_service_data(name,duration_minutes=None,price=None):
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor()
    SQL_QUERY="INSERT INTO service (name,duration_minutes,price) VALUES(%s,%s,%s) "
    cursor.execute(SQL_QUERY,(name,duration_minutes,price))
    last_row=cursor.lastrowid
    cnx.commit()
    cursor.close()
    cnx.close()
    return last_row


def insert_time_table(start_time,end_time,date,provider_id,is_booked=0):
    cnx=mysql.connector.connection.MySQLConnection(**config)

    cursor=cnx.cursor()
    SQL_QUERY="INSERT INTO time (start_time,end_time,date,is_booked,ID_provider_service) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(SQL_QUERY,(start_time,end_time,date,is_booked,provider_id))
    
    
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_provider_service_table(ID_provider,ID_service):

    cnx=mysql.connector.connection.MySQLConnection(**config)

    cursor=cnx.cursor()
    SQL_QUERY="INSERT INTO provider_service (ID_provider,ID_service)  VALUES(%s,%s)"
    cursor.execute(SQL_QUERY,(ID_provider,ID_service))
    
    cnx.commit()
    cursor.close()
    cnx.close()
    

#     ID                        bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
#   ID_provider_service                    bigint unsigned NOT NULL ,
#   ID_time                   bigint unsigned NOT NULL UNIQUE,
#   ID_customer               bigint unsigned DEFAULT NULL,
#   status                    enum('reserved','cancelled','done') DEFAULT 'reserved',
    
def insert_appointment (ID_provider_service,ID_time,ID_customer,status='reserved'):
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor()
    SQL_QUERY="INSERT INTO appointment (ID_provider_service,ID_time,ID_customer,status) VALUES(%s,%s,%s,%s)"

    cursor.execute(SQL_QUERY,(ID_provider_service,ID_time,ID_customer,status))
    cursor.execute("UPDATE TIME SET is_booked= 1 WHERE ID = %s",(ID_time,))
    cnx.commit()
    cursor.close()
    cnx.close()
    print("yes")

def delete_service(ID):
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor()
    SQL_QUERY="DELETE FROM service WHERE ID=%s"
    
    cursor.execute(SQL_QUERY,(ID,))

    print("service_delete")
    cnx.commit()
    cursor.close()
    cnx.close()

def delete_provider_service_row(ID_provider,ID_service):
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor()
    SQL_QUERY="DELETE FROM provider_service WHERE ID_provider = %s AND ID_service = %s"
    
    cursor.execute(SQL_QUERY,(ID_provider,ID_service))

    print("delete_provider_service_row")
    cnx.commit()
    cursor.close()
    cnx.close()

def change_status(ID, new_status):
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor()
    SQL_QUERY="UPDATE appointment SET status = %s WHERE ID = %s"
    cursor.execute(SQL_QUERY,(new_status,ID))
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":

    
    
     insert_customer_data("reza","091243242","MALE")
    # insert_customer_data("javad","09111123","MALE")
    # insert_customer_data("sara","091234345","FEMALE")
    
    # insert_provider_data("sofi","vanak","theran","0922233432")
    # insert_service_data("haircut","60","200000")
    # insert_service_data("dentist")
    #print(insert_service_data("کارواش","160","1110000"))
    #delete_provider_service_row(7886490404,17)
    #insert_provider_service_table(990,990)
    # insert_provider_service_table(2,11)
    # insert_time_table("22:00:00","23:00:00","2025-7-22",1,0)
    # insert_time_table("20:00:00","21:00:00","2025-7-22",1,0)
    # insert_time_table("15:00:00","16:00:00","2025-7-22",1,0)
    # insert_time_table("20:00:00","21:00:00","2025-7-22",2,0)
    # insert_time_table("16:00:00","18:00:00","2025-7-22",2,0)
    # insert_time_table("12:00:00","13:00:00","2025-7-22",2,0)
    # insert_appoimtment(1,10,100,1,"reserved")
    # insert_appoimtment(1,10,101,2,"reserved")
    # insert_appoimtment(1,10,102,3,"reserved")
    # insert_appoimtment(2,11,103,4,"reserved")
    # insert_appoimtment(2,11,104,1,"reserved")


