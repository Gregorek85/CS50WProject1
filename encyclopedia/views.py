from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from django.http import HttpResponse

class new_entry_form(forms.Form):
    entry = forms.CharField(label="New Entry Name:",max_length=20)
    entry_content =forms.CharField(label="Description", min_length=20, widget=forms.Textarea())

class search_form(forms.Form):
    q=forms.CharField(max_length=15,widget=forms.Select(attrs={'onchange': 'submit();'}))


def index(request):
    message ="All Pages"
    entries = util.list_entries()
    if request.method == "POST":
        form = search_form(request.POST)
        if form.is_valid():
            q= str(form.cleaned_data["q"]).lower()
            #check if we have a direct match
            for entry in entries:
                if str(entry).lower() == q:
                    return HttpResponseRedirect(reverse('entry', args=(q,)))
            #otherwise check if we have partial match:
            matching = [s for s in entries if q.lower() in s.lower()]
            if len(matching) > 0:
                entries = matching
                message = "Search Results"
            else:
                #nothing found
                return HttpResponseRedirect(reverse('entry', args=("No_Search_Result",)))
            
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "message":message
    })

def entry(request, entry):
    if entry == "No_Search_Result":
        entry_content = "**Sorry, nothing found**"
    else:
        entry_content = util.get_entry(entry)
        if entry_content is None:
            entry_content = util.get_entry('NoneZ4#')
            entry = "Not found.."
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entry_content" : markdown2.markdown(entry_content)
    })
def random(request):
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