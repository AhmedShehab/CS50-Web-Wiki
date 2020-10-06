from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from . import util
import markdown2,random
# Create your views here.
def index(request):
    if request.method=="POST":
        elements=[]
        entries=util.list_entries()
        lower_entries=[x.lower() for x in entries]
        entry=request.POST["entry"]
        for track,i in enumerate(lower_entries):
            if entry.lower()==i:
                return HttpResponseRedirect(reverse("encyclopedia:entry",args=(entries[track],)))
        for track,i in enumerate(lower_entries):
            if entry.lower() in i:
                elements.append(entries[track])
        return render(request,"encyclopedia/similar.html",{
            "elements":elements,
            "entry":entry
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,entry):
    entered=util.get_entry(entry)
    if entered==None:
        return render(request,"encyclopedia/error.html",{
            "entry":entry
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":entry,
            "text":markdown2.markdown(entered)
        })    
def create(request):
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        if util.get_entry(title):
            return render(request,"encyclopedia/exists.html")
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("encyclopedia:entry",args=(title,)))
    else:
        return render(request,"encyclopedia/create.html")

def rand(request):
    entries=util.list_entries()
    element=random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry",args=(element,)))

def edit(request):
    if request.method=="POST":
        if "title"  not in request.POST:
            some=request.POST["some_Value"]
            content=request.POST["content"]
            entries=util.list_entries()
            if some in entries:
                pass
            util.save_entry(some,content)
            return HttpResponseRedirect(reverse("encyclopedia:entry",args=(some,)))
        else:
            text=util.get_entry(request.POST["title"])
            return render(request,"encyclopedia/edit.html",{
                "text":text,
                "title":request.POST["title"]
    })  