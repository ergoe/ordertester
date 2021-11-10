import pyodbc
# import platform
from flask import Flask, Response

import collections
import json

server = '10.110.1.200'
database = '5StarDealCom'
username = 'dev'
password = 'hh$n!UNDNnF4f4WDST54GB2t8vb'
driver = '{ODBC Driver 17 for SQL Server}'
# driver = '{FreeTDS}'
# driver = '{SQL Server}'


app = Flask(__name__)


@app.route('/')
def hello():
    return "hello world"

@app.route('/order/<order_ref>')
def hello_world(order_ref):
    j = None
    # drivers = [item for item in pyodbc.drivers()]
    # driver = drivers[-1]
    # print("driver:{}".format(driver))
    # if platform.system() == 'Windows':
    #     driver = '{SQL Server}'

    with pyodbc.connect(
            'Driver=' + driver + ';Server=tcp:' + server + ';Port=1433;Database=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        try:
            with conn.cursor() as cursor:

                cursor.execute("SELECT orderId, queue FROM Orders with (nolock) WHERE orderreference like ?", order_ref)
                rw = cursor.fetchone()

                objects_list = []
                while rw:
                    d = collections.OrderedDict()
                    d['orderId'] = rw[0]
                    d['queue'] = rw[1]
                    objects_list.append(d)
                    rw = cursor.fetchone()
            j = json.dumps(objects_list)

        finally:
            cursor.close()

            # conn.close()
    return Response(j, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug= True, host='0.0.0.0')
