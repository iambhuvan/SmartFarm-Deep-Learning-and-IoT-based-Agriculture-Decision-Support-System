from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
from werkzeug.utils import secure_filename
from time import sleep
import json
import requests as rq
import soil_quality
import seed_quality



app = Flask(__name__)



IP = "192.168.130.114"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clearImage():
    files = os.listdir(UPLOAD_FOLDER)
    for f in files:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        except:
            pass


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('home.html')  


@app.route('/GetSensor', methods=["POST", "GET"])
def updateSensor():
    if request.method == "POST":
        try:
            resp = rq.get(f"http://{IP}/")
            dat = resp.json()
            print(dat)
            return dat
        except:
            return {"T":0,"H":0,"S":0}


# SoilQuality.html
@app.route('/CheckSoil', methods=["POST", "GET"])
def soilQ():
    if request.method == "GET":
        return render_template('SoilQuality.html',ipaddress = IP) 
    if request.method=="POST":
         try:
            data = json.loads(request.data.decode("utf-8"))
            n = float(data["N"])
            p = float(data["P"])
            k = float(data["K"])
            ph = float(data["PH"])
            t = float(data["temp"])
            h = float(data["humi"])
            s = float(data["soil"])
            soilQ = soil_quality.predict_soil_quality([n,p,k,ph,t,h,s])
            cropR = soil_quality.cropRecom([n,p,k,ph,t,h])
            
            #  print(data)
            return {"S":soilQ,'C':cropR}
         except:
             print("ERROR")
    return {"S":"",'C':""}


@app.route('/CheckSeed', methods=["POST", "GET"])
def seedQ():
    if request.method == "GET":
        param = request.args.to_dict()
        print(param)
        soilResult = ''
        CropResult = ''
        if param != {}:
            soilResult = param['param1']
            CropResult = param['param2']
        return render_template('SeedQuality.html',soilResult = soilResult,CropResult = CropResult) 
    if request.method=="POST":
        file = request.files['file']
        #  data = json.loads(request.data.decode("utf-8"))
        #  print(data)
        #  return {"D":"high"}
        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            filename = secure_filename(file.filename)
            if 'seed' not in filename:
                return {"message":'Unusable image'}
            imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(imagePath)
            file.save(imagePath)
            msg = seed_quality.detection(imagePath)
            clearImage()
            # sleep(2)
            # You can include your machine learning logic here using the uploaded image
            return {"message":msg}
    return {"D":""}


@app.route('/Yield', methods=["POST", "GET"])
def Yield_():
    if request.method == "GET":
        param = request.args.to_dict()
        Res = ""
        if param != {}:
            soilResult = param['param1']
            cropResult = param['param2']
            seedResult = param['param3']
            if seedResult  in ['Broken', 'Discolored']:
                yiEld = 'LOW'
            elif soilResult == "Very Good Quality":
                yiEld = 'HIGH'
            else:
                yiEld = 'MEDIUM'

            
            Res = f"""
<table>
    <tr>
        <td>Soil Quality</td>
        <td>{soilResult}</td>
    </tr>
    <tr>
        <td>Seed Quality</td>
        <td>{seedResult}</td>
    </tr>
    <tr>
        <td>Crop Recommended</td>
        <td>{cropResult}</td>
    </tr>
    <tr>
        <th>Yield</th>
        <th>{yiEld}</th>
    </tr>
</table>
"""
        return render_template('Yield.html',result = Res)  

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
