from django.shortcuts import render, redirect
from django.db import models
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import RegisterJob, ContactForm
from .models import RegisterUser
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.db import IntegrityError

def index(request):
    if request.method == 'POST':
        form = RegisterJob(request.POST)
        if form.is_valid():
            save_data=form.save(commit=False)
            try:
                save_data.save()
            except IntegrityError as e:
                return HttpResponse("already applied")

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            dob=form.cleaned_data['dob']
            job=form.cleaned_data['job']
            subject = "Regarding Job in field of " + job
            message="name: "+name+"\n"+"email: "+email+"\njob: "+job+"\nmobileNo.: "+str(mobile)
            sendMail=EmailMessage(subject,message,to=['surendrameena420@gmail.com'])
            try:
                sendMail.send()
            except:
                return HttpResponse('Invalid Mail')
            form=RegisterJob()
            return redirect('index')

    else:
        form = RegisterJob()
    return render(request, 'index.html', {'form':form})

def about(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render_to_response('about.html', context_dict, context)


def contacts(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am bold font from the context"}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = "From Contact Info"
            message = "name: " + name + "\n" + "email: " + email + "\nmessage: " + message
            sendMail = EmailMessage(subject, message, to=['surendrameena420@gmail.com'])
            try:
                sendMail.send()
            except:
                return HttpResponse('Invalid Mail')
            return HttpResponse(name)

    else:
        form = ContactForm()
    return render(request, 'contacts.html', {'form': form})

