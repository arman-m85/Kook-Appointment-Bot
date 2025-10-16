
import mysql.connector
from config import *
import jdatetime
import datetime
def get_customer_data(CUSTOMER_ID):
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor(dictionary=True)
    try:
        SQL_QUERY="SELECT * FROM customer WHERE ID=%s"
        cursor.execute(SQL_QUERY,(CUSTOMER_ID,))
        result=cursor.fetchall()
    
        cursor.close()
        cnx.close()
        return result[0]
    except  Exception as e :
        return 0

def get_provider_data(PROVIDER_ID):
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor(dictionary=True)
    try:
        SQL_QUERY="SELECT * FROM provider WHERE ID=%s"
        cursor.execute(SQL_QUERY,(PROVIDER_ID,))
        result=cursor.fetchall()

        cursor.close()
        cnx.close()
        return result[0]
    except  Exception as e :
        return 0,e
    
def get_customers_ID():
    cnx=mysql.connector.connection.MySQLConnection(**config)
    cursor=cnx.cursor()
    SQL_QUERY = "SELECT ID FROM customer"
    cursor.execute(SQL_QUERY)
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def get_providers_ID():
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor()
    SQL_QUERY = "SELECT ID FROM provider"
    cursor.execute(SQL_QUERY)
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def get_service_info(ID):
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor(dictionary=True)
    SQL_QUERY="SELECT * FROM service WHERE ID=%s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    if len(result)>0:
        cursor.close()
        cnx.close()
        return result[0]
    else:
        cursor.close()
        cnx.close()
        return 0
    

def get_provider_services_id(ID):
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor()
    SQL_QUERY="SELECT ID_service FROM provider_service WHERE ID_provider=%s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    if len(result)>0:
       cursor.close()
       cnx.close()
       return result
    else:
        cursor.close()
        cnx.close()
        return 0
    
def get_provider_services_row_id(ID):
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor()
    SQL_QUERY="SELECT ID FROM provider_service WHERE ID_service = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    if len(result)>0:
       cursor.close()
       cnx.close()
       return result[0]
    else:
        cursor.close()
        cnx.close()
        return 0
    
def get_provider_service_ID_by_cid(ID):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor()
    SQL_QUERY = "SELECT ID FROM provider_service WHERE ID_provider = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def get_service_id_from_provider_service(ID):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor()
    SQL_QUERY = "SELECT ID_service FROM provider_service WHERE ID = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result[0][0]
    
def get_datetime_info(ID):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM time WHERE ID_provider_service = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result


#def get_time_info_with_id_provider_service
def get_service_id_by_name(name):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor()
    SQL_QUERY = "SELECT ID FROM service WHERE name = %s"
    cursor.execute(SQL_QUERY,(name,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result


def get_provider_service_id(ID):

    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor()
    SQL_QUERY = "SELECT ID FROM provider_service WHERE ID_service = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result[0]

def get_provider_id_from_provider_service(ID):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor()
    SQL_QUERY = "SELECT ID_provider FROM provider_service WHERE ID = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result[0][0]

def get_time_info_with_id(ID):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM time WHERE ID = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result[0]

def get_customer_appointment(ID):
    cnx=mysql.connector.connect(**config)

    cursor = cnx.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM appointment WHERE ID_customer = %s"
    cursor.execute(SQL_QUERY,(ID,))
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def remove_appointment(ID_customer, ID_time_table):

    cnx=mysql.connector.connect(**config)
    cursor = cnx.cursor()
    SQL_QUERY = "DELETE FROM appointment WHERE ID_customer = %s and ID_time = %s"
    cursor.execute(SQL_QUERY,(ID_customer, ID_time_table))
    cnx.commit()
    cursor.close()
    cnx.close()

def get_appointment_info():
    cnx=mysql.connector.connect(**config)
    cursor=cnx.cursor(dictionary=True)
    SQL_QUERY="SELECT * FROM appointment "
    cursor.execute(SQL_QUERY)
    result=cursor.fetchall()
    cursor.close()
    cnx.close()
    return result



    
if __name__ == "__main__":
    # a=7886490404
    # print(get_customer_data(1989143229))
    # print(get_provider_data(7886490404))
    # for  i in get_customers_ID():
    #     print(i)
    # if (a,) in get_customers_ID():
    #     print("Provider ID exists in customers")
 # print(get_service_info(14))
  #  print(list(get_customers_ID())
  #print(get_provider_services_id(7886490404))
  #print(get_time_info_with_id(103))
#   print(get_provider_data(1989143229))
    # for i in get_appointment_info():
    #     cid=i['ID_customer']
    #     time=i['ID_time']
    #     print(cid,time)
    for info in get_appointment_info():
        cid=info['ID_customer']
        time=info['ID_time']
        time_info=get_time_info_with_id(time)
        date=time_info['DATE']
        hour=time_info['START_TIME']
        appointment_date = datetime.datetime(date.year, date.month, date.day, 0, 0)
        test=appointment_date + hour
        print(type(test))
