from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

class new_entry_form(forms.Form):
    entry = forms.CharField(label="New Entry Name:",max_length=20)
    entry_content =forms.CharField(label="Description", min_length=20, widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entry_content = util.get_entry(entry)
    if entry_content is None:
        entry_content = util.get_entry('NoneZ4#')
        entry = "Not found.."
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entry_content" : markdown2.markdown(entry_content)
    })
def random(request):
    print(request)
    entry = util.get_random_entry()
    return HttpResponseRedirect(reverse('entry', args=(entry,)))

def new_entry(request):
    message = ""
    if request.method == "POST":
        form = new_entry_form(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            new_entry_content = form.cleaned_data["entry_content"]
            #Check if the entry exists
            old_entry_content = util.get_entry(entry)
            if old_entry_content is None: #then it is ok to add new
                util.save_entry(entry, new_entry_content)
                return HttpResponseRedirect(reverse('entry', args=(entry,)))
            else:
                message = f'Error: Sorry, but the entry for {entry} already exists. Either choose a different name or edit it'
    else:
        form = new_entry_form()
    return render(request, "encyclopedia/add_new_entry.html", {
        "form": form,
        "message": message
    })