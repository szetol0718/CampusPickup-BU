from multiprocessing import context
import random
import time
from django.shortcuts import render

DailySpecials = {
    "Hong Kong Style French Toast": 5.99,
    "Pineapple Bun with Butter": 3.99,
    "Spam Indomie Goreng": 6.49,
    "Egg Tart": 4.99,
}

Menu = {
    "Satay Beef Noodles": 7.99,
    "Yang Chow Fried Rice": 9.99,
    "Beef Chow Fun": 9.49,
    "Minced Beef with Egg over Rice": 8.99,
    "Hong Kong Style Milk Tea": 3.99,
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

def confirmation(request):
    """
    Order confirmation page for the restaurant app
    URL: /restaurant/confirmation/
    """

    template = "restaurant/confirmation.html"
    if request.POST:

        customer_name = request.POST['customer_name']
        customer_phone = request.POST['customer_phone']
        customer_email = request.POST['customer_email']
        special_instructions = request.POST['special_instructions']

        ordered_items = []
        total_price = 0.0

        for item in Menu.keys():
            if item in request.POST:
                ordered_items.append((item, Menu[item]))
                total_price += Menu[item]

        for item in DailySpecials.keys():
            if item in request.POST:
                ordered_items.append((item, DailySpecials[item]))
                total_price += DailySpecials[item]

    context = {
        "current_time": time.ctime(),
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "customer_email": customer_email,
        "special_instructions": special_instructions,
        "ordered_items": ordered_items,
        "total_price": total_price,
    }
    return render(request, template, context)