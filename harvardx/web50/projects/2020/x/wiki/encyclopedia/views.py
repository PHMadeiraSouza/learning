from random import choice
from django.shortcuts import render
from django.http import Http404,HttpResponse
import markdown2
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_md(title):
    md_page = util.get_entry(title)
    markdowner = Markdown()
    if md_page is None:
        return None

    return markdowner.convert(md_page)

def Html_page(request,title):
    html_content = convert_md(title)
    if html_content is not None:
        return render(request,"encyclopedia/entry.html",{
        'title': title,
        'content': html_content,
    })
    return render(request,"encyclopedia/error.html",{
                    "message":"this entry page already exists"
            })

def create_page(request):
        if request.method == "GET":
            return render(request,"encyclopedia/create.html")
        else:
            title = request.POST['create_title']
            content = request.POST['create_content']
            title_exists = util.get_entry(title)
            if title_exists is not None:
                return render(request, "encyclopedia/error.html",{
                    "message":"this entry page already exists"
                })
            else:
                util.save_entry(title, content)
                new_page = convert_md(title)
                return render(request, "encyclopedia/entry.html",{
                    'title': title,
                    'content': new_page,
                })
def edit_page(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title": title,
            "content": content,
        })

def save_edit(request):
     if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        new_page = convert_md(title)
        return render(request, "encyclopedia/entry.html",{
                    'title': title,
                    'content': new_page,
                })
                
def search(request):
    title = request.GET['search_title']
    entry_exists = util.get_entry(title)
    if entry_exists is not None:
        html_content = convert_md(title)
        return render(request, "encyclopedia/entry.html",{
            'title': title,
            'content': html_content,
        })
    else:
        all_entries = util.list_entries()
        recomendations = []
        for entry in all_entries:
            if title.lower() in entry.lower():
                recomendations.append(entry)
        return render(request, "encyclopedia/search_result.html", {
            'recomendations': recomendations
        })
def random(request):
    page_title = choice(util.list_entries())
    page_content = convert_md(page_title)
    return render(request, "encyclopedia/entry.html",{
            'title': page_title,
            'content': page_content,
        })