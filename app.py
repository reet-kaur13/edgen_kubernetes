from distutils.log import debug
from faker import Faker
import psycopg2
from random import randint
from datetime import datetime
from faker.providers import DynamicProvider
import random
from flask import Flask, Markup, render_template
import os
import pandas as pd
from urllib import response
from flask import (Flask, flash, make_response,
                   render_template, request, redirect, session, url_for, jsonify)
from flask_cors import CORS
import json
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder="./templates")

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content'

app.secret_key = 'abc123'

fake = Faker('en-US')

hostname = "redshift-producer.cnnwpebe6bwf.us-west-2.redshift.amazonaws.com"
database = "dev"
username = "admin"
pwd = "Password_01"
port_id = 5439
indexes = 1
conn = psycopg2.connect(host=hostname, database=database,
                        user=username, password=pwd, port=port_id)
cur = conn.cursor()


@app.route('/')
def main():
    return render_template("index.html",a="ab")


@app.route('/input_customers', methods=["GET", "POST"])
def input_customers():
    cur = conn.cursor()
    cur.execute("ROLLBACK")

    cur.execute("select count(*) from dev.advance_jaffle_shop.customers")
    length1 = cur.fetchone()
    print(length1)
    index1 = 1 if length1[0] < 1 else length1[0] + 1
    customer_data = {}
    customer_data['cid'] = index1
    name1 = fake.name()
    customer_data['f_name'] = name1.split()[0]
    customer_data['l_name'] = name1.split()[1]

    cur.execute("insert into dev.advance_jaffle_shop.customers values('{}','{}','{}')".format(customer_data['cid'],customer_data['f_name'],customer_data['l_name']))
    conn.commit()
    ds = {
        'Customer id': customer_data['cid'],
        'First Name': customer_data['f_name'],
        'Last Name': customer_data['l_name'],
    }
    print(ds)
    ds = str(ds)
    return json.dumps(ds)


@app.route('/input_data_orders', methods=["GET", "POST"])
def input_data_orders():
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    cur.execute("select count(*) from dev.advance_jaffle_shop.orders")
    
    length = cur.fetchone()
    m = 0
    cur.execute('select max(user_id) from dev.advance_jaffle_shop.orders')
    m = cur.fetchone()
    print(length)
    customer_order = {}
    index = 1 if length[0] < 1 else length[0]+1

    customer_order = {}
    customer_order['id'] = index
    customer_order['user_id'] = randint(1, m[0])
    customer_order['status'] = random.choice(['completed', 'placed','return_pending','returned','shipped'])
    customer_order['_etl_loaded_at'] = datetime.now()
    customer_order['order_date'] = fake.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2019,12,31))
    cur.execute("INSERT into dev.advance_jaffle_shop.orders(id, user_id, order_date, status, _etl_loaded_at) values('{}','{}','{}','{}','{}')".format(customer_order['id'],customer_order['user_id'],customer_order['order_date'],customer_order['status'],customer_order['_etl_loaded_at']))
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
    return json.dumps(ds)


@app.route('/generate_get_data', methods=["GET", "POST"])
def generate_get_data():
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    product_data = {}

    product_data = {}
    cur.execute(
        "select distinct cust_id,ord_id from dev.advance_jaffle_shop.curated_dw1")
    length1 = cur.fetchall()
    print(length1[0][0])
    print(len(length1))

    xaxis = []
    yaxis = []
    for i in length1:
        xaxis.append(i[0])
        yaxis.append(i[1])

    print(xaxis)
    print(yaxis)

    return json.dumps({'xaxis': xaxis, 'yaxis': yaxis})


@app.route('/generate', methods=["GET", "POST"])
def generate():
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    product_data = {}

    product_data = {}
    cur.execute("select count(*) from dev.advance_stripe.payment")
    length1 = cur.fetchone()
    print(length1)
    index1 = 1 if length1[0] < 1 else length1[0] + 1

    m = 0
    cur.execute('select max(orderid) from dev.advance_stripe.payment')
    m = cur.fetchone()
    print(m,type(m))

    payment_data = {}
    payment_data['id'] = index1
    payment_data['orderid'] = randint(1, m[0])
    payment_data['paymentmethod'] = random.choice(['bank_transfer', 'coupon','credit_card','gift_card'])
    payment_data['amount'] = fake.pricetag()
    payment_data['amount'] = int(float(fake.pricetag()[1:].replace(',', '')))
    payment_data['_batched_at'] = datetime.now()
    payment_data['created'] = fake.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2019,12,31))
    cur.execute("INSERT into dev.advance_stripe.payment(id, orderid, paymentmethod, amount, created, _batched_at) values('{}','{}','{}','{}','{}','{}')".format(payment_data['id'],payment_data['orderid'],payment_data['paymentmethod'],payment_data['amount'],payment_data['created'],payment_data['_batched_at']))
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
    cur.execute(
        "select distinct cust_id,ord_id from dev.advance_jaffle_shop.curated_dw1")
    length1 = cur.fetchall()
    xaxis = []
    yaxis = []
    for i in length1:
        xaxis.append(i[0])
        yaxis.append(i[1])

    return json.dumps({'xaxis': xaxis, 'yaxis': yaxis, 'ds': ds})


cur.close()

def main():

    input_data_orders()
    input_customers()
    generate()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
