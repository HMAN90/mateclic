from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from .decorators import admin_only
from public.models import Equipment,Category,Rent
from .forms import CategoryForm
from datetime import date, datetime

@admin_only
def admin_dashboard(request):
    usersNumber = get_user_model().objects.count()
    return render(request,'adminmodule/admin-dashboard.html',{"usersNumber":usersNumber})
@admin_only
def admin_stats(request):
    usersNumber = get_user_model().objects.count()
    return render(request,'adminmodule/admin-stats.html',{"usersNumber":usersNumber})
@admin_only
def admin_categories_list(request):
    
    categoriesList = Category.objects.all().order_by('name')
    categoriesNumber = categoriesList.count()
    return render(request,'adminmodule/admin-categories-list.html',{"categoriesList":categoriesList,"categoriesNumber":categoriesNumber})
@admin_only
def admin_category_add(request):
   
    if(request.method=="POST"):
        form = CategoryForm(request.POST, request.FILES)
        if(form.is_valid()):
            category = form.save()
            
            return redirect('admin-categories-list')
    else:

        form = CategoryForm()

    return render(request,'adminmodule/admin-category-add.html',{'form':form})

@admin_only
def admin_category_update(request,categoryId):
   
   try:
        category = Category.objects.get(id=categoryId)
        if(request.method=="POST"):
            form = CategoryForm(request.POST, request.FILES,instance=category)
            if(form.is_valid()):
                category = form.save()
                
                return redirect('admin-categories-list')
        else:

            form = CategoryForm(instance=category)

        return render(request,'adminmodule/admin-category-update.html',{'form':form,'category':category})
   except Exception as e:
       print("il y a une exception")
       return render(request,'adminmodule/admin-category-update.html'),
       #return redirect('admin-categories-list')

@admin_only
def admin_category_delete(request,categoryId):
   
   try:
        category = Category.objects.get(id=categoryId)
        if(request.method=="POST"):
            form = CategoryForm(request.POST, request.FILES,instance=category)
            
            category.delete()
                
            return redirect('admin-categories-list')
        else:

            form = CategoryForm(instance=category)

        return render(request,'adminmodule/admin-category-delete.html',{'form':form,'category':category})
   except Exception as e:
        print("il y a une exception")
        #return render(request,'adminmodule/admin-category-delete.html')

        return redirect('admin-categories-list')
    

@admin_only
def admin_providers_list(request):
    providersList = get_user_model().objects.all()
    return render(request,'adminmodule/admin-providers-list.html',{"providersList":providersList})
@admin_only
def admin_category_equipments(request,category_id):
    categoriesList = Category.objects.all().order_by('name')
    
    
    if(not category_id == "all"):
        try:
            category = Category.objects.get(id=category_id)
            equipmentsList = Equipment.objects.filter(category=category)
        except Exception as e:

            print('Il y a une exception')
    else:
        equipmentsList = Equipment.objects.all().order_by('name')
    

                
    return render(request,'adminmodule/admin-category-equipments.html',{"categoriesList":categoriesList,"equipmentsList":equipmentsList,"categoryId":category_id})
@admin_only
def admin_equipments_stats(request):
    categoriesList = Category.objects.all().order_by('name')
    
    categoryId = 'all'
    category = None
    if(request.method=="POST"):
        dateMode = request.POST['periodicity']
        
        try:
            category = Category.objects.get(id=request.POST['categoryId'])
            categoryId = request.POST['categoryId']
        except Exception as e:
            print(f"il y a une exception")
            categoryId = 'all'
            category = None
        if(dateMode=="interval"):
            dateStartArray = request.POST['dateStart'].split('-')
            dateStart = datetime(int(dateStartArray[0]),int(dateStartArray[1]),int(dateStartArray[2]),0,0,0)
            dateEndArray = request.POST['dateEnd'].split('-')
            dateEnd = datetime(int(dateEndArray[0]),int(dateEndArray[1]),int(dateEndArray[2]),23,59,59)
        else:
            dateArray = request.POST['reportDate'].split('-')
            dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
            dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
        
    else:
        dateMode = "daily"
        now = datetime.now()
        today = str(datetime.today()).split()[0] 
        print(f"la valeur du now:{now} et la valeur du today:{today}")
        dateArray = today.split('-')
        dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
        dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
    if (categoryId=='all'):
        equipmentsRecords = Equipment.objects.filter(createdAt__range=(dateStart, dateEnd))
    else:
        equipmentsRecords = Equipment.objects.filter(createdAt__range=(dateStart, dateEnd),category=category)
    equipmentsRecordsNumber = equipmentsRecords.count()
    return render(request,'adminmodule/admin-equipments-stats.html',{"categoriesList":categoriesList,"equipmentsList":equipmentsRecords,"equipmentsRecordsNumber":equipmentsRecordsNumber,"category":category,"categoryId":categoryId})


@admin_only
def admin_users_stats(request):
    state = "all"
    
 
    
    if(request.method=="POST"):
        dateMode = request.POST['periodicity']
        
       
        if(dateMode=="interval"):
            dateStartArray = request.POST['dateStart'].split('-')
            dateStart = datetime(int(dateStartArray[0]),int(dateStartArray[1]),int(dateStartArray[2]),0,0,0)
            dateEndArray = request.POST['dateEnd'].split('-')
            dateEnd = datetime(int(dateEndArray[0]),int(dateEndArray[1]),int(dateEndArray[2]),23,59,59)
        else:
            dateArray = request.POST['reportDate'].split('-')
            dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
            dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
        
    else:
        dateMode = "daily"
        now = datetime.now()
        today = str(datetime.today()).split()[0] 
        print(f"la valeur du now:{now} et la valeur du today:{today}")
        dateArray = today.split('-')
        dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
        dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
    if (state=='all'):
        usersRecords = get_user_model().objects.filter(createdAt__range=(dateStart, dateEnd))
    else:
        usersRecords = get_user_model.objects.filter(createdAt__range=(dateStart, dateEnd),confirmed=True)
    usersRecordsNumber = usersRecords.count()
    return render(request,'adminmodule/admin-users-stats.html',{"usersList":usersRecords,"usersRecordsNumber":usersRecordsNumber,"state":state})

@admin_only
def admin_rents_stats(request):
    
    
    state = "all"
    
 
    
    if(request.method=="POST"):
        dateMode = request.POST['periodicity']
        
       
        if(dateMode=="interval"):
            dateStartArray = request.POST['dateStart'].split('-')
            dateStart = datetime(int(dateStartArray[0]),int(dateStartArray[1]),int(dateStartArray[2]),0,0,0)
            dateEndArray = request.POST['dateEnd'].split('-')
            dateEnd = datetime(int(dateEndArray[0]),int(dateEndArray[1]),int(dateEndArray[2]),23,59,59)
        else:
            dateArray = request.POST['reportDate'].split('-')
            dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
            dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
        
    else:
        dateMode = "daily"
        now = datetime.now()
        today = str(datetime.today()).split()[0] 
        print(f"la valeur du now:{now} et la valeur du today:{today}")
        dateArray = today.split('-')
        dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
        dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
    if (state=='all'):
        rentsRecords = Rent.objects.filter(createdAt__range=(dateStart, dateEnd))
    else:
        rentsRecords = Rent.objects.filter(createdAt__range=(dateStart, dateEnd),state=state)
    rentsRecordsNumber = rentsRecords.count()
    return render(request,'adminmodule/admin-rents-stats.html',{"rentsList":rentsRecords,"rentsRecordsNumber":rentsRecordsNumber,"state":state})
@admin_only
def admin_revenue(request):
    
    
    
    
 
    
    if(request.method=="POST"):
        dateMode = request.POST['periodicity']
        
       
        if(dateMode=="interval"):
            dateStartArray = request.POST['dateStart'].split('-')
            dateStart = datetime(int(dateStartArray[0]),int(dateStartArray[1]),int(dateStartArray[2]),0,0,0)
            dateEndArray = request.POST['dateEnd'].split('-')
            dateEnd = datetime(int(dateEndArray[0]),int(dateEndArray[1]),int(dateEndArray[2]),23,59,59)
        else:
            dateArray = request.POST['reportDate'].split('-')
            dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
            dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
        
    else:
        dateMode = "daily"
        now = datetime.now()
        today = str(datetime.today()).split()[0] 
        print(f"la valeur du now:{now} et la valeur du today:{today}")
        dateArray = today.split('-')
        dateStart = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),0,0,0)
            
        dateEnd = datetime(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]),23,59,59)
    
    revenue  = Rent.objects.filter(createdAt__range=(dateStart, dateEnd),state="confirmed").aggregate(totalAmount=Sum("rentTotalAmount"))
    print(f'la valeur de revenue:{revenue}')
    try:
        revenue['gain'] = float(str(revenue['totalAmount'])) * 5 / 100
    except Exception as e:
        revenue['gain'] =   0
    return render(request,'adminmodule/admin-revenue.html',{"revenue":revenue})
