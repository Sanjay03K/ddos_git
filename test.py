import numpy as np
import sys
import pickle
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

white_listed = []

def icmp_test(attributes):
    model = pickle.load(open("./saved_model/icmp_data.sav", 'rb'))
    result = model.predict([attributes])
    print(result)

@app.route('/', methods=['GET'])
def udp_test():
    args = request.args
    data = args.get("data").split(",")
    print(data)
    # attributes = ['1.0', '0.0', '1.0', '9.0', '10.0', '255.255.1.168']
    # attributes = attributes[:len(attributes) - 1]
    model = pickle.load(open("./saved_model/udp_data.sav", 'rb'))
    result = model.predict([data])
    if(result):
        present = white_listed.count(request.remote_addr)
        if(present):
            return { "data" : args.get("data"), "message" : "<h3>Resource Access is Granted</h3>" }
        else:
            return redirect(url_for('null_route', ip=args.get("data"))) 
    else:
        return { "data" : args.get("data"), "message" : "<h3>Resource Access is Granted</h3>" }

@app.route('/blackhole/<ip>')
def null_route(ip):
    message = "<h3>DDOS Attack has been detected on the server..</h3><p>Your ip "+ request.remote_addr +" is not Whitelisted and hence discarded.</p>"
    return { "data" : ip, "message" : message }

@app.route('/WhiteListMyIP', methods=['GET'])
def White_list():
    present = white_listed.count(request.remote_addr)
    if(present):
        return "<h3>Already WhiteListed Your IP</h3>"
    else:
        white_listed.append(request.remote_addr)
        return "<h3>Your IP " +request.remote_addr+ " has been WhiteListed Successfully</h3>"

def tcp_syn_test(attributes):
    model = pickle.load(open("./saved_model/tcp_syn_data.sav", 'rb'))
    result = model.predict([attributes])
    print(result)

if __name__ == "__main__":
    app.run(debug=True)
    if sys.argv[1] == "icmp": 
        icmp_test(sys.argv[2:])
    elif sys.argv[1] == "tcp_syn":
        tcp_syn_test(sys.argv[2:])
    elif sys.argv[1] == "udp":
        udp_test(sys.argv[2:])
    else:
        sys.exit("Incorrect protocol has been chosen for testing. Try again.")