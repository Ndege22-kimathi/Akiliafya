import json

import requests
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from MentalHealth.credentials import LipanaMpesaPpassword, MpesaAccessToken
from MentalHealth.forms import CheckoutForm, ImageUploadForm
from MentalHealth.models import Checkout, Member, Images
from .models import Professional
from .forms import ProfessionalForm

def trainers(request):
    if request.method == "POST":
        form = ProfessionalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service-professionals')  # Redirect after successful upload
    else:
        form = ProfessionalForm()

    trainers = Professional.objects.all()
    context = {
        'service-professionals': trainers,
        'form': form,
    }
    return render(request, 'service-professionals.html', context)

# Create your views here.
def home(request):
    if request.method == 'POST':
        if Member.objects.filter(
                username=request.POST['username'],
                password=request.POST['password'],
        ).exists():
            members = Member.objects.get(
                username=request.POST['username'],
                password=request.POST['password'],
            )
            return render(request, 'index.html', {'members': members})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def about(request):
    return render(request,'about.html')
def plan(request):
    return render(request,'plans.html')
def contact(request):
    return render(request,'contact.html')
def details(request):
    return render(request,'service-details.html')
def Services(request):
    return render(request,'Services.html')
def pricing(request):
    return render(request,'pricing.html')

def starter(request):
    return render(request,'starter-page.html')
def checkout(request):
    if request.method == "POST":
        mycheckout = Checkout(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            payment_method=request.POST['payment_method'],  # added payment method
            mpesa_number=request.POST['mpesa_number'],  # added mpesa phone number

        )
        mycheckout.save()
        return redirect('/display')
    else:

        return render(request, 'checkout.html', )  # updated the template name to 'checkout.html'

def view(request):
    checkouts= Checkout.objects.all()
    return render(request,'display.html',{'checkout':checkouts})
def delete(request, id):
    appoint = Checkout.objects.get(id=id)
    appoint.delete()
    return redirect('display')

def edit(request,id):
    edit=Checkout.objects.get(id=id)
    return render(request,'edit.html',{'checkout':edit})
def update(request,id):
    updateinfo = Checkout.objects.get(id=id)
    form = CheckoutForm(request.POST,instance=updateinfo)
    if form.is_valid():
        form.save()
        return redirect('/display')
    else:
        return render(request,'edit.html')
def register(request):
    if request.method ==   "POST":
        memberinfo=Member(
            name = request.POST['name'],
            username = request.POST['username'],
            password = request.POST['password']
        )
        memberinfo.save()
        return redirect('/login')
    else:
        return render(request,'register.html')
def login(request):
    return render(request,'login.html')


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/showimage')
    else:
        form = ImageUploadForm()
    return render(request, 'upload-image.html', {'form': form})

def show_image(request):
    images = Images.objects.all()
    return render(request, 'show-image.html', {'images': images})

def pay(request):
   return render(request, 'payment.html')


def imagedelete(request, id):
    image = Images.objects.get(id=id)
    image.delete()
    return redirect('/showimage')
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'payment.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Your Payment has been successfully made!")

