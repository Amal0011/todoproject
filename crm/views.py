from django.shortcuts import render,redirect
from django import forms
from django.views.generic import View
# Create your views here.
from crm.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control btn btn-outline-danger"}),
            "department":forms.TextInput(attrs={"class":"form-control btn btn-outline-danger"}),
            "gender":forms.Select(attrs={"class":"form-select btn btn-outline-danger"}),
            "salary":forms.NumberInput(attrs={"class":"form-control btn btn-outline-danger"}),
            "email":forms.EmailInput(attrs={"class":"form-control btn btn-outline-danger"}),
            "profile_pic":forms.FileInput(attrs={"class":"form-control btn btn-outline-danger"}),
            "address":forms.Textarea(attrs={"class":"form-control btn btn-outline-danger","rows":5})

        }

class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password1","password2"]

        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "last_name":forms.TextInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "email":forms.EmailInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "username":forms.TextInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "password":forms.PasswordInput(attrs={"class":"form-control btn btn-outline-success text-white"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control btn btn-outline-danger text-white"}))
    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control btn btn-outline-danger text-white"}))

    
class SignUpView(View):
    def get(self,request,*args,**kw):
        form = RegistrationForm()
        return render(request,"reg.html",{"form":form})
    def post(self,request,*args,**kw):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"reg.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kw):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kw):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pd = form.cleaned_data.get("password")
            usr = authenticate(request,username=uname, password=pd)
            print(usr)
            if usr:
                login(request, usr)
            return redirect("todo-list")
        return render(request,"login.html",{"form":form})



class EmployeeCreateView(View):
    def get(self,request,*args,**kw):
        form = EmployeeForm()
        return  render(request,"emp-add.html",{"form":form})
    def post(self,request,*args,**kw):
        form=EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("emp-list")
        return render(request,"emp-add.html",{"form":form})

class EmployeeListView(View):
    def get(self,request,*args,**kw):
        qs=Employee.objects.all()
        return render(request,"emp-list.html",{"employees":qs})
    
class EmployeeDetailView(View):
    def get(self,request,*args,**kw):
        print(kw)
        id = kw.get('pk')
        qs=Employee.objects.get(id=id)
        
        return render(request,"emp-detail.html",{"employee":qs})
    
class EmployeeDeleteView(View):
    def get(self,request,*args,**kw):
        print(kw)
        id = kw.get('pk')
        Employee.objects.get(id=id).delete()
        
        return redirect('emp-list')
    
class EmployeeEditView(View):
    def get(self,request,*args,**kw):
        id = kw.get("pk")
        emp = Employee.objects.get(id = id)
        form = EmployeeForm(instance = emp)
        return render(request,"emp-edit.html",{"form":form})
    
    def post(self,request,*args,**kw):
        id = kw.get('pk')
        emp = Employee.objects.get(id = id)
        form = EmployeeForm(request.POST, request.FILES, instance = emp)
        if form.is_valid():
            form.save()
            return redirect("emp-detail",pk=id)
        return render(request,"emp-edit.html",{"form":form})
    
    

def signout_view(request, *args, **kw):
    logout(request)
    return redirect("signin")
        


            