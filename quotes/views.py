# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 1/28/2026
# Description: Django view functions for the quotes application.
# The app displays random Confucius (Kong Qiu) quotes and images,
# plus pages to show all quotes/images and an about page.


from django.shortcuts import render
import random
import time

#quotes list 
QUOTES = [
    "It does not matter how slowly you go as long as you do not stop.",
    "Our greatest glory is not in never falling, but in rising every time we fall.",
    "The man who moves a mountain begins by carrying away small stones.",
    "To see what is right and not do it is the want of courage.",
    "Real knowledge is to know the extent of one’s ignorance.",
    "Choose a job you love, and you will never have to work a day in your life.",
    "What the superior man seeks is in himself; what the small man seeks is in others.",
    "Do not impose on others what you yourself do not desire.",
    "Virtue is not left to stand alone. He who practices it will have neighbors.",
    "Better a diamond with a flaw than a pebble without."
]
#images list
IMAGES = [
    "images/i1.jpg",
    "images/i2.jpg",
    "images/i3.jpg",
    "images/i4.jpg",
] 



#handle quote request
def quote(request):
    """
    Main page:
    Displays ONE random quote and ONE random image
    URL: / and /quote
    """
    context = {
        "quote": random.choice(QUOTES), #randomly select 1 quote from the list
        "image": random.choice(IMAGES), #randomly select 1 image from the list
        "current_time": time.ctime(),
    }
    template = "quotes/quote.html"
    return render(request, template, context)

#handle show_all request
def show_all(request):
    """
    Show all quotes and images
    URL: /show_all
    """
    context = {
        "quotes": QUOTES, #all quotes
        "images": IMAGES, #all images
        "current_time": time.ctime(),
    }
    template = "quotes/show_all.html"
    return render(request, template, context)

#handle about request
def about(request):
    """
    About page
    URL: /about
    """
    context = {
        "current_time": time.ctime(),
    }
    template = "quotes/about.html"
    return render(request, template, context)
