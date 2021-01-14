from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .form import *
from .filter import orderFilter


def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    order_delivered=orders.filter(status='Delivered').count()
    order_pending=total_orders-order_delivered
    instanceOfModels={'customers':customers,
    'orders':orders,'total_orders':total_orders,'order_delivered':order_delivered,'order_pending':order_pending}
    return render(request,'accounts/dashboard.html',instanceOfModels)


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


def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})


def create_order(request):
    form=OrderForm()
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/')
        

    context={'form':form,'multipleOrder':False}
    return render(request,'accounts/order_form.html',context)


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


def delete_order(request,pk_val):
    order=Order.objects.get(id=pk_val)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    return render(request,'accounts/delete.html',{'order':order})

def add_customer(request):
    if request.method=='POST':
        form=addCustomer(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    form=addCustomer()
    return render(request,'accounts/create_customer.html',{'form':form})


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
