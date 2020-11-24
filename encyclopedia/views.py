import markdown2

from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):


def newEntry(request, entry):


def edit(request, entry):


def random(request):


def search(request):
