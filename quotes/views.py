from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
#from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']

		#https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_a761220ffee04e0e844a4b7a50e4bf62
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_a761220ffee04e0e844a4b7a50e4bf62")

		try:
			api = json.loads(api_request.content)

		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a ticker above"})


def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ('Stock Has been Added'))
			return redirect('add_stock')
	else: 
		ticker = Stock.objects.all()
		output = []

		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_a761220ffee04e0e844a4b7a50e4bf62")

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ('Item Has been deleted'))
	return redirect('delete_stock')	

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})