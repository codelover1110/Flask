import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import json
import config
from flask_mail import Mail, Message
import time
import threading
from missingmoney import CrawlSearchManager, CrawlThreadManager, JDefine
from flask import jsonify

app = Flask(__name__)
global csm
csm = CrawlSearchManager()
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.secret_key = 'any random string'

mail = Mail(app)

#     url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'
#     ctm = CrawlThreadManager(1)
#     ret = ctm.set_param(url, key)
#     if ret == JDefine.GET_PROXY_LIST_ERROR:
#         print("No Proxy!")

def url_key_state(lname,  fname, state):
    search_key = ''
    url = ''
    f_state = None
    if fname == "" and state == "":
        search_key = lname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'
        ##url.format(l)
    elif fname == "" and state != "":
        search_key = lname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&State={}&page={}'
        f_state = state
    elif fname != "" and state != "":
        search_key = lname + " " + fname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&State={}&page={}'
        f_state = state
    elif fname != "" and state == "":
        search_key = lname + " " + fname
        url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'

    return url, search_key, state

@app.route('/', methods=['GET', 'POST'])
def index():
    global ctm
    
    if request.method == "GET":
        default_data = {
          'lname': '',
          'fname': '',
          'state': '',
        }
        return render_template("lists.html", data = [], details = default_data)

    if request.method == "POST":
        details = request.form.to_dict()
        lname = details['l_name_search']
        fname = details['f_name_search']
        state = details['state_search']
        thread_status  = details['thread_status']

        print (thread_status, "\t", details['client_key'], "sssssssssssss")
        if thread_status == '':
            print("Create CrawlThreadManager!")
            url = 'https://missingmoney.com/en/Property/Search?searchName={}&page={}'
            if fname == "":
                search_key = lname
            else:
                search_key = lname + " " + fname
            #url, search_key, state = url_key_state(lname, fname, state)
            ctm1 = CrawlThreadManager(5)         

            client_key1 = str(time.time())   
            details['client_key'] = client_key1
            # if ctm1.set_param(url, search_key) == JDefine.NO_SEARCH_RESULT:
            #     print ("no result for: ", key)
            #     thread_status = 'end'
            ctm1.set_param(url, search_key)
            #ctm1.set_param(url, search_key, state)
            ctm1.start()
            csm.append_search(client_key1, ctm1)

            thread_status = 'crawling'
            data = [[], thread_status, client_key1]
            return json.dumps(data)

        client_key = details['client_key']

        ret1, state1, data1 = csm.get_crwal_data(client_key)
        if ret1:
            if state1 == False and len(data1) == 0:
                if secs == 0:
                    secs = time.time() - t
                print ("result count1 = ", search_cnt1)
                print ("search engine_count = ", csm.get_search_count())

                thread_status = 'end'
            else:
                thread_status = 'crawling'
        else:
            print("no no no no no search engine__________111111111111111", csm.get_search_count())

        print ("send data: &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        data = [data1, thread_status, client_key]
        print('---------------------------------------')
        print(json.dumps(data))
        return json.dumps(data)


# @app.route("/get_my_ip", methods=["GET"])
# def get_my_ip():
#     return jsonify({'ip': request.remote_addr}), 200


# @app.route('/', methods=['GET', 'POST'])
# def index():
   
#     t = None
#     if request.method == "GET":
#         default_data = {
#           'lname': '',
#           'fname': '',
#           'state': '',
#         }
#         return render_template("lists.html", data = [], details = default_data)

#     if request.method == "POST":
#         details = request.form.to_dict()
#         lname = details['l_name_search']
#         fname = details['f_name_search']
#         state = details['state_search']
#         thread_status  = details['thread_status']
#         session['username'] = lname
#         if thread_status == '':
#             t = time.time()

#         if t != None:
#             session['time'] = [[t, t, t, t, t, t]]

#         reader = []
#         thread_status = 'crawling'

#         print ("send data: &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
#         print ("data:", reader)
#         data = [session['time'], thread_status]
#         print('---------------------------------------')
#         print(json.dumps(data))
#         return json.dumps(data)

@app.route('/register_people', methods=['POST'])
def register_people():
    if request.method == "POST":
        details = request.form.to_dict()
        print(details)

        msg = Message('Subject: new website query submitted', sender=config.MAIL_USERNAME, recipients=['wilson@inlifeclaims.com','ryan@inlifeclaims.com'])
        msg.body = render_template('register_customer_mail.txt',  data = details,  )
        msg.html = render_template('register_customer_mail.html',  data = details,  )
        with app.app_context():
            mail.send(msg)
        return 'success'

if __name__ == "__main__":
    app.secret_key = 'asdf'
    app.run(debug=False, host='0.0.0.0', port=80)
