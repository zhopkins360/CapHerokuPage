from flask import Flask, render_template, request
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
    
    vertArr = [int(i) for i in output["vertArr"].split(',')]
    
    #faceMatrix = solchecker.faceMatrixMaker(output["faceMatrix"])
    faceMatrix = solchecker.getMatrixFromGithub()
    
    isSol = solchecker.solChecker(vertArr, faceMatrix)
    
    return render_template("page.html", isSol = isSol)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',33507))
    app.run(debug=True)
