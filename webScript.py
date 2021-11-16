import re
from flask import Flask, render_template, request, redirect
import solchecker
import os


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("page.html")

@app.route("/result",methods = ['POST','GET'])
def result():
    output = request.form.to_dict()
    
    try:
        vertArr = [int(i) for i in output["vertArr"].split(',')]
        #faceMatrix = solchecker.faceMatrixMaker(output["faceMatrix"])
        if output["whichFaceMatrix"] == "600cell":
            faceMatrix = solchecker.get600CellFromGithub()
        else:
            faceMatrix = solchecker.get120CellFromGithub()
    
        isSol = solchecker.solChecker(vertArr, faceMatrix)

    except (ValueError, KeyError):
        return redirect("/home")
    
    
    return render_template("page.html", isSol = isSol)

@app.route("/uploadmatrix", methods=["GET","POST"])
def uploadmatrix():
    if request.method == "POST":
        if request.files:

            try:
                output = request.form.to_dict()
                vertArr = [int(i) for i in output["vertArr"].split(',')]

                txtFile = request.files["faceMatrix"]
                filePath = os.path.join("uploads",txtFile.filename)
                txtFile.save(filePath)
                faceMatrix = solchecker.parseCSV(filePath)

                os.remove(filePath)

            except:
                os.remove(filePath)
                return render_template("uploadmatrix.html", message="Incorrect User Inputs") 

            isSol = solchecker.solChecker(vertArr,faceMatrix)
            return render_template("uploadmatrix.html", message="Upload Succesful",isSol=isSol)
            
    return render_template("uploadmatrix.html",message="Upload")

if __name__ == '__main__':
    #port = int(os.environ.get('PORT',33507))
    app.run(debug=True)
