#Import statements
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


# Create an app instance
app = Flask(__name__)

# At the end point /
@app.route("/")

# Call method hello
def hello():
    # Render Template index.html
    return render_template("index.html")

# Method for POST values from index.html
@app.route("/", methods = ["POST"])

def mf():
    # Initialize Nornir with a configuration file
    nr = InitNornir("config.yml")
    dna = request.form['dname']                            # Get device name from the form
    getter= request.form['gname']                        # Get the interface name from the form

    if getter == 'Facts': # If the NAPALM getter is = facts
        #Nornir to run napalm getters e.g. facts
        getter_output = nr.run(task=napalm_get, getters=["facts"])
        #Print napalm getters output via print_result function
        print_result(getter_output)
        list = []
        try:
            #For loop to get interusting values from the multiple devices output
            for host, task_results in getter_output.items():
                #Get the device facts result
                device_output = task_results[0].result
                data = {}
                data["host"] = host
                #From Dictionery get vendor name
                data["vendor"] = device_output["facts"]["vendor"]
                #From Dictionery get model
                data["model"] = device_output["facts"]["model"]
                # From Dictionery get version
                data["version"] = device_output["facts"]["os_version"]
                # From Dictionery get serial
                data["ser_num"] = device_output["facts"]["serial_number"]
                # From Dictionery get uptime
                data["uptime"] = device_output["facts"]["uptime"]
                # Append results to a list to be passed to facts.html page
                list.append(data)
            #print (list)
            return render_template("facts.html", resfac=list)      # Send the values of list to the next page for printing
        except:
            return render_template("facts.html", noresfac="No Response from Device")  # Send the values of list to the next page

    elif getter == 'Interface IP':  # If the NAPALM getter is = Interface IP
        #Nornir to run napalm getters interfaces_ip
        getter_output = nr.run(task=napalm_get, getters=["interfaces_ip"])
        #Print napalm getters output via print_result function
        print_result(getter_output)
        list = []
        try:
            #For loop to get interusting values from the output
            for host, task_results in getter_output.items():
                #Get the device interface ip result
                device_output = task_results[0].result
                #print (device_output)
                interface_ip = device_output["interfaces_ip"]
                #print (interface_ip)
                for inte, val in interface_ip.items():
                    data = {}
                    data["host"] = host
                    data["interface"] = inte
                    data["ip_address"] = val["ipv4"].popitem()[0]
                    list.append(data)
            return render_template("interfaceip.html", resint=list)      # Send the values of list to the next page for printing
        except:
            return render_template("interfaceip.html", noresint="No Response from Device")  # Send the values of list to the next page


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)           # run the flask app

