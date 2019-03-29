
import os
import json
from flask import Flask, render_template, Markup, redirect
app = Flask(__name__)

""" Server to save filedata from fileroulette to JSON db utilizing simple http requests. """
# + Need to write a parser to check json for expired files


# App routes for each possible layer of submission. Only module name and the random string generated by urlgen is required, but you can resubmit the same item to update it at a later point if necessary
@app.route('/submit/', methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>/',methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>/<file_name>/', methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>/<file_name>/<file_size>/', methods=['POST','GET'])
@app.route('/submit/<module>/<url_number>/<file_name>/<file_size>/<expiration>/', methods=["POST", "GET"])
def submit(module=None,url_number=None,file_name=None,file_size=None, expiration=None):
    # /submit  rendered page to give an overview
    basic_usage= """<pre>
                                        -----Basic user information-----\n\n
                                -- localhost:5000/submit will show this message--\n\n

                                    \t-|Upfile.io|-\n
                    http://localhost:5000/submit/upfile/123456/   ---- Bare minimum request. ipaddr:5000/submit/module_name/character string made with url_gen | Upfile.io service
                    http://localhost:5000/submit/upfile/123456/test.txt/  ----Bare minimum plus file_name
                    http://localhost:5000/submit/upfile/123456/test.txt/3mb/ ----Bare minimum plus file_name, and file_size
                    http://localhost:5000/submit/upfile/123456/test.txt/3mb/4-20-1922 ----full request - has module,string found with urlgen, filename,filesize, and expiration date
                      
                                    \t-|Gofile.io|-\n
                    http://localhost:5000/submit/gofile/123456/  ---Bare minimum request. ipaddr:5000/submit/module_name/character string made with url_gen 
                    http://localhost:5000/submit/gofile/123456/test.txt/   Bare minimum plus file name
                    http://localhost:5000/submit/gofile/123456/test.txt/3mb/ Bare minimum plus file name, and file size
                    http://localhost:5000/submit/gofile/123456/test.txt/3mb/4-20-1922 full request - has module,string found with urlgen, filename,filesize, expiration date
                
                    Note: This allows you to update the entry once its already been added.
                          ex. http://localhost:5000/submit/gofile/123456/    This adds 123456 entry in the gofile part of the structure. 
                          ex  http://localhost:5000/submit/gofile/123456/file_name.iso/700mb/3-29-2019  This appends the filename and the file size to the already entered item
                </pre>    """
    
    # Our data loaded from JSON
    data = load_json()
    
    #If its just a base /submit , then it will return the message explaining the format
    if module ==None and url_number == None and file_name==None and file_size==None and expiration==None:
        return Markup("{}".format(basic_usage))

    #If at least the base required entries for submission are present... add to file and return the information written
    elif module!=None and url_number !=None:
        modules = {"upfile":"https://uploadfiles.io/{}".format(url_number), "gofile":"https://gofile.io/?c={}".format(url_number)}
        print('Url: {} File: {} File Size:{} Expiration: {}'.format(modules[module], file_name, file_size, expiration))
        data['modules'][module][url_number] = {"url":modules[module],"file_name":file_name, "file_size":file_size, "expiration": expiration}
        write_json(data)
        print("Module: {} Url: {} file_name: {} file_size:{} expiration:{}".format(module,modules[module],file_name,file_size,expiration))
        return "Module: {} Url: {} file_name: {} file_size:{} expiration:{}".format(module,modules[module],file_name,file_size,expiration)

def load_json():
    """Loads JSON structure from database/files.json. If files.json isnt found, initialize it with our module names as ('modules':{"module1":{},"module2":{}}}"""
    try:
        with open('database/files.json', 'r+') as json_file:
            data = json.load(json_file)
    #If the file isnt present, make it and initalize with the modules as keys        
    except FileNotFoundError:
        with open('database/files.json', 'w+') as json_file:
            data = dict()
            data['modules'] = {'gofile':{},'upfile':{}}
            json.dumps(data)
            #Write to database/files.json
            write_json(data)
    return data

def write_json(json_object):
    """Writes JSON object to the files.json database"""
    with open('database/files.json', "r+") as json_file:
        json.dump(json_object, json_file)
    print("[+] File Added ")

if __name__ == "__main__":
    app.run()