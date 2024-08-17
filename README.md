Something I thought of a while ago but web scraping seemed too scary at that time
Started last night and ironed out some of the kinks this morning
It's really not that bad especially with all of the documentation online for it
Flask was annoying and reminded me why I'm not in webdev or any sort of frontend development (sometimes foreshadowing is obvious)

-> All the code does is take in a user input for movie titles 
-> use OMDB database api to search the title and grab the movie ID for IMDB 
-> go to IMDB movie url and grab the castlist 
-> take the two castlists and find which names pop up both times 
-> send that data back to the frontend and display it

Still working on the functionality to grab multiple movies at the same time, gotta update some data structures and figure some other stuff out but shouldn't be too difficult
I have no intention of making the website look nicer because I have no respect for html and css

This was also my introduction to flask and general frontend (aside from visual basic .net in high school) so there's probably some excess floating around. I'll get to trimming the fat after fixing the multiple movies.
