from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users import templates  
from django.core.files.storage import FileSystemStorage
import subprocess
import os
from django.contrib import messages
from pathlib import Path
import pandas as pd
from django.template import Context

import numpy as np
from glob import glob
from joblib import dump, load #FOR saving 
from tensorflow.keras.models import load_model

import csv
from .models import Revo
from django.db import connection 

@login_required
def home(request):
    return render(request,'Home.html',{'title':'Network Monitoring and anomalys detection system'})

@login_required
def monitoring(request):
    return render(request,'monitoringpage.html',{'title':'Network Monitoring '})
context={'filechecked' : [] ,'query' : []}
@login_required
def detection(request):
    context['filechecked'] = glob("media/*.csv")
    if len(context['filechecked'])==0 :
        test = True
        return render (request,'detectionpage.html',{"test": test})
        
    else :
        print(context['filechecked'])
        return render(request,'detectionpage.html',{"context" :context})


@login_required
def startcicflowmter(request):
    #import os
    #os.system("cmd")
    #os.system("cmd E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat")
    #subprocess.call(["E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat"], shell=True)
    #Popen("E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat",creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    subprocess.Popen('explorer "E:\\PFE\\cicflowmeter\\bin"')

    return render(request,'monitoringpage.html',{'title':'Network Monitoring and anomalys detection system'})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['csvfile']:
        myfile = request.FILES['csvfile']
        
        if os.path.exists("media\\"+myfile.name)  :          
            if len(request.POST.getlist('delete')) == 1:
                os.remove("media\\"+myfile.name)
            else : messages.error(request, 'File already up ')
        else:
            pass

        if not myfile.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
        else:    
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                #df = pd.read_csv(myfile)
                uploaded_file_url = fs.url(filename)
               
                return render(request, 'monitoringpage.html', {
                    'uploaded_file_url': uploaded_file_url
                })   

    return render(request, 'monitoringpage.html')


def satrtanomleisdetection(request):
    
    context['filechecked'] = glob("media/*.csv")
    if len(context['filechecked'])==0 :
        test = True
        return render (request,'detectionpage.html',{"test": test})
        
    else :
        if request.method == "POST":
            a = request.POST.getlist('checkfile')
            if len(a) == 0 :
                messages.error(request, 'Chose your CSV file for the detection paret pleas ')
            else : 
                    
                CIC = pd.read_csv(a[0])
                for i in a[1:] :
                    CIC=pd.concat([CIC,pd.read_csv(i)]) 
            
                flows=CIC
                #Preprocessing
                #Storing THE SOCKET INFO COLUMNS into a variable:
                socket_info=flows[flows.columns[0:7]] 
                print(socket_info)
                flows=flows[flows.columns[7:]]

                #Dropping the Label column
                flows=flows[flows.columns[:-1]]

                #REPLACING inf and -inf values with NAN:
                flows = flows.replace([np.inf, -np.inf], np.nan)

                #REMOVING NAN INSTANCES :
                flows = flows.dropna(axis=0,how='any') 

                #Converting the values into floats
                for i in flows.columns:
                    flows[i]=flows[i].astype(float)
                
                #SCALING THE FEATURES
                #Same thing concerning the path 
                scaler =load('anomalydetection/static/model/Scaler.joblib')
                flows = scaler.transform(flows)

                #Use of PCA
                #Remeber the path 
            # pca =load('anomalydetection/static/model/PCA.joblib')
                #flows_pca = pca.transform(flows)

                #The reverse Hot Encoding (from binary arrays to string )
                encoder=load('anomalydetection/static/model/OHE.joblib')
                #END of Preprocessing 

                #Anomaly detection (Two possibilities available for now, untill we choose the final one )

                #In case of using ANN without pca
                ANN = load_model("anomalydetection/static/model/FINAL_ANN.h5") #the path :)
                result = ANN.predict(flows)

                result = encoder.inverse_transform(result) #reverse of one hot encoding
                result_DF= pd.DataFrame(result, index=None, columns=['Classification']) #Necessary conversion from ndarray to a DataFrame
                classification_results  = pd.concat((socket_info,result_DF), axis=1) #Concatinating the socket infos with the ANN output column
                classification_results.to_csv('media/../trial1.csv') #Exporting the result to a csv file
              
                csvtomodle("trial1.csv")
                
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT Id,Flow_ID,Src_IP,Src_Port,Dst_IP,Dst_Port,Protocol,Timestamp,Classification  FROM 'anomalydetection_revo' LIMIT 0,130")
                finally:
                   
                    context['query'] = cursor.fetchall()
                   
                    
    return render(request ,'detectionpage.html',{"context" :context})
                #In case of using PCA-ANN:
                #ANN_PCA = load_model("/content/gdrive/My Drive/Kaggle/MachineLearningCSV/MachineLearningCVE/FINAL_PCA-ANN.h5") #the path :)
                #result_PCA = ANN_PCA.predict(flows_pca)

                #result_PCA = encoder.inverse_transform(result_PCA)
                #result_DF_PCA= pd.DataFrame(result_PCA, index=None, columns=['Classification'])
                #classification_result_PCA  = pd.concat((socket_info,result_DF_PCA), axis=1)
                #classification_result_PCA.to_csv('trial1.csv') #Exporting the result to a csv file
                #END of Anomaly Detection
                
             

    

def csvtomodle(filecsv) :
   
    with open(filecsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Classification'] != 'BENIGN' :
                # The header row values become your keys
               
                iid = row['']
                Flow_ID = row['Flow ID']
                Src_Port = row['Src Port']
                Dst_IP = row['Dst IP']
                Dst_Port = row['Dst Port']
                Protocol = row['Protocol']
                Timestamp =row['Timestamp']
                Classification =row['Classification']
                new_revo = Revo(Id = iid , Flow_ID=Flow_ID, 
                Src_Port=Src_Port,Dst_IP=Dst_IP,Dst_Port=Dst_Port ,Protocol =Protocol ,Timestamp =Timestamp ,Classification=Classification)
                new_revo.save()


             