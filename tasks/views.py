from django.shortcuts import render,redirect
from django.views.generic import View
from tasks.models import todo
from django import forms
from django.contrib import messages

class TodoForm(forms.Form):
    task_name = forms.CharField()
    # user = forms.CharField()


class TodoCreateView(View):
    def get(self,request,*args,**kw):
        form = TodoForm()
        return render(request,"add.html",{"form":form})
# Create your views here.
 
    def post(self,request,*args,**kw):
        form = TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo.objects.create(**form.cleaned_data,user = request.user)
            messages.success(request,"Task successfully created")
            return redirect("todo-list")
        messages.error(request,"error")
        return render(request,"add.html",{"form":form})

class TodoListView(View):
    def get(self,request,*args,**kw):
        qs = todo.objects.filter(status=False, user = request.user).order_by("-date")
        return render(request,"list.html",{"todos":qs})

class TodoDetailView(View):
    def get(self,request,*args,**kw):
        id = kw.get('pk')
        qs = todo.objects.get(id=id)
        return render(request,"detail.html", {"todo":qs})
    
class TodoDeleteView(View):
    def get(self,request,*args,**kw):
        id = kw.get("pk")
        todo.objects.get(id=id).delete()
        messages.success(request,"task deleted")
        return redirect("todo-list")

class TodoEditView(View):
    def get(self,request,*args,**kw):
        print(kw)
        id=kw.get('pk')
        todo.objects.filter(id=id).update(status=True)
        messages.success(request,"Moved to completed tasks")
        return redirect("todo-list")
    
class TodoCompletedView(View):
    def get(self,request,*args,**kw):
        qs = todo.objects.filter(status=True).order_by("-date")
        return render(request,"completed.html",{"todos":qs})
