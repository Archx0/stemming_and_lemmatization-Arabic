from crypt import methods
from flask import Flask, render_template, request,current_app,send_file
import os 
import random
from time import ctime
from datetime import date
import qalsadi.lemmatizer
from nltk.stem.isri import ISRIStemmer


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uplaod'
app.config['SECRET_KEY'] = '1234567890'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/count',methods=['GET'])

@app.route('/', methods=['POST','GET'])
def upload_file():
    randomFile = str(ctime()[10:-5].replace(':','')+str(date.today()).replace('-','')).replace(" ","")
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.filename = f'{randomFile}.txt'
        uploaded_file.save(os.path.join('upload', uploaded_file.filename))
        cleanStopWords(randomFile,"clean")
        stem(randomFile,"clean") 
        lemmatization_Ar(randomFile,"clean") 
        PhraseAssignment(randomFile,"create")   
    return render_template('index.html', original=originalText(randomFile) ,stopWord = cleanStopWords(randomFile,"getfile"),lemmatization=lemmatization_Ar(randomFile,"getfile") , stemmer=stem(randomFile,"getfile"),autoPhraseAssignment=PhraseAssignment(randomFile,"getfile") )


@app.route('/static/upload/',methods=['GET'])
def download(filename):
        upload_path = os.path.join(current_app.root_path,f'static/upload/'+str(filename)+".zip")
        return send_file(upload_path,as_attachment=True)

def originalText(filename):
          with open(f"upload/{filename}.txt",'r') as file:
               
            return file.read()
        
def PhraseAssignment(filename,status):
    if status == "getfile":
           file = open(f"PhraseAssignment/{filename}.txt")
           return file.read()
    if status =="create":
        file = open(f"lemmatization/{filename}.txt")
        data = file.read().split()
        for _ in range(1000):
            
            word = random.choice(data)+" "+random.choice(data)
            output = open(f"PhraseAssignment/{filename}.txt",'a')
            output.write("\n"+word)
        output.close
            
            
            
                
def stem(filename,status):
    if status == "getfile":
        stemmer = open(f"stemmer/{filename}.txt")
        return stemmer.read()
    if status =="clean":
        file = open(f'stopword/{filename}.txt')
        for line in file.readlines():
            words = line.split()
            result = list()
            stemmer = ISRIStemmer()
            outfile = open(f"stemmer/{filename}.txt",'a')
            for word in words:
                word = stemmer.norm(word, num=1)  
                if not word in stemmer.stop_words: 
                    
                    # ----------------------
                    # from : motazsaad  github : https://github.com/motazsaad/arabic-light-stemming-py
                    word = stemmer.pre32(word)       # remove length three and length two prefixes in this order
                    word = stemmer.suf32(word)     # remove length three and length two suffixes in this order
                    word = stemmer.waw(word)          # remove connective ‘و’ if it precedes a word beginning with ‘و’
                    word = stemmer.norm(word, num=2)  # normalize initial hamza to bare alif
                    # ----------------------

                    result.append(word) 
                    outfile.write(' '.join(result)+"\n")
            outfile.close()
   
def lemmatization_Ar(filename,status):
    if status == "getfile":
       file =  open(f'lemmatization/{filename}.txt')
       return file.read()
    if status == "clean":
        lemmer = qalsadi.lemmatizer.Lemmatizer()
        with open(f"stemmer/{filename}.txt",'r') as file:
            lemmatization = lemmer.lemmatize_text(file.read())
            open(f'lemmatization/{filename}.txt','a').write(" ".join(lemmatization))
    
def cleanStopWords(filename,status):
    if status == "getfile":
        with open(f"stopword/{filename}.txt",'r') as file:
               
            return file.read()
    if status == "clean":
        block = ["'",'//','+',";",":","!","@","#","$","%","^","&","*","(",")","=","/","\\","]","`","|",".",",","<",">","،","؛"]
        file = open(f'upload/{filename}.txt') 
        stop_words = open("stop_words_list.txt").read()
        
        line = file.read()
        words = line.split() 
        for r in words: 
            if  r not in stop_words and  r not in block: 
                appendFile = open(f'stopword/{filename}.txt','a') 
                appendFile.write("\n"+r.replace("،","").replace(":","").replace(".","").replace("(","").replace(")","").replace("؛","")) 
                appendFile.close() 

            
if __name__ == "__main__":
    app.run(debug=True)
