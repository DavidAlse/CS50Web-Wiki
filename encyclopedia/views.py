from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util
import encyclopedia
from markdown2 import Markdown

class newEntryForm(forms.Form):
    entryTitle = forms.CharField(label='New Entry')
    entryText = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries
    })

def entry(request, entry):
   markdowner = Markdown()
   entryPage = util.get_entry(entry)
   if entryPage is None:
       return render(request, "encyclopedia/noSuchEntry.html") 
   else:
       return render(request, "encyclopedia/entry.html", {
           "entry": markdowner.convert(entryPage),
       })

def search(request):
    value = request.GET.get('q','')
    subStringEntries = []
    for entry in util.list_entries():
        if value.upper() in entry.upper():
            subStringEntries.append(entry)
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    elif(len(subStringEntries) == 0):
        return render(request, "encyclopedia/noSuchEntry.html")
    else:      
        return render(request, "encyclopedia/index.html", {
        "entries": subStringEntries,
    })

def newPage(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            entryTitle = form.cleaned_data["entryTitle"]
            entryText = form.cleaned_data["entryText"]
            #do something here to store the new entry information
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/newPage.html", {
        'form': form
        })

    return render(request, "encyclopedia/newPage.html", {
        'form': newEntryForm()
    })