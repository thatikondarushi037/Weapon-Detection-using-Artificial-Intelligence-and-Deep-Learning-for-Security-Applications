from django.shortcuts import render,HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.core.files.storage import FileSystemStorage


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})
def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})
def UserHome(request):
    return render(request, 'users/UserHome.html', {})


def UserSurveillance(request):
    import os
    import subprocess
    try:
        p = os.path.join(os.getcwd(), 'media', 'models', 'yolo.py')
        print(p)
        process = subprocess.call(['python', p, '--webcam', 'arg2'])
        # output =subprocess.run(p,capture_output=True,shell=False)
        # exitstatus = process.poll()
        return render(request, 'users/UserHome.html', {})
    except Exception as ex:
        return render(request, 'users/UserHome.html', {})


def UserViewImages(request):
    return render(request, 'users/viewDataset.html',{})

def modelTraing(request):
    # from .utility.trainingUtility import startModelBuilding
    # h = startModelBuilding()
    return render(request,'users/modelresults.html',{})

def UserImageTest(request):
    if request.method == 'POST':
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        from .utility import weaponr_predictions
        result = weaponr_predictions.start_prediction(filename)
        print('Result:', result)
        return render(request, "users/test_form.html", {"result": result, "path": uploaded_file_url})
    else:
        return render(request, "users/test_form.html", {})
