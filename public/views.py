from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Sum
import json
#from public.models import User
from public.models import CustomUser
from public.models import Equipment
from public.models import Rent
from public.models import Withdraw
from public.forms import RegisterForm
from public.forms import RegisterProviderForm
from public.forms import EquipmentForm
from public.forms import RentFirstForm
from public.forms import SettingsForm
from public.forms import CustomUserCreationForm
from public.forms import CustomProviderCreationForm

import random
import requests

from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    equipmentsList = Equipment.objects.all()
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True 
        return render(request,'public/home.html',{"equipmentsList":equipmentsList,"isConnected":isConnected,"user":myuser,"noPadding":True})
        
            
    

    return render(request,'public/home.html',{"equipmentsList":equipmentsList,"isConnected":isConnected,"noPadding":True})
def about(request):
    
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True 
        return render(request,'public/about.html',{"isConnected":isConnected,"user":myuser,"noPadding":True})
        
            
    

    return render(request,'public/about.html',{"isConnected":isConnected,"noPadding":True})
def contact(request):
    
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True 
        return render(request,'public/contact.html',{"isConnected":isConnected,"user":myuser,"noPadding":True})

    return render(request,'public/contact.html',{"isConnected":isConnected,"noPadding":True})

def equipments(request):
   
    equipmentsList = Equipment.objects.all()
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        return render(request,'public/equipments.html',{"equipmentsList":equipmentsList,"isConnected":isConnected,"user":myuser})
    
    return render(request,'public/equipments.html',{"equipmentsList":equipmentsList,"isConnected":isConnected})
def providers(request):
   
    providersList = CustomUser.objects.filter(role="provider")
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        return render(request,'public/providers.html',{"providersList":providersList,"isConnected":isConnected,"user":myuser})

    return render(request,'public/providers.html',{"providersList":providersList,"isConnected":isConnected})
def provider_equipments(request,provider_id):
    
    isConnected = False
    try:

        provider = CustomUser.objects.get(id=provider_id)
        if(provider):
            equipment = Equipment()
            equipmentsList = Equipment.objects.filter(owner=provider)
            myuser = authent_session(request)
            if(myuser):
                isConnected = True
                return render(request,'public/provider-details.html',{"provider":provider,"equipmentsList":equipmentsList,"isConnected": isConnected,"user":myuser})

            return render(request,'public/provider-details.html',{"provider":provider,"equipmentsList":equipmentsList,"isConnected": isConnected})
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
        #return redirect('providers')

        

            
    
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 1. Get the username/password from the cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # 2. Use the authenticate() function to verify credentials
            # This function uses check_password() internally.
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # 3. If valid, call login() to establish the session
                login(request, user)
                return redirect('home') # Redirect to a protected page
            # Note: The form handles most invalid credential errors before this point
    else:
        form = AuthenticationForm()
        
    return render(request, 'public/login.html', {'form': form,"isConnected":False})
def logout_view(request):

    logout(request)
    return redirect('login')
def change_password(request):
    myuser = authent_session(request)
    if(myuser):
        if request.method == 'POST':
            form = PasswordChangeForm (user=request.user, data=request.POST)
            if form.is_valid():
                # 1. Get the username/password from the cleaned data
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
               
                
                # 2. Use the authenticate() function to verify credentials
                # This function uses check_password() internally.
            # user = authenticate(request, username=username, password=password)
                user = form.save()
                
                if user is not None:
                    # 3. If valid, call login() to establish the session
                    #login(request, user)
                    return redirect('login') # Redirect to a protected page
                # Note: The form handles most invalid credential errors before this point
        else:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            
        return render(request, 'public/change-password.html', {'form': form,"isConnected":True,"user":myuser})
def login_old(request):
    
    if(request.method=="POST"):
        myuser = User.objects.get(email=request.POST['email'])
        if(myuser != None):
            if(myuser.password==request.POST['password']):
                request.session['user_id'] = myuser.id
                return redirect("dashboard")
        else:
            return render(request,"public/login.html",{"mode":"error"})
           
           
    return render(request,"public/login.html",{"mode":"normal"})
        
    
def register_old(request):
    
    if(request.method=="POST"):
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            myuser =  form.save()
            myuser.confirmationCode = random.randint(100000,999999)
            myuser.save()
            return redirect('register-confirm',myuser.id)
           
    else:
        form = RegisterForm()

    return render(request,'public/register.html',{'form':form})
def confirm_registration(request):
    #myuser = User.objects.get(id=user_id)
    isConnected = False
    myuser = request.user
    userEntity = get_user_model().objects.get(id=myuser.id)
    if(not userEntity == None):
        isConnected = True
        if (userEntity.confirmed == False):

            if(request.method=="POST"):
                #print(f"comparaison de :{request.POST['confirmationCode']}** et celui du user:{myuser.confirmationCode}**")
                if(int(request.POST["confirmationCode"])==myuser.confirmationCode):
                    myuser.confirmed = True
                    myuser.save()
                    login(request,myuser, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("register-success")
                else:
                    return render(request,'public/confirm_registration.html',{'user':myuser,'mode':'error','isConnected':isConnected})
            
            return render(request,'public/confirm_registration.html',{'user':myuser,'mode':'normal','isConnected':isConnected})
        else:
            logout(request)
            return redirect('login')

def registration_success(request):
    #myuser = User.objects.get(id=user_id)
    myuser = authent_session(request)
    if(myuser):
        return render(request,'public/registration_success.html',{"user":myuser})
def register_new(request):
    if(request.method == "POST"):
        if(request.POST['role']=="provider"):
            return redirect('register-provider')
        
    return render(request,'public/register.html',{"isConnected":False})
def terms_of_use(request):
        
    return render(request,'public/terms-of-use2.html',{"isConnected":False})
def privacy_policy(request):
        
    return render(request,'public/privacy-policy.html',{"isConnected":False})
def register_provider(request):
    if(request.method == "POST"):
        form = CustomProviderCreationForm(request.POST)
        if(form.is_valid()):
            myuser = form.save()
            myuser.confirmationCode = random.randint(100000,999999)
            myuser.role = "provider"
            myuser.save()
            login(request,myuser, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('register-confirm')
        
    form = CustomProviderCreationForm()
    return render(request,'public/register-provider.html',{"form":form,"isConnected":False})
    
def dashboard(request):
    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        return render(request,'public/dashboard.html',{"user":myuser,"isConnected":isConnected})
    else:
        return redirect("login")
def dashboard_wallet(request):

    myuser = authent_session(request)
    if(myuser):
        revenue  = Rent.objects.filter(state="confirmed",equipment__owner=myuser).aggregate(totalAmount=Sum("rentTotalAmount"))
        print(f'la valeur de revenue:{revenue}')
        try:
            revenue['gain'] = float(str(revenue['totalAmount'])) * 95 / 100
        except Exception as e:
            revenue['gain'] =   0
        withdrawsTotalAmount  = Withdraw.objects.filter(provider=myuser).aggregate(totalAmount=Sum("amount"))
        print(f'la valeur de withdraw:{withdrawsTotalAmount}')
        try:
            withdrawsTotalAmount['total'] = float(str(withdrawsTotalAmount['totalAmount'])) 
        except Exception as e:
            withdrawsTotalAmount['total'] =   0

        balance = revenue['gain'] - withdrawsTotalAmount['total']
    return render(request,'public/dashboard-wallet.html',{"revenue":revenue,"withdraws":withdrawsTotalAmount,"balance":balance})
def dashboard_cashin(request):

    myuser = authent_session(request)
    if(myuser):
        cashInflows  = Rent.objects.filter(state="confirmed",equipment__owner=myuser)
       
       
    return render(request,'public/dashboard-cashin.html',{"cashInflowsList":cashInflows})
def dashboard_cashout(request):

    myuser = authent_session(request)
    if(myuser):
        cashOutflows  = Withdraw.objects.filter(state="confirmed",provider=myuser)
       
       
    return render(request,'public/dashboard-cashout.html',{"cashOutflowsList":cashOutflows})

def dashboard_settings(request):
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        if(request.method=="POST"):
            form = SettingsForm(request.POST, request.FILES,instance=myuser)
            if(form.is_valid()):
                form.save()
                
        else:

            form = SettingsForm(instance=myuser)

        return render(request,'public/dashboard-settings.html',{'user':myuser,'form':form,'isConnected':isConnected})
        
    else:
        return redirect('login')
def dashboard_equipments_list(request):
    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        
        equipmentsList = Equipment.objects.filter(owner=myuser)
        return render(request,'public/dashboard-equipments-list.html',{"user":myuser,"equipmentsList":equipmentsList,"isConnected":isConnected})
    else:
        return redirect("login")
def dashboard_equipment_add(request):
    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        if(request.method=="POST"):
            form = EquipmentForm(request.POST, request.FILES)
            if(form.is_valid()):
                equipment = form.save()
                equipment.owner = myuser
                equipment.save()
                return redirect('dashboard-equipments-list')
        else:

            form = EquipmentForm()

        return render(request,'public/dashboard-equipment-add.html',{'user':myuser,'form':form,'isConnected':isConnected})
        
    else:
        return redirect('login')
def dashboard_equipment_update(request,equipment_id):
    isConnected = False
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
        equipment = Equipment.objects.get(id=equipment_id)
        if(request.method=="POST"):
            form = EquipmentForm(request.POST, request.FILES,instance=equipment)
            if(form.is_valid()):
                form.save()
                
                return redirect('dashboard-equipments-list')
        else:

            form = EquipmentForm(instance=equipment)

        return render(request,'public/dashboard-equipment-update.html',{'user':myuser,'form':form,'isConnected':isConnected})
        
    else:
        return redirect('login')


def rent(request,equipment_id):

    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
    
    equipment = Equipment.objects.get(id=equipment_id)
    if(request.method=='POST'):
        form = RentFirstForm(request.POST)
        if(form.is_valid()):

            rent = form.save()
            rent.equipment = equipment
            rent.rentTotalAmount = equipment.price * rent.quantity * rent.duration
            rent.save()
            return redirect('rent-payment-method',rent.id)
        else:
            print(form.errors.as_data())
        
    else:
        form = RentFirstForm()
    return render (request,'public/equipment-rent.html',{'form':form,'equipment':equipment,'isConnected':isConnected})
def rent_payment_method(request,rent_id):

    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True
    rent = Rent.objects.get(id=rent_id)
    equipment = rent.equipment
    if(request.method=='POST'):
        
        rent.paymentMethod = request.POST["paymentMethod"]
        rent.save()
        if(rent.paymentMethod=="mobileMoney"):
            return redirect('rent-mobilemoney-payment',rent.id)

    orderAmount = rent.rentTotalAmount
    return render (request,'public/rent-payment-method.html',{'rent':rent,'equipment':equipment,'orderAmount':orderAmount,'isConnected':isConnected})
def rent_mobilemoney_payment(request,rent_id):

    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True

    rent = Rent.objects.get(id=rent_id)
    equipment = rent.equipment
    
    if(request.method== "POST"):

        rent.mobileMoneyPhone = request.POST["mobileMoneyPhone"]
        
        requestUrl = build_hmoney_service_url()
        requestUrl = f"{requestUrl}&IDTRANS={rent.id}&AMOUNT={rent.rentTotalAmount}"
        requestUrl = requestUrl + "&CURRENCY=USD" + "&PHONENUMBER=" + rent.mobileMoneyPhone + "&operation=initPayment&RETURNURL=a&CANCELURL=b&SUMMARY=s"
        response = requests.get(requestUrl)
        print(requestUrl)
        print(f'la reponse {response.text}')
        hmoneyResponse = decodeHmoneyResponse(response)
        if(hmoneyResponse['ACK']=='SUCCESS'):

            rent.paymentToken = hmoneyResponse['TOKEN']
            rent.paymentId = hmoneyResponse['IDPAY']
            rent.save()

        mode = "processing"

    else:
        mode = "getNumber"
    orderAmount = rent.duration * equipment.price * rent.quantity
            
        

    
    return render (request,'public/rent-mobilemoney-payment.html',{'rent':rent,'equipment':equipment,'orderAmount':orderAmount,'isConnected':isConnected,'mode':mode})
def rent_mobilemoney_payment_confirmed(request,rent_id):

    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True

    rent = Rent.objects.get(id=rent_id)
    equipment = rent.equipment
    
    
    orderAmount = rent.duration * equipment.price * rent.quantity
            
    mode = "paid"

    
    return render (request,'public/rent-mobilemoney-payment-confirmed.html',{'rent':rent,'equipment':equipment,'orderAmount':orderAmount,'isConnected':isConnected,'mode':mode})
def rent_mobilemoney_payment_canceled(request,rent_id):

    isConnected = False 
    myuser = authent_session(request)
    if(myuser):
        isConnected = True

    rent = Rent.objects.get(id=rent_id)
    equipment = rent.equipment
    
    
    orderAmount = rent.duration * equipment.price * rent.quantity
            
    mode = "paid"

    
    return render (request,'public/rent-mobilemoney-payment-canceled.html',{'rent':rent,'equipment':equipment,'orderAmount':orderAmount,'isConnected':isConnected,'mode':mode})

def rent_mobilemoney_payment_check(request,payment_id):
    requestUrl = build_hmoney_service_url()
    requestUrl = f"{requestUrl}&IDTRANS=1&IDPAY={payment_id}&operation=checkPayment"
    response = requests.get(requestUrl)
    print(f'la reponse Hmoney:{response.text}')
    hmoneyResponse = decodeHmoneyResponse(response)

    responseArray ={"state":"unknown"}
    if(hmoneyResponse['STATUS']=='SUCCESSFUL'):
        responseArray ={"state":"paid"}
    else:
        if(hmoneyResponse['STATUS']=='CANCELED'):
            responseArray ={"state":"canceled"}
        else:
            responseArray ={"state":hmoneyResponse['STATUS']}
    responseJson = json.dumps(responseArray) 
    return JsonResponse(responseJson,safe=False)
def authent_session_old(request):
    if(request.session['user_id']):
        myuser = User.objects.get(id=request.session['user_id'])
        if(myuser):
            return myuser
        else:
            return False 
def authent_session(request):
    myuser = request.user
    try:

        myuser = get_user_model().objects.get(id=myuser.id)
        if(not myuser == None):
            return myuser
        else:
            return False
    except:
        return False

def build_hmoney_service_url():
    api_hmoney = 'https://services.hmoneypay.com/api/transactionstest.php?'
      
    version = 1

    

    user = 'henocman@gmail.com' # Utilisateur API

    password = '123'# Mot de passe API

    apiKey = '5744bb828cb31469fe89c024d05138'# VOTRE APIKEY


    api_hmoney = api_hmoney + '&USER=' + user + '&PWD=' + password + '&APIKEY='+ apiKey  # Ajoute tous les paramètres
  

    return  api_hmoney # Renvoie la chaîne contenant tous nos paramètres.
def decodeHmoneyResponse(response):

    result = {}
    responseArray = response.text.split("&")
    for param in responseArray:
        paramContent = param.split("=")
        result[paramContent[0]] = paramContent[1]

    print(result)
    return result