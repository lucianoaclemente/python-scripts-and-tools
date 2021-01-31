from flask import Flask, request
from flask_restful import Resource, Api
import mysql.connector
from random import *
import random
import time

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)

def create_order():    
    orderDate = random_date("2015-01-01", "2019-01-01", random.random())    

    mydb = mysql.connector.connect(
      host="your host",
      user="root",
      passwd="root pass",
      database="classicmodels"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT IFNULL(max(orderNumber), 0)+1 FROM orders")
    recOrder = mycursor.fetchall()
    orderNumber = recOrder[0]

    mycursor.execute("select customerNumber from customers order by rand() limit 1")
    recCustomer = mycursor.fetchall()
    customerNumber = recCustomer[0]

    sql = "INSERT INTO orders (orderNumber, orderDate, requiredDate, status, customerNumber  ) VALUES (%s, '" + orderDate + "', '" + orderDate + "', '1', (select customerNumber from customers order by rand() limit 1))"
    val = (orderNumber)
    mycursor.execute(sql, val)
    mydb.commit()

    itemCount = int(uniform(1,4))

    for item in range(1, itemCount+1):
        sql = "select productCode, buyPrice from products WHERE productCode NOT IN (SELECT productCode FROM orderdetails WHERE orderNumber = " + str(orderNumber[0]) + ") order by rand() limit 1"
        mycursor.execute(sql)
        
        recProduct = mycursor.fetchall()
        productCode = recProduct[0][0]
        buyPrice = recProduct[0][1]

        quantity = int(uniform(1,10))
        
        sql = "INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber) VALUES (%s, %s, %s, %s," + str(item) + ")"
        val = (orderNumber[0], productCode, quantity, buyPrice)
        mycursor.execute(sql, val)
        mydb.commit()
        
for x in range(10000):
    print(x)
    create_order()