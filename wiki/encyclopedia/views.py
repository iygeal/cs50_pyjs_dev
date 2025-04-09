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


def create_page(request):
    """This functuion handles the creation of a new page"""
    if request.method == "POST":
        # Get the title and content from the form submission
        title = request.POST.get("title").strip()
        content = request.POST.get("content")

        # Check if an entry with this title already exists (case-insensitive)
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with that title already exists."
            })

        # Save the new entry and redirect to its page
        util.save_entry(title, content)
        return redirect("entry_page", title=title)

    # For GET requests, render the new page form
    return render(request, "encyclopedia/create_page.html")


# Function to handle GET and POST requests for editing an existing page
def edit_page(request, title):
    """Handles the editing of an existing page"""
    if request.method == "POST":
        # Process the submitted form data
        content = request.POST.get("content")
        util.save_entry(title, content)
    else:
        # Display the edit form with current content
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })

        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })
