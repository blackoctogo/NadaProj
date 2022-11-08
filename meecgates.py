
from flask import *
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient,_container_client
from flask_sqlalchemy import SQLAlchemy

import os

'''
import sqlite3
import pandas as pd
filename="worddb"
con=sqlite3.connect(filename+".db")
wb=pd.ExcelFile(filename+'.xlsx')
for sheet in wb.sheet_names:
        df=pd.read_excel(filename+'.xlsx',sheet_name=sheet)
        df.to_sql(sheet,con, index=False,if_exists="replace")
con.commit()
con.close()
'''

storage_account_key = "x3uGxcHOPRBGr6ubganIRxZwH/OtDyVFE6SoekthOBRd4yq57I+o07lWMrSkXxbck6rM+5vIXB+++AStjwIrAQ=="
storage_account_name = "tutoriel"
connection_string = "DefaultEndpointsProtocol=https;AccountName=tutoriel;AccountKey=x3uGxcHOPRBGr6ubganIRxZwH/OtDyVFE6SoekthOBRd4yq57I+o07lWMrSkXxbck6rM+5vIXB+++AStjwIrAQ==;EndpointSuffix=core.windows.net"
container_name = "photos"
def uploadToBlobStorage(file,filename):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(file)
    print(f"Uploaded {filename}.")
# calling a function to perform upload
#uploadToBlobStorage(r"C:\Users\LOMRI Yassine\Documents\GitHub\NadaProj\img\uploads\Logo nada.png",'Logo.png')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worddb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Word(db.Model):
    string = db.Column(db.String(50), primary_key=True)
    added = db.Column(db.Boolean, default= False)

    def __repr__(self):
        return f"Word(string = {self.string}, added = {self.added})"


'''
connect_str = "DefaultEndpointsProtocol=https;AccountName=tutoriel;AccountKey=x3uGxcHOPRBGr6ubganIRxZwH/OtDyVFE6SoekthOBRd4yq57I+o07lWMrSkXxbck6rM+5vIXB+++AStjwIrAQ==;EndpointSuffix=core.windows.net"
#os.getenv('AZURE_STORAGE_CONNECTION_STRING') # retrieve the connection string from the environment variable
container_name = "photos" # container name in which images will be store in the storage account

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
'''




@app.route("/")
def home():
    return render_template('home.html')


@app.route("/mentions-legales")
def ml():
    return render_template('ml.html')


app.config["ALLOWED_IMAGE_EXTENSONS"] = ["M4V","MP4","MOV"]

def allowed_video(filename) :
    if not "." in filename :
        return False
    ext= filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSONS"] :
        return True
    else :
        return False

@app.route("/upload-image", methods= ["GET","POST"])
def upload_image():

    if request.method=="POST" :

        if request.files:

           image = request.files["image"]

           if image.filename== "" :
               print("Image must have a filename")
               return redirect(request.url, text = "Votre vidéo doit comporter un nom.")

           if not allowed_video(image.filename) :
               print("That image ext is not allowed")
               redirect(request.url, text ="Ce type de fichier n'est pas accepté.")

           else :
                filename= secure_filename(image.filename)
                #image.save(os.path.join(app.config["IMAGE_UPLOAD"], filename))
                try:
                    uploadToBlobStorage(image,filename)
                    print("Image Saved")
                except Exception as e:
                    print(e)
                    print("Ignoring duplicate filenames")  # ignore duplicate filename





           #image.save(os.path.join(app.config["IMAGE_UPLOAD" ], image.filename) )

           return redirect(request.url, texte = "Votre vidéo a bien été enregistrée, merci pour votre contribution !")


    return render_template('upload-image.html')



@app.route("/contribuer", methods= ["GET","POST"])
def contribuer():

    if request.method=="POST" :

        if request.files:

           video = request.files["video"]

           if video.filename== "" :
               print("Video must have a filename")
               return render_template('contribute.html', text = "Votre vidéo doit comporter un nom.")

           if not allowed_video(video.filename) :
               print("That video ext is not allowed")
               return render_template('contribute.html', text ="Ce type de fichier n'est pas accepté.")

           else :
                filename= secure_filename(video.filename)
                #image.save(os.path.join(app.config["IMAGE_UPLOAD"], filename))
                try:
                    uploadToBlobStorage(video,filename)
                    print("Video Saved")
                    return render_template('contribute.html',
                                           text="Votre vidéo a bien été enregistrée, merci pour votre contribution !")
                except Exception as e:
                    print(e)
                    print("Ignoring duplicate filenames")  # ignore duplicate filename
                return render_template('contribute.html',
                                       text="Ce nom de vidéo est déjà existant, merci de le modifier.")





           #image.save(os.path.join(app.config["IMAGE_UPLOAD" ], image.filename) )





    return render_template('contribute.html')




if __name__ == '__main__':
    app.run(debug=True)