from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from Cacher import pickled

#Takes a Zipcode and budget and scrapes Yelp Website accordingly.
#Returns a dictionary of restaurants
@pickled
def yelp_restuarants(ZipCode, url_no):
  res = {}
  #Selects url to scrape based on the Budget
  if(url_no == 1):
      url = 'https://www.yelp.com/search?find_loc=' + ZipCode + '&start=0&attrs=RestaurantsPriceRange2.1'
  elif(url_no == 2):
      url = 'https://www.yelp.com/search?find_loc=' + ZipCode + '&start=0&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2'
  elif(url_no == 3):
      url = 'https://www.yelp.com/search?find_loc=' + ZipCode + '&start=0&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.3'
  else:
      url = 'https://www.yelp.com/search?find_loc=' + ZipCode + '&start=0&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.3,RestaurantsPriceRange2.4'
  
  #Number of attempts is restricted to 100
  for i in range(100):
    #Try Parsing the url
    try:
      html = urlopen(url)
    except HTTPError as e:
      print(e)
      return None
    #Read the HTML into a BS4 object
    soup = BeautifulSoup(html.read(), 'lxml')

    #Find all the tags for individual restaurants
    res_tags = soup.findAll("div", {"class" : "lemon--div__373c0__6Tkil arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"})


    index = 0  
    #Iterate through all the tags and get the attributes
    #If a particular attribute tag is missing, empty value "" is assigned.
    for i in range(len(res_tags)):
      #name
      try:
        name = res_tags[i].find("h3", {"class" : "lemon--h3__373c0__5Q5tF heading--h3__373c0__1n4Of alternate__373c0__1uacp"}).a.get_text().strip()
        index += 1
      except Exception:
        continue

      #phone
      try:
        phone = res_tags[i].find("div", {"class" : "lemon--div__373c0__6Tkil display--inline-block__373c0__2de_K border-color--default__373c0__2oFDT"}).get_text().strip()
      except Exception:
        phone = ""
      
      #address
      try:
        address = res_tags[i].find("address").get_text().strip()
      except Exception:
        address = ""
      
      #neighborhood
      try:
        neighborhood = res_tags[i].find("div", {"class" : "lemon--div__373c0__6Tkil u-space-t1 border-color--default__373c0__2oFDT"}).get_text().strip()
      except Exception:
        neighborhood = ""
      
      #rating
      try:
        rating = res_tags[i].find("span", {"class" : "lemon--span__373c0__1xR0D display--inline__373c0__1DbOG border-color--default__373c0__2oFDT"}).contents[0]['aria-label']
      except Exception:
        rating = ""
      
      #dollar
      try:
        dollar = res_tags[i].find("span", {"class" : "lemon--span__373c0__1xR0D text__373c0__2pB8f priceRange__373c0__2DY87 text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-bullet--after__373c0__1ZHaA"}).get_text().strip() 
      except Exception:
        dollar = ""

      #review
      try:
        review = res_tags[i].find("p", {"class" : "lemon--p__373c0__1hkz1 text__373c0__2pB8f text__373c0__2P1WD alternateStyling__373c0__2ithU text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_"}).contents[0].strip()
      except Exception:
        review = ""

      #Add restaurants to the result dictionary with index starting from 1..
      res[index] = {"name" : name, "phone" : phone, "address" : address \
                ,"neighborhood": neighborhood, "rating" : rating, "dollar" : dollar \
              ,"review" : review}

    if len(res) != 0:
      break  
  return res 


#Test code for Yelp and save result set to Excel to verify the Yelp scrapper
if __name__ == '__main__':  
  Area = ['15217', '60612']
  Sheet = ['pittsburghClean', 'chicagoClean']
  Budget = [100, 50]
  writer = pd.ExcelWriter('yelp_output.xlsx')
  for index in range(len(Area)):
    for i in range(1):
      res_dict = yelp_restuarants(Area[index], )
      if(len(res_dict) != 0):
        print("Requests: ", i)
        break

    res_df = pd.DataFrame(res_dict).T
    print(res_df.head())
    res_df.to_excel(writer, Sheet[index])
  writer.save()