from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import JsonResponse
from .models import File, UploadedFile, UserProfile
from io import TextIOWrapper
from .forms import UserCreationForm
import os
import csv

def uploaded_data_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'data': 'Invalid file format. Please upload a CSV file.'})

        try:
            decoded_file = TextIOWrapper(uploaded_file.file, encoding=request.encoding)
            csv_reader = csv.DictReader(decoded_file)
        except Exception as e:
            return JsonResponse({'data': 'Error reading CSV file.'})
        
        csv_fields = csv_reader.fieldnames

        required_fields = ['id', 'name', 'domain', 'year_founded', 'industry', 'size_range', 'locality', 'country',
                           'linkedin_url', 'current_employee_estimate', 'total_employee_estimate']

        if not all(field in csv_fields for field in required_fields):
            return JsonResponse({'data': 'CSV file is missing required fields.'})

        for row in csv_reader:
            uploaded_file_instance = UploadedFile(
                id=row['id'],
                name=row['name'],
                domain=row['domain'],
                year_founded=int(row['year_founded']),
                industry=row['industry'],
                size_range=row['size_range'],
                locality=row['locality'],
                country=row['country'],
                linkedin_url=row['linkedin_url'],
                current_employee_estimate=int(row['current_employee_estimate']),
                total_employee_estimate=int(row['total_employee_estimate']),
            )
            uploaded_file_instance.save()

        return JsonResponse({'data': 'File uploaded successfully.'})

    elif request.method == 'GET':
        return render(request, 'home.html')

    else:
        return JsonResponse({'data': 'Invalid request method.'})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        return redirect('uploaded_data')

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'register.html')
    

def query_builder(request):
    if request.method == 'POST':

        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')
        field3 = request.POST.get('field3')
        field4 = request.POST.get('field4')
        field5 = request.POST.get('field5')
        field6 = request.POST.get('field6')
        field7 = request.POST.get('field7')
        field8 = request.POST.get('field8')

        search_criteria = {
            'name__icontains': field1,
            'domain__icontains': field2,
            'industry__icontains': field3,
            'size_range__icontains': field4,
            'locality__icontains': field5,
            'country__icontains': field6,
            'linkedin_url__icontains': field7,
            'year_founded__icontains': field8,
        }

        search_criteria = {key: value for key, value in search_criteria.items() if value is not None}

        matched_results = UploadedFile.objects.filter(**search_criteria)

        return render(request, 'query_result.html', {'results': matched_results})

    return render(request, 'query.html')


def user(request):
    users_data = UserProfile.objects.all()
    context = {'users_data': users_data}
    return render(request, 'user.html', context)


def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)

            if not created:
                user_profile.status = 'Active'
                user_profile.save()
            messages.success(request, 'New user added successfully!')
            return redirect('user')  
    else:
        form = UserCreationForm()

    return render(request, 'add_user.html', {'form': form})
