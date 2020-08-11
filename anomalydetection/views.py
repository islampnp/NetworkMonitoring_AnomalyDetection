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
import glob
from django.template import Context


@login_required
def home(request):
    return render(request,'Home.html',{'title':'Network Monitoring and anomalys detection system'})

@login_required
def monitoring(request):
    return render(request,'monitoringpage.html',{'title':'Network Monitoring '})

@login_required
def detection(request):
    context = glob.glob("media/*.csv")
    if len(context)==0 :
        test = True
        return render (request,'detectionpage.html',{"test": test})
        
    else :
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
    
    context = glob.glob("media/*.csv")
    if len(context)==0 :
        test = True
        return render (request,'detectionpage.html',{"test": test})
        
    else :
        if request.method == "POST":
            
            a = request.POST.getlist('checkfile')
            CIC = pd.read_csv(a[0])
            for i in a[1:] :
                
                CIC=pd.concat([CIC,pd.read_csv(i)]) 
            print(CIC.shape)
            print(a[0])
        
        return render(request ,'detectionpage.html',{"context" :context})