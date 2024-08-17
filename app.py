from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)



#WEB SCRAPING --------------------------------------------------
#aka the reason I started this project

#takes in movie title and returns url for the cast list of the movie
def get_movie_url(title):
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
    mURL1 = get_movie_url(movies[0])
    mURL2 = get_movie_url(movies[1])

    cast1 = get_cast(mURL1)
    cast2 = get_cast(mURL2)

    cast3 = get_cast_union(cast1, cast2)

    return cast3




#website flask stuff (aka the part of this project I don't like) ----------------------------------
def remove_vowels(text):
    return ''.join(c for c in text if c.lower() not in 'aeiou')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get all movie titles from the form
        movie_titles = request.form.getlist('movie')
        # Remove vowels from each movie title
        actor_list = driver_logic(movie_titles)
        
        #processed_titles = [remove_vowels(title) for title in movie_titles]
        # Redirect to the display page with the processed titles
        return redirect(url_for('actors', actors=','.join(actor_list)))
    return render_template('index.html')

@app.route('/actors')
def actors():
    # Get the processed titles from the query parameters
    actors = request.args.get('actors', '')
    # Split the titles back into a list
    actor_list = actors.split(',')
    return render_template('actors.html', actor_list=actor_list)

if __name__ == '__main__':
    app.run(debug=True)
