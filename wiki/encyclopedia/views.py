from django.shortcuts import render, redirect

from . import util
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    """This function fetches the content of the entry page"""
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": html_content
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

        # Redirect after saving
        return redirect("entry_page", title=title)
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


def random_page(request):
    """Redirects to a random encyclopedia entry."""
    entries = util.list_entries()

    # If entries exist,
    if entries:
        # Select a random entry
        random_entry = random.choice(entries)

        # Redirect to the selected entry
        return redirect('entry_page', title=random_entry)
    else:

        # If no entries exist, display an error message
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
