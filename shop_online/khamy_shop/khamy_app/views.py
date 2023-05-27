from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.

@unauthenticated_user
#function name (registerPage) to take a request from urls file
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request,'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'khamy_temp/register.html', context) #returning register.html from templates

@unauthenticated_user
#function name (loginPage) to take a request from urls file
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'khamy_temp/login.html', context) #returning login.html from templates

#function name (logoutUser) to take a request from urls file
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
#function name (home) to take a request from urls file
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status= 'Delivered').count()
    pending = orders.filter(status= 'Pending').count()

    context = {'orders':orders, 'customers':customers, 
    'total_orders':total_orders, 'delivered':delivered, 
    'pending':pending }

    return render(request, 'khamy_temp/dashboard.html', context) #returning dashboard.html from templates


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
#function name (userPage) to take a request from urls file
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status= 'Delivered').count()
    pending = orders.filter(status= 'Pending').count()

    print('ORDER:', orders)

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 
    'pending':pending}
    return render(request, 'khamy_temp/user.html', context) #returning user.html from templates


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
#function name (accountSettings) to take a request from urls file
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'khamy_temp/khamy_temp_settings.html', context) #returning khamy_temo_settings.html from templates



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
#function name (products) to take a request from urls file
def products(request):
    products = Product.objects.all() #querying our database from product model
    return render(request, 'khamy_temp/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
#function name (customers) to take a request from urls file
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'khamy_temp/customers.html', context) #returning customer.html from templates

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
#function name (createOrder) to take a request from urls file
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('printing Post:', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'khamy_temp/order_form.html', context) #returning order_form.html from templates

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
#function name (updateOrder) to take a request from urls file
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'khamy_temp/order_form.html', context) #returning order_form.html from templates

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
#function name (deleteOrder) to take a request from urls file
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'khamy_temp/delete.html', context) #returning delete.html from templates