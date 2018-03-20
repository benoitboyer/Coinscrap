from django.shortcuts import render
from .forms import ScrapForm
import requests
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
	form= ScrapForm()
	return render(request, 'mycoins/base.html',{'form':form})

def scrap_coin(request):

	#get the needed page to scrap
	page = requests.get("https://coinmarketcap.com/currencies/siacoin/historical-data/?start=20130428&end=20171025")
	soup = BeautifulSoup(page.content, 'html.parser')
	
	#get only raw data we need
	table_data= soup.tbody
	
	#extract all td tags
	tr_data=table_data.find_all('tr')
	
	date_val=[]
	high_val=[]
	low_val=[]

	#for each tr tag get all needed td tags and extract them
	for tr in tr_data:
		td = tr.find_all('td')
		row= [i.text for i in td]
		date_val.append(row[0])
		high_val.append(row[2])
		low_val.append(row[3])

	#process extracted data and return them 
	max_val=max(high_val, key=float)
	max_date_key=high_val.index(max_val)
	max_date_val=date_val[max_date_key]
	
	min_val=min(low_val, key=float)
	min_date_key=low_val.index(min_val)
	min_date_val=date_val[min_date_key]
	
	
	return render(request,'mycoins/index.html',{'max_val':max_val, 'min_val':min_val, 'max_date_val':max_date_val,'min_date_val':min_date_val})