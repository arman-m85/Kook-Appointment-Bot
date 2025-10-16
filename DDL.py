

import mysql.connector

from config import *

def create_and_drop(database):
    conn=mysql.connector.connect(**config)
    print("connect")
    cur=conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database};")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    conn.commit()
    cur.close()
    conn.close()
    print("database create successfully")

def create_table_customer():
    conn=mysql.connector.connect(**config)
    print("connect")
    cur=conn.cursor()

    cur.execute("""
        CREATE TABLE customer (
        ID                  bigint unsigned NOT NULL PRIMARY KEY,
        FULL_NAME           varchar(250) NOT NULL,
        SEX                 ENUM("MALE","FEMALE") NOT NULL,
        PHONE               BIGINT unsigned DEFAULT NULL,
        REGISTER_DATE       DATETIME DEFAULT CURRENT_TIMESTAMP,
        LAST_UPDATE         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("table customer create successfully")

def create_table_provider():
    conn=mysql.connector.connect(**config)
    print("connect")
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE provider (
    ID                    bigint unsigned NOT NULL PRIMARY KEY,
    full_name             varchar(250) NOT NULL,
    address               text NOT NULL,
    city                  varchar(100) NOT NULL,
    phone                 bigint unsigned NOT NULL,
    longitude             DECIMAL(9,6) NOT NULL,
    latitude              DECIMAL(9,6) NOT NULL,
    REGISTER_DATE         DATETIME DEFAULT CURRENT_TIMESTAMP,
    LAST_UPDATE           TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                          
                )

""")
    
    conn.commit()
    cur.close()
    conn.close()
    print("provider_table create successfully")
    
def create_table_service():
    conn=mysql.connector.connect(**config)
    print("connect")
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE service (
    ID                            int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                          varchar(256) NOT NULL,
    duration_minutes              mediumint DEFAULT NULL,
    price                         mediumint DEFAULT NULL

                )AUTO_INCREMENT=10

"""
    )
    conn.commit()
    cur.close()
    conn.close()
    print("sevice_table create successfully")

def create_time_table():
    conn=mysql.connector.connect(**config)
    cur=conn.cursor()
    cur.execute("""
    CREATE TABLE time (
    ID                        bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    START_TIME                                time NOT NULL,
    END_TIME                                  time NOT NULL,
    DATE                                      date NOT NULL,
    IS_BOOKED                              BOOLEAN NOT NULL DEFAULT 0,
    ID_provider_service                    bigint unsigned NOT NULL ,

    FOREIGN KEY (ID_provider_service) REFERENCES provider_service(ID)

          
    
    

    )AUTO_INCREMENT=100
""")

    conn.commit()
    cur.close()
    conn.close()
    print("time_table create successfully")

    
def create_provider_service_table():
    conn=mysql.connector.connect(**config)
   
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE provider_service (
  ID                        bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,             
  ID_provider               bigint unsigned NOT NULL,
  ID_service                int unsigned NOT NULL,

  FOREIGN KEY(ID_provider) REFERENCES provider(ID),
  FOREIGN KEY(ID_service) REFERENCES service(ID)
    )AUTO_INCREMENT=1000
                
""")
   
    conn.commit()
    cur.close()
    conn.close()
    print("provider_service table create successfully")

def create_appointment_table():
    conn=mysql.connector.connect(**config)
    
    cur=conn.cursor()

    cur.execute("""

    CREATE TABLE appointment (
  ID                        bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ID_provider_service                    bigint unsigned NOT NULL ,
  ID_time                   bigint unsigned NOT NULL UNIQUE,
  ID_customer               bigint unsigned DEFAULT NULL,
  status                    enum('reserved','cancelled','done','notified') DEFAULT 'reserved',
    
  
  
    FOREIGN KEY (ID_provider_service) REFERENCES provider_service(ID),
    FOREIGN KEY (ID_time) REFERENCES time(ID),
    FOREIGN KEY (ID_customer) REFERENCES customer(ID),
    UNIQUE (ID_customer,ID_time))
    

""")
    
    conn.commit()
    cur.close()
    conn.close()
    print("table appointment create successfully")


create_and_drop(database)
create_table_customer()
create_table_provider()
create_table_service()
create_provider_service_table()
create_time_table()

create_appointment_table()



