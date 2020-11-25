from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
from markdown2 import Markdown

class EntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8','rows':4,'cols':15}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    mark = Markdown()
    page = util.get_entry(entry)
    if page == None:
        return render(request, "encyclopedia/noEntry.html", {
            "entryTitle": entry    
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": entry,
            "entry": mark.convert(page)   
        })

def search(request):
    return request

def newEntry(request):
    if request.method == "POST":
        entryForm = EntryForm(request.POST)
        if entryForm.is_valid():
            title = entryForm.cleaned_data["title"]
            content = entryForm.cleaned_data["content"]
            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={
                    'entry': title
                }))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form": entryForm,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": entryForm,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": EntryForm(),
            "existing": False
        })

def edit(request, entry):
    return request

def random(request):
    return request
