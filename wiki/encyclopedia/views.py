from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    """This function fetches the content of the entry page"""

    entries = util.list_entries()
    formatted_title = next(
        (entry for entry in entries if entry.upper() == title.upper()), title)

    content = util.get_entry(formatted_title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry_page.html", {
        "title": formatted_title,
        "content": content
    })
