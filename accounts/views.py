from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.contrib import messages
from .decorators import *
from .models import *
from .form import *
from .filter import orderFilter

@checkIfAuthenticated
def registerPage(request):
    form=RegisterNewUser()
    if request.method=='POST':
        form=RegisterNewUser(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            group.user_set.add(user)
            Customer.objects.create(user=user,name=user.username)
            messages.success(request,'Account is sucessfully created +'+username)
            return redirect('login')
        else:
            print(form.errors)
    
    context={'form':form}
    return render(request,'accounts/register.html',context)

@checkIfAuthenticated
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,"Username or Password is incorrect !")
    context={}
    return render(request,'accounts/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['customer']))
def userProfile(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    order_delivered=orders.filter(status='Delivered').count()
    order_pending=total_orders-order_delivered
    ordersPerPage=5
    paginator=Paginator(orders,ordersPerPage)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={'orders':orders,'total_orders':total_orders,
    'order_delivered':order_delivered,'order_pending':order_pending,
    'page':page_obj,'paginator':paginator}
    return render(request,'accounts/userProfile.html',context)

@login_required(login_url='login')
@adminOnly(allowed_groups=set(['admin']))
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    order_delivered=orders.filter(status='Delivered').count()
    order_pending=total_orders-order_delivered
    instanceOfModels={'customers':customers,
    'orders':orders,'total_orders':total_orders,'order_delivered':order_delivered,'order_pending':order_pending}
    return render(request,'accounts/dashboard.html',instanceOfModels)

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['customer']))
def accountSetting(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'accounts/account_setting.html', context)
        

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['customer']))
def ourProducts(request):
    products=Product.objects.all()
    productsPerPage=3
    paginator=Paginator(products,productsPerPage)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    productObjectList=page_obj.object_list
    context={'page':page_obj,'paginator':paginator,'productObjectList':productObjectList}
    return render(request,'accounts/ourProducts.html',context)

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def customers(request,pk_val):
    customer=Customer.objects.get(id=pk_val)
    orders=customer.order_set.get_queryset().order_by('id')
    order_count=orders.count()
    Filter=orderFilter(request.GET,queryset=orders)
    orders=Filter.qs
    paginator=Paginator(orders,2)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    instanceOfModels={'customer':customer,'orders':orders,'order_count':order_count,'Filter':Filter,\
    'page':page_obj,'paginator':paginator}
    return render(request,'accounts/customers.html',instanceOfModels)

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def create_order(request):
    form=OrderForm()
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/')
        

    context={'form':form,'multipleOrder':False}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def update_order(request,pk_val):
    
    order=Order.objects.get(id=pk_val)
    
    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
        return redirect('/')
    form=OrderForm(instance=order)
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def delete_order(request,pk_val):
    order=Order.objects.get(id=pk_val)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    return render(request,'accounts/delete.html',{'order':order})

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def add_customer(request):
    if request.method=='POST':
        form=addCustomer(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    form=addCustomer()
    return render(request,'accounts/create_customer.html',{'form':form})

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def update_customer(request,pk_val):
    
    customer=Customer.objects.get(id=pk_val)
    if request.method=='POST':
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
        return redirect('/')
    form=CustomerForm(instance=customer)
    context={'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
@checkPermission(allowed_groups=set(['admin']))
def place_orders(request,pk_val):
    orderFromSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk_val)
    
    if request.method=='POST':
        formset=orderFromSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()

        return redirect('/')
        
    formset=orderFromSet(queryset=Order.objects.none(),instance=customer)
    context={'form':formset,'multipleOrder':True}
    return render(request,'accounts/order_form.html',context)
# Create your views here.
