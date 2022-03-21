from tkinter import OFF
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import random

from . import util

from markdown2 import Markdown

#The styling of the form fields is being overridden by the default django style because we're using django form widgets. 
#Need to change widget styling by creating an attributes dictionary (which can use Bootstrap)
class newEntryForm(forms.Form):
    entryTitle = forms.CharField(widget=forms.TextInput(attrs={'id' : 'newEntryTitle','placeholder': 'Title', 'class': 'form-control', 'autofill': OFF}))
    entryText = forms.CharField(widget=forms.Textarea(attrs={'id' : 'newEntryText', 'placeholder': 'Your text here', 'class': 'form-control', 'autofill': OFF}))
    edit = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)

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
           "entryTitle": entry,
       })

def search(request):
    value = request.GET.get('q','')
    subStringEntries = []
    for entry in util.list_entries():
        if value.upper() in entry.upper():
            subStringEntries.append(entry)
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': value}))
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
            if(util.get_entry(entryTitle) is None or form.cleaned_data["edit"] is True):
                util.save_entry(entryTitle, entryText)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': entryTitle}))
            else:
                return render(request, "encyclopedia/newPage.html", {
                    "form":form,
                    "alreadyExists": True,
                    "entry": entryTitle,
                })

        else:
            return render(request, "encyclopedia/newPage.html", {
            'form': form,
            'alreadyExists': False,
        })
    else:
        return render(request, "encyclopedia/newPage.html", {
            'form': newEntryForm(),
            'alreadyExists': False,
    })

def edit(request, entry):
    entryText = util.get_entry(entry)
    if entryText is None:
        return render(request, "encyclopedia/noSuchEntry.html", {
            "entryTitle": entry,
        })

    else:
        form = newEntryForm()
        form.fields["edit"].initial = True
        form.fields["entryTitle"].initial = entry
        form.fields["entryTitle"].widget = forms.HiddenInput()
        form.fields["entryText"].initial = entryText
        
        return render(request, "encyclopedia/newPage.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["entryTitle"].initial
        })

def randomPage(request):
    entryList = []
    for entry in util.list_entries():
        entryList.append(entry)
    entryListRange = (len(entryList)-1)
    surpriseNumber = random.randint(0, entryListRange)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': entryList[surpriseNumber]}))