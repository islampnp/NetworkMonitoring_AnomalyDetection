from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users import templates  
from django.core.files.storage import FileSystemStorage
import subprocess
import os



@login_required
def home(request):
    return render(request,'Home.html',{'title':'Network Monitoring and anomalys detection system'})

@login_required
def monitoring(request):
    return render(request,'monitoringpage.html',{'title':'Network Monitoring '})

@login_required
def detection(request):
    return render(request,'detectionpage.html',{'title':'anomalys detection system'})


@login_required
def startcicflowmter(request):
    #import os
    #os.system("cmd")
    #os.system("cmd E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat")
    #subprocess.call(["E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat"], shell=True)
    #Popen("E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat",creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    subprocess.Popen('explorer "E:\\PFE\\cicflowmeter\\bin"')

    return render(request,'monitoringpage.html',{'title':'Network Monitoring and anomalys detection system'})

from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from pathlib import Path
def simple_upload(request):
    if request.method == 'POST' and request.FILES['csvfile']:
        myfile = request.FILES['csvfile']

        

        
        
        if os.path.exists("media\\"+myfile.name) :
              messages.error(request, 'The file is already ubloaded')
        else:
            #  check if the file is a csv file
            if not myfile.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            else:    
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                return render(request, 'monitoringpage.html', {
                    'uploaded_file_url': uploaded_file_url
                })
        
           

    return render(request, 'monitoringpage.html')