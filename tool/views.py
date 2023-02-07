from django.shortcuts import render, redirect
from .forms import TicketForm, UserRegistrationForm, OperatorProfile
from .models import Ticket,Operator,NidanTicket
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from .decorators import unauthorized_user,allowed_users,admin_only
from django.core.paginator import Paginator
# Create your views here.

@unauthorized_user
def loginuser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'username or password might be wrong.')
    return render(request,'registration/login.html')


def logoutuser(request):
    messages.success(request,'Logout Successfully')
    logout(request)
    return redirect('login')


@unauthorized_user
def register(request):
    form = UserRegistrationForm()
    if request.method=='POST':
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account Created Successfully For '+username)
            return redirect('index')
    dic = {
        'user_form':form,
    }
    return render(request,'registration/register.html',dic)


@login_required(login_url='login')
def userSettings(request):
    form = OperatorProfile(instance = operator)
    if request.method == 'POST':
        form = OperatorProfile(request.POST,request.FILES,instance=operator)
        if form.is_valid():
            form.save()
    dic = {
        'form':form,
    }
    return render(request,'ticket/userprofile.html',dic)



@login_required(login_url='login')
# @allowed_users(allowed_roles=['operator'])
def api_nidan(request):
    message_flag = None
    response_data =  None
    if request.method=='GET':
        url = 'https://uat3.cgg.gov.in/cggrievancemmu/getDocketDetails'
        response = requests.get(url)
        data = response.json()
        response_data = data['data']
        for  glpi_client in response_data:
            client = NidanTicket(
            docket_number = glpi_client['docketNo'],
            citizen_name = glpi_client['citizenName'],
            phone =glpi_client['phone'],
            address =glpi_client['address'],
            email =glpi_client['email'],
            district_name =glpi_client['districtName'],
            municipality =glpi_client['municipality'],
            colony_name =glpi_client['colonyName'],
            house_number =glpi_client['houseNo'],
            street_test =glpi_client['street'],
            section =glpi_client['section'],
            message =glpi_client['message'],
            subsection =glpi_client['subsection'],
            status =glpi_client['status'],
            grievance_remark =glpi_client['grievanceRemarks'],
            callstart  =glpi_client['callStart'],
            opuserid = glpi_client['opuserid']
            )
            try:
                client.save()
                message_flag = True
            except:
                message_flag = False
    if message_flag == True :        
        messages.success(request,'New data is arrived')
    else:
        messages.warning(request,'All data have been fatched from the Nidan Api')
    nidan_tickets = NidanTicket.objects.filter(status='pending')
    print(nidan_tickets)
    dic = {
        'nidan_tickets':nidan_tickets,
    }
    return render(request,'ticket/api_html.html',dic)

@login_required(login_url='login')
def nidan_ticket_data(request,nidan_id):
    nidan_ticket = NidanTicket.objects.get(id = nidan_id)
    if request.method=='POST':
        nidan_ticket.status = 'solved'
        nidan_ticket.save
        return redirect('api_nidan')
    return render(request,'ticket/api_html.html',)


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator','admin'])
def index(request):
    ticket_open= None
    ticket_closed= None
    total_ticket= None
    ticket_reopened= None
    ticket_duplicate= None
    ticket_resolved= None     
    print('new pritn',request.user.groups)
    if request.user.groups == 'admin':
        tickets = Ticket.objects.all()
        total_ticket = tickets.count()
        print('admin call:',total_ticket)
        # ticket_open = tickets.filter(status = 1).count()
        # ticket_reopened = tickets.filter(status  = 2).count()
        # ticket_resolved = tickets.filter(status = 3).count()
        # ticket_closed = tickets.filter(status= 4).count()
        # ticket_duplicate = tickets.filter(status = 5).count()
    if request.user.groups == 'operator':
        tickets = request.user.operator.ticket_set.all()
        total_ticket = tickets.count()
        print('operator call:',total_ticket)
        # ticket_open = tickets.filter(status = 1).count()
        # ticket_reopened = tickets.filter(status = 2).count()
        # ticket_resolved = tickets.filter(status = 3).count()
        # ticket_closed = tickets.filter(status= 4).count()
        # ticket_duplicate = tickets.filter(status = 5).count()
    dic = {
        'ticket_open' : ticket_open,
        'ticket_closed' : ticket_closed,
        'total_ticket' : total_ticket,
        'ticket_reopened':ticket_reopened,
        'ticket_duplicate':ticket_duplicate,
        'ticket_resolved':ticket_resolved,  
    }
    return render(request, 'ticket/home.html',dic)


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator'])
def createTicket(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            new_form =  ticket_form.save(commit=False)
            new_form.created_by =request.user.operator
            new_form.save()
            return redirect('all_tickets')
    return render(request, 'ticket/ticket.html', {'ticket_form': ticket_form})


def deleteTicket(request):
    pass


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator'])
def updateTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            new_form =  ticket_form.save(commit=False)
            new_form.created_by =request.user.operator
            new_form.save()
            return redirect('all_tickets')
    return render(request, 'ticket/ticket.html', {'ticket_form': ticket_form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator','admin'])
def allTicket(request):
    tickets_object = request.user.operator.ticket_set.all()
    paginator = Paginator(tickets_object,10)
    query = request.GET.get('query') if request.GET.get('query') != None else ''
    tickets = tickets_object.filter(
        Q(contact__icontains=query) |
        Q(first_name__icontains=query)
    )
    return render(request, 'ticket/allticket.html', {'tickets': tickets})


def search(request):
    tickets_object = request.user.operator.ticket_set.all()
    query = request.GET.get('query') if request.GET.get('query') != None else ''
    tickets = tickets_object.filter(
        Q(contact__icontains=query) |
        Q(first_name__icontains=query)
    )
    return render(request, 'ticket/allticket.html', {'tickets': tickets})