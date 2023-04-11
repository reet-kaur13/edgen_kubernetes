from distutils.log import debug
from faker import Faker
import psycopg2
from random import randint
from datetime import datetime
from faker.providers import DynamicProvider
import random
import os
import pandas as pd
from urllib import response
import json
import sys
import os


fake = Faker('en-US')

hostname = "www.americaniche.com"
database = "postgres"
username = "postgres"
pwd = "password"
port_id = 33306
indexes = 1
conn = psycopg2.connect(host=hostname, database=database,
                        user=username, password=pwd, port=port_id)
cur = conn.cursor()


def input_customers():
    cur = conn.cursor()
    cur.execute("ROLLBACK")

    cur.execute("select count(*) from postgres.advance_jaffle_shop.customers")
    length1 = cur.fetchone()
    print(length1)
    index1 = 1 if length1[0] < 1 else length1[0] + 1




    customer_data = {}
    customer_data['cid'] = index1
    name1 = fake.name()
    customer_data['f_name'] = name1.split()[0]
    customer_data['l_name'] = name1.split()[1]
    try:
        cur.execute("insert into postgres.advance_jaffle_shop.customers values('{}','{}','{}')".format(customer_data['cid'],customer_data['f_name'],customer_data['l_name']))
        conn.commit()
        ds = {
            'Customer id': customer_data['cid'],
            'First Name': customer_data['f_name'],
            'Last Name': customer_data['l_name'],
        }
        print(ds)
        ds = str(ds)
    except:
        print("Waiting.....")


    return ''


def input_data_orders():
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    cur.execute("select count(*) from postgres.advance_jaffle_shop.orders")
    
    length = cur.fetchone()
    m = 0
    cur.execute('select max(user_id) from postgres.advance_jaffle_shop.orders')
    m = cur.fetchone()
    print(length)
    customer_order = {}
    index = 1 if length[0] < 1 else length[0]+1

    customer_order = {}
    customer_order['id'] = index
    customer_order['user_id'] = 100 if m[0]==None else randint(1, m[0])
    customer_order['status'] = random.choice(['completed', 'placed','return_pending','returned','shipped'])
    customer_order['_etl_loaded_at'] = datetime.now()
    customer_order['order_date'] = fake.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2019,12,31))
    try:
        cur.execute("INSERT into postgres.advance_jaffle_shop.orders(id, user_id, order_date, status, _etl_loaded_at) values('{}','{}','{}','{}','{}')".format(customer_order['id'],customer_order['user_id'],customer_order['order_date'],customer_order['status'],customer_order['_etl_loaded_at']))
        conn.commit()
        ds = {
        'id': customer_order['id'],
        'User Id': customer_order['user_id'],
        'Order Date': customer_order['order_date'],
        'status': customer_order['status'],
        '_etl_loaded_at': customer_order['_etl_loaded_at']
        }
        index = index + 1
        ds = str(ds)
        print(ds)
    except:
        print("Waiting.....")



    return ''



def generate():
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    product_data = {}

    product_data = {}
    cur.execute("select count(*) from postgres.advance_jaffle_shop.payment")
    length1 = cur.fetchone()
    print(length1)
    index1 = 1 if length1[0] < 1 else length1[0] + 1

    m = 0
    cur.execute('select max(orderid) from postgres.advance_jaffle_shop.payment')
    m = cur.fetchone()
    # print(m,type(m))

    payment_data = {}
    payment_data['id'] = index1
    payment_data['orderid'] = 100 if m[0]==None else randint(1, m[0])
    payment_data['paymentmethod'] = random.choice(['bank_transfer', 'coupon','credit_card','gift_card'])
    payment_data['amount'] = fake.pricetag()
    payment_data['amount'] = int(float(fake.pricetag()[1:].replace(',', '')))
    payment_data['_batched_at'] = datetime.now()
    payment_data['created'] = fake.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2019,12,31))
    try:
        cur.execute("INSERT into postgres.advance_jaffle_shop.payment(id, orderid, paymentmethod, amount, created, _batched_at) values('{}','{}','{}','{}','{}','{}')".format(payment_data['id'],payment_data['orderid'],payment_data['paymentmethod'],payment_data['amount'],payment_data['created'],payment_data['_batched_at']))
        conn.commit()

        ds = {
            'id': payment_data['id'],
            'orderid': payment_data['orderid'],
            'paymentmethod': payment_data['paymentmethod'],
            'amount':  payment_data['amount'],
            'created': payment_data['created'],
            '_batched_at': payment_data['_batched_at']
        }
        index1 = index1 + 1
        ds = str(ds)
        print(ds)
    except:
        print("Waiting.....")


    return ''


cur.close()

def main():

    input_data_orders()
    input_customers()
    generate()

if __name__ == '__main__':
    try:
        while True:
            globals()[sys.argv[1]]()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
