from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import notename
from .models import folders
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import os
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def allnotes(request):
    data=notename.objects.all()
    l=[]
    for i in data:
        f=open("./notesapp/files/"+i.name+".txt","r")
        s=[x.replace("\n",'')+'<br>' for x in f.readlines()]
        s1=''
        for j in s:
            s1+=j
        l.append({'name':i.name.upper(),'d':s1,'id':i.id,'date':i.date})
    template=loader.get_template('shownote.html')
    context={'data':l}
    return HttpResponse(template.render(context,request))

def addnewnote(request):
    template=loader.get_template('addnote.html')
    return HttpResponse(template.render())    

@csrf_exempt
def adding(request):
    t=request.POST["title"]
    c=request.POST["content"]
    d=notename(name=t,date=datetime.now())

    f=open("./notesapp/files/"+t+".txt","w")
    for i in c:
        if i!="\n":
            f.write(i)
    d.save()
    return HttpResponseRedirect(reverse('allnotes'))

def delete(request,id):
    d=notename.objects.get(id=id)
    d.delete()
    os.remove("./notesapp/files/"+d.name+".txt")
    return HttpResponseRedirect(reverse('allnotes'))
    
def update(request,id):
    d=notename.objects.get(id=id)
    f=open("./notesapp/files/"+d.name+".txt","r")
    template=loader.get_template('updnote.html')
    context={'name':d.name.upper(),'d':f.read(),'id':id}
    print(context)
    return HttpResponse(template.render(context,request))   

@csrf_exempt
def updating(request,id):
    d=notename.objects.get(id=id)
    t=d.name=request.POST["title"]
    d.date=datetime.now()
    c=request.POST["content"]
    f=open("./notesapp/files/"+t+".txt","w")
    for i in c:
        if i!="\n":
            f.write(i)
    d.save()
    return HttpResponseRedirect(reverse('allnotes'))

def showfolders(request):
    f=folders.objects.all()
    fname=[]
    for i in f:
        fname.append({"name":i.name,"id":i.id})
    context={'f':fname,}
    template=loader.get_template("foldershow.html")
    return HttpResponse(template.render(context,request))

def openfold(request,id):
    fold=folders.objects.get(id=id)
    d=[]
    for i in fold.files.split(","):
        d.append(notename.objects.get(id=i))
    l=[]
    for i in d:
        f=open("./notesapp/files/"+i.name+".txt","r")
        s=[x.replace("\n",'')+'<br>' for x in f.readlines()]
        s1=''
        for j in s:
            s1+=j
        l.append({'name':i.name.upper(),'d':s1,'id':i.id})
    template=loader.get_template('showfoldnotes.html')
    context={'data':l,'y':fold.name}
    return HttpResponse(template.render(context,request))

def prints(request,id):
    d=notename.objects.get(id=id)
    f=open("./notesapp/files/"+d.name+".txt","r")
    s=[x.replace("\n",'')+'<br>' for x in f.readlines()]
    s1=''
    for j in s:
        s1+=j
    template=loader.get_template('mailit.html')
    context={'name':d.name.upper(),'id':id}
    return HttpResponse(template.render(context,request))   

def mailing(request,id):
    d=notename.objects.get(id=id)
    f=open("./notesapp/files/"+d.name+".txt","r")
    s=f.readlines()
    
    p=FPDF(orientation='L',unit='mm',format="letter")
    p.add_page()
    p.set_font('Arial',size=20)
    p.cell(250,1,txt=d.name.upper(),ln=1,align='C')
    p.cell(250,5,txt="",ln=1,align='L')
    p.set_font('Arial',size=7)
    for j in s:
        p.cell(250,3,txt=j,ln=1,align='C')
    p.output(d.name+'.pdf')

    name=d.name+".pdf"

    body='''please find attached
    your notesapp pdf
    python test uwu'''

    sender="adonuts593@gmail.com"
    password="aastwoqmutpbhbsf"

    receiver=request.POST['email']

    message=MIMEMultipart()
    message['From']=sender
    message['To']=receiver
    message['Subject']="attachment given"

    message.attach(MIMEText(body,'plain'))
    pdf=open(name,'rb')

    pl=MIMEBase('application','octate-stream',Name=name)
    pl.set_payload(pdf.read())

    encoders.encode_base64(pl)
    pl.add_header('Content-Decomposition','attachment',filename=name)
    message.attach(pl)

    session=smtplib.SMTP('smtp.gmail.com',587)

    session.starttls()

    session.login(sender,password)

    text=message.as_string()
    session.sendmail(sender,receiver,text)
    session.quit()

    print('mail sent')
    return HttpResponseRedirect(reverse('allnotes'))
