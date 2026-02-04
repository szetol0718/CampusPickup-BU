from multiprocessing import context
import random
import time
from django.shortcuts import render

DailySpecials = {
    "Hong Kong Style French Toast": 6.99,
    "Baked Pork Chop Rice": 12.99,
    "Milk Tea": 3.99,
    "Egg Tart": 4.99,
}

Menu = {    
    "Dim Sum": 12.99, 
    "Noodle Soup": 7.99,
    "BBQ Pork Bun": 5.99,
    "Congee": 8.99,
}


# Create your views here.
def restaurant(request):
    """
    Main page for the restaurant app
    URL: /restaurant/
    """
    template = "restaurant/main.html"

    context = {
        "current_time": time.ctime(),
               }
    return render(request, template, context)

def order(request):
    """
    Order page for the restaurant app
    URL: /restaurant/order/
    """

    template = "restaurant/order.html"
    special_name = random.choice(list(DailySpecials.keys()))
    special_price = DailySpecials[special_name]

    context = {
        "current_time": time.ctime(),
        "daily_special": special_name,
        "daily_special_price": special_price,
        "menu": Menu,
    }
    return render(request, template, context)
