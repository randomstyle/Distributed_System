from flask import Flask, request, Response
import os
import uuid
import json
import subprocess
import rocksdb
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to home page"

@app.route("/api/v1/scripts", methods = ['POST'])
def uploader():
    # get post request upload file 
    upFile = request.files['data']
    fileName = uuid.uuid4().hex
    pathh = "/api/v1/scripts"
    if not os.path.isdir(pathh):
        os.makedirs(pathh)
    # save FileStorage to a new file in server
    pathToFile = pathh + "/" + fileName + ".py"
    upFile.save(pathToFile)
    
    db.put(fileName.encode(), pathToFile.encode())
    # create a response with status 201 and json body
    res = Response(json.dumps({'script-id':fileName}), status=201, mimetype='application/json')
    return res

@app.route("/api/v1/scripts/<scriptID>")
def invoker(scriptID):
    # add .py extension so we can run and get the output from stdout. Remove .py extension after that
    #os.rename('/api/v1/scripts/' + scriptID, '/api/v1/scripts/' + scriptID + '.py')
    #result = subprocess.check_output("python3 " + '/api/v1/scripts/' + scriptID + ".py", shell = True)
    #os.rename('/api/v1/scripts/' + scriptID + '.py', '/api/v1/scripts/' + scriptID)

    value = db.get(scriptID.encode()).decode()
    result = subprocess.check_output("python3 " + value, shell = True)
    return result

if __name__ == "__main__":
    db = rocksdb.DB("lab1.db", rocksdb.Options(create_if_missing=True))
    app.run(host='0.0.0.0', port=3000)