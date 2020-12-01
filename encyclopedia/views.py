import random as rando
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from . import util
from markdown2 import Markdown

class EntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control col-md-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-md-8','rows':4,'cols':15}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def entry(request, entry):
    mark = Markdown()
    page = util.get_entry(entry)
    if page != None:
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": entry,
            "entry": mark.convert(page)   
        })
    else:
        return render(request, "encyclopedia/noEntry.html", {
            "entryTitle": entry    
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    term = request.GET.get('q','')
    if util.get_entry(term) != None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': term}))
    else:
        partialTerms = []
        for n in util.list_entries():
            if term.upper() in n.upper():
                partialTerms.append(n)
        if len(partialTerms) == 0:
            return render(request, "encyclopedia/noEntry.html")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": partialTerms,
                "search": True,
                "value": term
            })

def newEntry(request):
    if request.method == "POST":
        entryForm = EntryForm(request.POST)
        if entryForm.is_valid():
            title = entryForm.cleaned_data["title"].capitalize()
            content = entryForm.cleaned_data["content"]
            if util.get_entry(title) is None or entryForm.cleaned_data["edit"] is True:
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
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/noEntry.html", {
            "entryTitle": entry
        })
    else:
        form = EntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = page
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })

def random(request):
    randomize = rando.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": randomize}))
