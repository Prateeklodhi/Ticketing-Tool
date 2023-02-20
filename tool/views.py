from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, UserRegistrationForm, OperatorProfile, NidanForm
from .models import Ticket, Operator, NidanTicket
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from .forms import UserRegistrationForm
from .decorators import unauthorized_user, allowed_users, admin_only
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NidanSolvedSerializer

# Create your views here.
@unauthorized_user
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, 'Welcome, you have been logged in successfully.')
            return redirect('index')
        else:
            messages.error(request, 'username or password might be wrong.')
    return render(request, 'credential/login.html')


def logoutuser(request):
    messages.success(request, 'Logout Successfully')
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['admin',])
def registeruser(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 'Account Created Successfully For '+username)
            return redirect('index')
    dic = {
        'user_form': form,
    }
    return render(request, 'credential/register.html', dic)


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator'])
def userSettings(request):
    operator_id = request.user
    operator = Operator.objects.get(user=operator_id)
    form = OperatorProfile(instance=operator)
    if request.method == 'POST':
        form = OperatorProfile(request.POST, request.FILES, instance=operator)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile has been updated successfully.')
        else:
            messages.error(request, 'Something went wrong.')
    dic = {
        'form': form,
    }
    return render(request, 'ticket/userprofile.html', dic)


# Nidan flows starts from here 
@login_required(login_url='login')
# @allowed_users(allowed_roles=['operator'])
def api_nidan(request): # to retrive all the nidan api data and store it in to the data base if data already exsists it drop the save function and if new data will arrive it will take the data as pending data and save it into the data base.
    message_flag = None
    response_data = None
    if request.method == 'GET':
        url = 'https://uat3.cgg.gov.in/cggrievancemmu/getDocketDetails'
        response = requests.get(url)
        data = response.json()
        response_data = data['data']
        for glpi_client in response_data:
            client = NidanTicket(
            docket_number = glpi_client['docketNo'],
            citizen_name = glpi_client['citizenName'],
            phone =glpi_client['phone'],
            address =glpi_client['address']+' '+glpi_client['houseNo']+' '+ glpi_client['colonyName']+' '+glpi_client['districtName'],
            email =glpi_client['email'],
            municipality =glpi_client['municipality'],
            section =glpi_client['section'],
            message =glpi_client['message'],
            subsection =glpi_client['subsection'],
            status =glpi_client['status'],
            grievance_remark =glpi_client['grievanceRemarks'],
            callstart  =glpi_client['callStart'],
            )
            try:
                client.save()
                message_flag = True
            except:
                message_flag = False
    if message_flag == True:
        messages.success(request, 'New data is arrived')
    else:
        messages.warning(
            request, 'All data have been fatched from the Nidan Api')
    nidan_tickets = NidanTicket.objects.all()
    dic = {
        'nidan_tickets': nidan_tickets,
    }
    return render(request, 'ticket/nidan_all_tickets.html', dic)


@login_required(login_url='login')
def nidanTicketData(request,pk):
    nidan_instance = get_object_or_404(NidanTicket,id=pk)
    nidan_form = NidanForm(request.POST or None,instance=nidan_instance)
    if nidan_form.is_valid():
        nidan_form_status = nidan_form.save(commit=False)
        if nidan_form_status.status == 'solved':
            nidan_form_status.save()
            messages.success(request,'Docket for '+ str(nidan_instance)+" is solved now.")
            return redirect('api_nidan')
        else:
            messages.warning(request,'No changes detacted.')
    dic = {
        'nidan_form':nidan_form,
        'nidan_instance':nidan_instance,
    }
    return render(request,'ticket/nidan_form.html',dic)


@login_required(login_url='login')
def nidan_pending_data(request):
    nidan_tickets = NidanTicket.objects.filter(status='pending')
    dic = {
         'nidan_tickets': nidan_tickets,
    }
    return render(request,'ticket/nidan_pending_tickets.html',dic)


# to show all the solved data of the nidan api
@login_required(login_url='login')
def nidan_solved_data(request):
    nidan_tickets = NidanTicket.objects.filter(status='solved')
    dic = {
        'nidan_tickets': nidan_tickets,
    }
    return render(request,'ticket/nidan_solved_tickets.html',dic)


#this api will return all the sovled docket number 
@api_view(['GET'])
def nidanSolvedList(request):
    nidansolved = NidanTicket.objects.filter(status='solved')
    print(nidansolved)
    nidanserializer = NidanSolvedSerializer(nidansolved,many=True)
    return Response(nidanserializer.data)


#this api will return selected sovled docket number 
@api_view(['GET'])
def nidanSolvedDetail(request,dcnum):
    Nidansolvedticket= NidanTicket.objects.get(docket_number=dcnum)
    nidanserializer = NidanSolvedSerializer(Nidansolvedticket,many=False)
    return Response(nidanserializer.data)


#this is the home page of ticketing tool webapplication allowed user for this page are admin and operator.
@login_required(login_url='login')
@allowed_users(allowed_roles=['operator', 'admin'])
def index(request):
    if str(request.user.groups.all()[0]) == 'admin':
        tickets = Ticket.objects.all()
        total_ticket = tickets.count()
        ticket_open = tickets.filter(status=1).count()
        ticket_reopened = tickets.filter(status=2).count()
        ticket_resolved = tickets.filter(status=3).count()
        ticket_closed = tickets.filter(status=4).count()
        ticket_duplicate = tickets.filter(status=5).count()
    if str(request.user.groups.all()[0]) == 'operator':
        tickets = request.user.operator.ticket_set.all()
        total_ticket = tickets.count()
        ticket_open = tickets.filter(status=1).count()
        ticket_reopened = tickets.filter(status=2).count()
        ticket_resolved = tickets.filter(status=3).count()
        ticket_closed = tickets.filter(status=4).count()
        ticket_duplicate = tickets.filter(status=5).count()
    dic = {
        'section':'index',
        'ticket_open': ticket_open,
        'ticket_closed': ticket_closed,
        'total_ticket': total_ticket,
        'ticket_reopened': ticket_reopened,
        'ticket_duplicate': ticket_duplicate,
        'ticket_resolved': ticket_resolved,
    }
    return render(request, 'ticket/home.html',dic)


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator'])
def createTicket(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            new_form = ticket_form.save(commit=False)
            new_form.created_by = request.user.operator
            new_form.save()
            messages.success(request, 'Ticket created succfully for ' +str(new_form.first_name+" "+new_form.last_name+'.'))
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
            new_form = ticket_form.save(commit=False)
            new_form.created_by = request.user.operator
            new_form.save()
            messages.success(request, 'Ticket updated succfully for ' +
                             str(new_form.first_name+" "+new_form.last_name+'.'))
            return redirect('all_tickets')
    return render(request, 'ticket/ticket.html', {'ticket_form': ticket_form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['operator', 'admin'])
def allTicket(request):
    if str(request.user.groups.all()[0]) == 'admin':
        tickets_object = Ticket.objects.all()
    if str(request.user.groups.all()[0]) == 'operator':
        tickets_object = request.user.operator.ticket_set.all()
    query = request.GET.get('query') if request.GET.get(
        'query') != None else ''
    tickets = tickets_object.filter(
        Q(contact__icontains=query) |
        Q(first_name__icontains=query)
    )
    return render(request, 'ticket/alltickets.html', {'tickets': tickets})




