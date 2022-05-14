from flask import render_template
import pymysql

con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'train')


def insert(pname,age,ptrainno,ptrainname,pclass,psource,pdest,pamt,pstatus,pdoj):
    cursor = con.cursor()       
    SQLQuery = 'insert into passengers(pname,age,ptrainno,ptrainname,pclass,psource,pdest,pamt,pstatus,pdoj) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'   
    i = cursor.execute(SQLQuery,(pname,age,ptrainno,ptrainname,pclass,psource,pdest,pamt,pstatus,pdoj))
    con.commit()    
    return i

def update(pname,age,ptrainno,ptrainname,pclass,psource,pdest,pamt,pstatus,pdoj,pnrno):
    cursor = con.cursor()       
    SQLQuery = 'update passengers set pname=%s,age=%s,ptrainno=%s,ptrainname=%s,pclass=%s,psource=%s,pdest=%s,pamt=%s,pstatus=%s,pdoj=%s where pnrno=%s'   
    i = cursor.execute(SQLQuery,(pname,age,ptrainno,ptrainname,pclass,psource,pdest,pamt,pstatus,pdoj,pnrno))
    con.commit()
    return i

def delete(pnrno):
    cursor = con.cursor()
    SQLQuery = 'delete from passengers where pnrno=%s'
    i = cursor.execute(SQLQuery,(pnrno))
    con.commit()
    return i

def all():
    cursor = con.cursor()
    SQLQuery = 'select * from passengers'
    i = cursor.execute(SQLQuery)
    rows = cursor.fetchall()
    return rows

def get_single_passenger(pnrno):
    cursor = con.cursor()
    SQLQuery = 'select * from passengers where pnrno=%s'
    cursor.execute(SQLQuery,(pnrno))
    row = cursor.fetchone()
    return row


