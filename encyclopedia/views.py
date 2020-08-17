from django.shortcuts import render

from . import util
import markdown2

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

def new_entry(request):
    return render(request, "encyclopedia/add_new_entry.html", {
        "entries": util.list_entries()
    })