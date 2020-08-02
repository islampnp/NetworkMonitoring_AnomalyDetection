from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users import templates  

def ss(request):
    return HttpResponse("Hello, world. You're at the polls index.")



def home(request):
    return render(request,'Home.html',{'title':'Network Monitoring and anomalys detection system'})

def monitoring(request):
    return render(request,'monitoringpage.html',{'title':'Network Monitoring and anomalys detection system'})

def detection(request):
    return render(request,'detection.html',{'title':'Network Monitoring and anomalys detection system'})


@login_required
def startcicflowmter(request):
    #import os
    #os.system("cmd")
    #os.system("cmd E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat")
    #subprocess.call(["E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat"], shell=True)
    #Popen("E:\\PFE\\cicflowmeter\\bin\\CICFlowMeter.bat",creationflags=subprocess.CREATE_NEW_CONSOLE)
    import subprocess
    subprocess.Popen('explorer "E:\\PFE\\cicflowmeter\\bin"')

    return render(request,'monitoringpage.html',{'title':'Network Monitoring and anomalys detection system'})

