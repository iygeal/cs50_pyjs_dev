from django.shortcuts import render, redirect

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


def search(request):
    """This function handles the search functionality"""

    # Get the search query from the request
    query = request.GET.get("q", "").strip()

    if query:
        entries = util.list_entries()  # Get all entries
        matched_entry = next(
            (entry for entry in entries if entry.lower() == query.lower()), None)

        if matched_entry:
            # Exact match: Redirect to the entry page
            return redirect("entry_page", title=matched_entry)

        # Partial matches (substring search)
        results = [entry for entry in entries if query.lower()
                   in entry.lower()]

        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })

    return redirect("index")  # If no query, go back to index
