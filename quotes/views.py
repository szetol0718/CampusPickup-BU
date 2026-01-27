from django.shortcuts import render
import random
import time



QUOTES = [
    "The only thing we have to fear is fear itself.",
    "In the middle of difficulty lies opportunity.",
    "Life is what happens when you're busy making other plans."
]


# --------------------------------------------------
# Views
# --------------------------------------------------

def quote(request):
    """
    Main page:
    Displays ONE random quote and ONE random image
    URL: / and /quote
    """
    context = {
        "quote": random.choice(QUOTES),
        "current_time": time.ctime(),
    }

    return render(request, "quotes/quote.html", context)


def show_all(request):
    """
    Show all quotes and images
    URL: /show_all
    """
    context = {
        "quotes": QUOTES,
        "current_time": time.ctime(),
    }

    return render(request, "quotes/show_all.html", context)


def about(request):
    """
    About page
    URL: /about
    """
    context = {
        "current_time": time.ctime(),
    }

    return render(request, "quotes/about.html", context)
