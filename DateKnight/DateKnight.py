import os
import Yelp as y
import numpy as np
import pandas as pd
from tabulate import tabulate
from pyfiglet import figlet_format
from pyfiglet import Figlet
from colorama import init
from termcolor import cprint
import textwrap
import Visual as v
import requests
import json  
from pandas.io.json import json_normalize
from Cacher import pickled
    
### VARIABLES ###
Budget = 0
Spent_Already = 0
ZipCode = ''
SelectedOptions = {}
res_df = pd.DataFrame()
ratings = pd.DataFrame()

### METHODS ###
def visualize():
    while True:
        display_title_bar()
        choice = input("Select your viz: \n1. Runtime vs frequency. Seeing the average runtime of latest movies\n2. Average Ratings vs frequency. Seeing the average ratings of latest movies.\nz. Go back\n")    
        if choice=='1':
            v.first()
        elif choice=='2':
            v.second()
        elif choice=='z':
            break
        else:
            print ("Invalid choice, please enter again.")

def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('cls')
    f = Figlet()
    cprint(f.renderText("Date Knight"), 'yellow', 'on_red')
    #display the Budget only if it's greater than 0
    if(Budget > 0):
        print('Budget: $', Budget, '\tSpent already: $' , Spent_Already)

def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Movie")
    print("[2] Restaurant")
    print("[v] Visualizations to help")
    print("[r] Reset\t\t\t[q] Quit")
    
    return input("What would you like to do? ")

@pickled
def get_movies():
    urlmovies = "https://api-gate2.movieglu.com/filmsNowShowing/"

    querystringmovies = {"n":"10"}
    headermovies = {
    'client': "DTKN",
    'x-api-key' : "ukxgLs4xQB3Vk4s9he3ff4Mj3BaBIfX92PrzwxsQ",
    'territory': "US",
    'authorization': "Basic U1RVRF8zODozVWI1QUdUOUFuVEo=",
    'device-datetime': "2018-12-04T15:30:49.478Z",
    'api-version': "v200",
    'cache-control': "no-cache",
    'postman-token': "bd520b1c-09b8-b3a3-cd5f-bcd545527663"
    }

    responsemovies = requests.request("GET", urlmovies, headers=headermovies, params=querystringmovies)
    return json.loads(responsemovies.text)  

@pickled
def parse_Zip(zipcode):
    urlzip = "https://www.zipcodeapi.com/rest/o8El8xsUKF2s8OqLln0d0U6cSug1wQO2vu9bRKJdKKUbrwH7iUIJr7XXIlNcpklK/info.json/"+zipcode+"/degrees"
    headerszip = {
      'cache-control': "no-cache",
      'postman-token': "o8El8xsUKF2s8OqLln0d0U6cSug1wQO2vu9bRKJdKKUbrwH7iUIJr7XXIlNcpklK"
     }


    responsezip = requests.request("GET", urlzip, headers=headerszip)
     
    return json.loads(responsezip.text)

@pickled
def get_showtimes(f_id, lat, long):
    url1 = "https://api-gate2.movieglu.com/filmShowTimes/"

    querystring = {"film_id":f_id,"date":"2018-12-04","n":"5"}

    headers = {
      'client': "DTKN",
      'x-api-key': "ukxgLs4xQB3Vk4s9he3ff4Mj3BaBIfX92PrzwxsQ",
      'territory': "US",
      'authorization': "Basic U1RVRF8zODozVWI1QUdUOUFuVEo=",
      'device-datetime': "2018-12-04T18:01:23.979Z",
      'api-version': "v200",
      'geolocation': lat+";"+long,
      'cache-control': "no-cache",
      'postman-token': "a22d9eaf-f626-5de8-5e78-e68f91ac3b05"
    }

    times= requests.request("GET", url1, headers=headers, params=querystring)
    return json.loads(times.text)

def show_movies():
    global ratings
    print("\nHere are the movies I know.\n")
    
    json_movies = get_movies()

    resultmovies=json_normalize(json_movies['films'])
    
    print("********************Please Select a Movie*************************")
    #####displays film_id, imdb_id, film_name
    
    l2=resultmovies['imdb_id'].tolist()
    rate = []
    runtime = []
    genre = []
    votes = []
    final = []
   
    for x in l2:
       ratings2 = ratings.loc[ratings['tconst']==x]
       genre = (ratings2['genres'].tolist())
       name = (ratings2['primaryTitle'].tolist())
       rate = (ratings2['averageRating'].tolist())
       runtime = (ratings2['runtimeMinutes'].tolist())
       final.append(name+rate+genre+runtime)
       
   
    show = pd.DataFrame(final,columns=['Movie Title','IMDB Rating','Genre','Runtime'])
    print(tabulate(show,headers="keys"))
    
    movie_choice=input("Movie Choice: ")
    mc=int(movie_choice)

    json_zip =   parse_Zip(ZipCode)

#Extract lat,long,city,state from response
    lat=str(json_zip['lat'])
    long=str(json_zip['lng'])
    city=json_zip['city']
    state=json_zip['state']
    f_id=resultmovies.loc[mc,'film_id'] ##based on user selection


    times_json = get_showtimes(f_id, lat, long)

    count1 = 1
    tempDict = {}
    
    for x in times_json["cinemas"]:
      
      print ("\n\n",count1,x["cinema_name"])
      print ("     Show timings:")
      tempDict[count1]=x["cinema_name"]
      count1 = count1 + 1
      count = 0
      for z in x["showings"]["Standard"]["times"]:
     
        print ("          ",z["start_time"],end=" ")
        count = count + 1
        if(count==3):
          count = 0
          print ("\n")
        
    
    choice = input("\n\nEnter your choice of cinema from above:")
    count=0

    dummy = int(choice)
    
   
    print ("\nYou have selected",tempDict[dummy])
    
    count = 1
    tempDict2 = {}
    for x in times_json["cinemas"]:
        if x["cinema_name"] == tempDict[dummy]:
            for z in x["showings"]["Standard"]["times"]:
                #print ('xya')
                print ("          ",count,"]",z["start_time"],end=" ")
                tempDict2[count]=z["start_time"]  
                count = count + 1
                
                
    choice2 =  input("\n\nSelect a timing from the list given above:")
    dummy2 = int(choice2)
   
 
    
    global Spent_Already
    global SelectedOptions
    if None is SelectedOptions.get('movie', None):
        Spent_Already += 16
    detList = [tempDict[dummy],final[mc][0],tempDict2[dummy2]]
    SelectedOptions['movie']=[detList]    
    return resultmovies.loc[mc,'film_id']

#Calls the method from Yelp Web Scrapper
#Top 10 restuarants based on the location and budget is returned in a data frame
def get_restuarants():
    res_dict = {}
    ret = pd.DataFrame()
    if(Budget < 20):
        url_no = 1
    elif(Budget < 60):
        url_no = 2
    elif(Budget < 120):
        url_no = 3
    else:
        url_no = 4
  
    res_dict = y.yelp_restuarants(ZipCode, url_no)
    if res_dict is None:
        print('Aw, Snap! Restaurants are not available.')
        return None
    elif len(res_dict) != 0:
        ret = pd.DataFrame(res_dict).transpose()
    else:
        pass
    
    return ret
    

#Displays restaurants in a tabular format
def show_restuarants():
    #clear screen
    display_title_bar()
    print("\nHere are the restuarants I know..\n")  
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        res_print = res_df.loc[:,['name', 'dollar']]
        print(tabulate(res_print, headers='keys', tablefmt='psql'))
    #Restaurant selection method is called
    select_restaurant()
    
#User is prompted to restaurants from the table with inputs from 1 - 10
#User can also go back to the main menu, by selecting 'z'
def select_restaurant():
    global SelectedOptions
    global Spent_Already

    print('[z] Go back')
    selection = 0
    while(True):
        try:
            selection = input('\nEnter your selection: ')
            #Go back option
            if(selection == 'z'):
                return None
            #Basic checks for valid input
            if(int(selection) in res_df.index.values):
                break
            else:
                raise Exception('Error')
        except:
            print('Invalid selection, please enter again')
    
    #Refresh screen with the updated selection
    display_title_bar()

    #Display information about the selected restaurant
    print('Your selected restuarant:')
    res_details = res_df.loc[int(selection)]
    res_details1 = pd.Series.to_frame(res_details[['name', 'dollar', 'address',\
     'neighborhood', 'phone', 'rating']])
    print(tabulate(res_details1, tablefmt='presto'))
    print(textwrap.fill(res_details['review'], 40))
    
    #Prompt the user if he wants to select this restaurant
    #Based on his selection, the budget will be updated
    #Only one restaurant can be selected, 
    #hence if other restaurant is already selected, it will be replaced
    #and budget will be updated accordingly
    #User can go back, by selecting 'n'
    while(True):
        if None is SelectedOptions.get('restaurant', None):    
            temp = input('Would you like to select this restaurant?(y/n)')
        else:
            temp = input('You have already selected one. Do you want to change?(y/n)')
            #Logic to update price, if the restaurant is already selected.
            if temp == 'y':
                _rem_price = 0
                _rem_dollar = SelectedOptions['restaurant']['dollar']
                print(_rem_dollar)
                if _rem_dollar == '$':
                    _rem_price = 20
                elif _rem_dollar == '$$':
                    _rem_price = 60
                elif _rem_dollar == '$$$':
                    _rem_price = 120
                else:
                    _rem_price = 150

                Spent_Already -= _rem_price        

        _dollar = res_df.loc[int(selection), 'dollar']
        price = 0
        if _dollar == '$':
            price = 20
        elif _dollar == '$$':
            price = 60
        elif _dollar == '$$$':
            price = 120
        else:
            price = 150
        
        if('y' == temp):
            SelectedOptions['restaurant'] = res_df.loc[int(selection)]
            Spent_Already += price
            break
        elif('n' == temp):
            show_restuarants()            
            break
        else:            
            print('Please enter a valid selection')

#Prints a report at the end of all the selections
def print_report():
    global SelectedOptions
    if None is not SelectedOptions.get('restaurant', None):
        print('Here''s the restaurant..')    
        print(tabulate(pd.Series.to_frame(SelectedOptions['restaurant'][['name', 'address','neighborhood','phone']]), tablefmt='psql'))
    if None is not SelectedOptions.get('movie', None):
        print('Here''s the movie..')    
        print(tabulate(pd.DataFrame(SelectedOptions['movie'])))

#Global reset and prompts user to select his location and budget again
def reset():
    global Budget
    global Spent_Already
    global ZipCode
    global SelectedOptions
    global res_df
    
    Budget = 0
    Spent_Already = 0
    ZipCode = ''
    SelectedOptions = {}
    res_df = pd.DataFrame()

#Method to get inputs from the user, with validation of the input
def get_inputs():
    global Budget
    global ZipCode    
    display_title_bar()

    #Get inputs, validate the inputs
    mes = 'How much do you love to spend?'
    #Validate budget
    while(True):
        try:
            temp = input(mes)
            Budget = int(temp)
            break
        except:
            print('Please enter a valid budget')
            mes = 'Again, how much do you love to spend?'
    
    #Validate Zipcode
    while(True):
        try:
            ZipCode = input('Enter your area Zipcode:')
            if(len(ZipCode) != 5):
                 raise Exception('Size error')
            temp = int(ZipCode)
            break
        except:
            print('Please enter a correct Zipcode')


#Process Inputs, by getting restuarants
def process_inputs():
    global res_df
    global ratings
    print('Processing...')
    res_df = get_restuarants()
    ratings = v.load_file()
    v.set_data(ratings)
    
### MAIN PROGRAM ###

# Set up a loop where users can choose what they'd like to do.
def main():
    choice = ''
    
    get_inputs()
    process_inputs()
    #Check if the input processing went fine
    if (res_df is None) or (len(res_df) == 0):
        print('Something went wrong, please try again later.')
    else:
        #Until, the choice 'q' is selected, the prompt always user to select options
        while choice != 'q':    
            display_title_bar()
            choice = get_user_choice()
            # Respond to the user's choice.
            display_title_bar()
            if choice == '1':
                show_movies()
            elif choice == '2':
                show_restuarants()
            elif choice == 'r':
                reset()
                get_inputs()
                process_inputs()
            elif choice =='v':
                visualize()
            elif choice == 'q':
                print_report()
                print("\nHave a great night.")
            else:
                print("\nI didn't understand that choice.\n")


if __name__ == "__main__":
    main()