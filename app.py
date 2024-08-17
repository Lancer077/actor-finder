from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)



#WEB SCRAPING --------------------------------------------------
#aka the reason I started this project

#takes in movie title and returns url for the cast list of the movie
def get_movie_url(title):
    #title.replace("spiderman", "spider man") #spiderman doesn't work without the hyphen or a space
    #title.replace("Spiderman", "spider man")

    api_key = "" #It's only a matter of time before I accidentally leak this lmao
    search_url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}" #search the movie title using the api key
    #the actual IMDB website blocks bot activity for searches but does not block bots from accessing the cast list

    response = requests.get(search_url) #grab the response

    if response.status_code != 200:
        print("Problem retrieving the data")
        return None

    data = response.json() #parse data

    if data['Response'] == 'False':
        print("Movie Not Found")
        return None

    imdb_id = data['imdbID']
    movie_url = f"https://www.imdb.com/title/{imdb_id}/fullcredits" #grab the movie cast url
    return movie_url


#takes in a movie cast url and returns a list of the actor names
def get_cast(movie_url):
    response = requests.get(movie_url) #accesses the cast website url

    #print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser') #parse the data

    cast_section = soup.find('table', {'class': 'cast_list'}) #grab the table

    actors = cast_section.find_all('a', {'href': lambda x: x and x.startswith('/name/')}) #stackoverflow moment

    actor_names = [actor.get_text(strip=True) for actor in actors] #create the list of actor names

    return actor_names


#get all cast members in both films
def get_cast_union(cast1, cast2):
    set1 = set(cast1)
    set2 = set(cast2)

    set3 = set1.intersection(set2)

    cast3 = []

    for name in set3:
        if(name != ""):
            cast3.append(name)

    return cast3

def driver_logic(movies):
    num_of_movies = len(movies)

    cast_URLs = []

    for movie in movies:
        cast_URLs.append(get_movie_url(movie))
    
    cast_lists = []
    for url in cast_URLs:
        cast_lists.append(get_cast(url))

    big_cast_list = dict()

    for cast_list in cast_lists:
        for cast_member in cast_list:
            if cast_member in big_cast_list: #if cast member was found and was already in the list
                big_cast_list[cast_member] = big_cast_list[cast_member] + 1 #increment the number of times that cast member was found
                
            else: #if cast member was not already in the list
                big_cast_list[cast_member] = 1 #add the cast member to the list with one movie to their name
                # I could make it so that if a cast member was not found in the first movie, they are just disregarded but eventually I want to allow for 3 movies to be entered
                #   and the website would show people who only show up in 2 of the 3 movies
    
    final_cast_list = []

    names = big_cast_list.keys()

    for name in names:
        if big_cast_list[name] == num_of_movies:
            final_cast_list.append(name)


    return final_cast_list
    
   
    


#website flask stuff (aka the part of this project I don't like) ----------------------------------


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get all movie titles from the form
        movie_titles = request.form.getlist('movie')
        #perform the driver logic on the movies
        actor_list = driver_logic(movie_titles)


        return redirect(url_for('actors', actors=','.join(actor_list)))

    return render_template('index.html')

@app.route('/actors')
def actors():
    # actor names
    actors = request.args.get('actors', '')
    # Split the actors back into a list
    actor_list = actors.split(',')
    return render_template('actors.html', actor_list=actor_list)

if __name__ == '__main__':
    app.run(debug=True)
