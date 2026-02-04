from multiprocessing import context
import random
from django.shortcuts import render

DailySpecials = [
    "Hong Kong Style French Toast",
    "Baked Pork Chop Rice",
    "Milk Tea",
    "Egg Tart",
    ]
# Create your views here.
def restaurant(request):
    """
    Main page for the restaurant app
    URL: /restaurant/
    """
    template = "restaurant/main.html"
    return render(request, template)

def order(request):
    """
    Order page for the restaurant app
    URL: /restaurant/order/
    """

    template = "restaurant/order.html"

    context = {
        "daily_specials": random.choices(DailySpecials)
    }
    return render(request, template, context)