
import os
import json
from flask import Flask

app = Flask(__name__)

""" Server to save filedata from fileroulette to JSON db utilizing simple http requests. """
# + Need to write a parser to check json for expired files


@app.route('/submit', methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>', methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>/<file_name>/<file_size>', methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>/<file_name>/<file_size>/<expiration>', methods=["POST", "GET"])
def submit(module=None,url_number=None,file_name=None,file_size=None, expiration=None):
    basic_usage= """http://localhost:5000/submit/upfile/123456/  Bare minimum request , ipaddr:5000/submit/module_name/character string made with url_gen | Upfile.io service
       http://localhost:5000/submit/upfile/123456/test.txt/   Bare minimum plus file name
       http://localhost:5000/submit/upfile/123456/test.txt/3mb/ Bare minimum plus file name, and file size
       http://localhost:5000/submit/upfile/123456/test.txt/3mb/4-20-1922 full request - has module,string found with urlgen, filename,filesize, expiration date
       
       http://localhost:5000/submit/gofile/123456/  Bare minimum request , ipaddr:5000/submit/module_name/character string made with url_gen | Upfile.io service
       http://localhost:5000/submit/gofile/123456/test.txt/   Bare minimum plus file name
       http://localhost:5000/submit/gofile/123456/test.txt/3mb/ Bare minimum plus file name, and file size
       http://localhost:5000/submit/gofile/123456/test.txt/3mb/4-20-1922 full request - has module,string found with urlgen, filename,filesize, expiration date
       """

    data = load_json()
    #If its just a base /submit , then it will return the message explaining the format
    if module ==None and url_number == None and file_name==None and file_size==None and expiration==None:
        return basic_usage

    elif module!=None and url_number !=None:
        modules = {"upfile":"https://uploadfiles.io/{}".format(url_number), "gofile":"https://gofile.io/?c={}".format(url_number)}
        print('Url: {} File: {} File Size:{} Expiration: {}'.format(modules[module], file_name, file_size, expiration))
        data['modules'][module][url_number] = {"url":modules[module],"file_name":file_name, "file_size":file_size, "expiration": expiration}
        write_json(data)
        return "Module: {} Url: {} file_name: {} file_size:{} expiration:{}".format(module,modules[module],file_name,file_size,expiration)

def load_json():
    try:
        with open('files.json', 'r+') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        with open('files.json', 'w+') as json_file:
            data = {
                "modules":{
                    "gofile":{

                    },
                    "upfile":{

                    }
                }
            }
            json_data = json.dumps(data)
            print("Data is : {}".format(data))
            write_json(json_data)
    return data

def write_json(json_object):
    with open('files.json', "r+") as json_file:
        json.dump(json_object, json_file)

if __name__ == "__main__":
    app.run()