import random
from imdb import IMDb

# Create an IMDb object
ia = IMDb()

# List of genres for recommendations
#https://www.imdb.com/feature/genre/
genres = ["action", "comedy", "drama", "sci-fi", "horror", "adventure", "romance", 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 
            'family', 'fantasy', 'film-noir', 'history', 'music', 'musical', 'mystery', 'short', 'sport',
             'thriller', 'war', 'western' ]

genre_tv = ["action", "comedy", "drama", "sci-fi", "horror", "adventure", "romance", 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 
            'family', 'fantasy', 'film-noir', 'history', 'music', 'musical', 'mystery', 'short', 'sport',
             'thriller', 'war', 'western', 'reality-tv', 'game-show', 'talk-show', 'news']

user_inputs = ['recommendations', 'Info', 'search', 'q']

def get_recommendation(genre):
    # Search for top-rated movies in the specified genre
    movies = ia.get_top50_movies_by_genres(user_input_genre)
    genre_movies = [movie for movie in movies if genre.lower() in [g.lower() for g in movie.data['genres']]]

    if genre_movies:
        random_movies = random.sample(movies, min(5, len(movies)))
        recommendations = []
        for movie in random_movies:
            ia.update(movie)
            title = movie.get('title', 'N/A')
            year = movie.get('year', 'N/A')
            rating = movie.get('rating', 'N/A')
            recommendations.append(f"{title} ({year}), Rating: {rating}")
    
        return recommendations

    else:
        return "Sorry, I couldn't find any recommendations for that genre."
    
def get_recommendation_serie(genre_tv):
    # Search for top-rated series in the specified genre
    series = ia.get_top50_tv_by_genres(user_input_genre)
    genre_series = [serie for serie in series if genre_tv.lower() in [g.lower() for g in serie.data['genres']]]

    if genre_series:
        random_serie = random.choice(genre_series)
        return f"I recommend watching '{random_serie}' ({random_serie.data['year']})."
    else:
        return "Sorry, I couldn't find any recommendations for that genre."
    
def search_movie(movie):
    movies = ia.search_movie(movie)

    print("searching for the movie...")

    for movie in movies:
        title = movie['title']
        year = movie['year']
        print(f"{title} - {year}")

def get_plot_by_title(title):
    search_results = ia.search_movie(title)

    if not search_results:
        return "No results found for the given title."

    first_result = search_results[0]
    ia.update(first_result, info=['plot'])
    
    if 'plot' in first_result:
        return first_result['plot'][0]
    else:
        return "Plot information not available for this title."

# Main menu
print("Hello, this is your Tv series/Movies chatbot recommendator.\n")

print("You can ask for recommendations or asking info about a movie or Tv serie. \n")

while True:
    user_input = input ("Input one of the following command: 'recommendations', 'Info', 'search' or press 'q' to quit'\n")
    
    if user_input not in user_inputs:
        print("Invalid input.")

    elif user_input.lower() == "q":
        print("Thank you for using the Recommendation Chatbot. Goodbye!")
        break

    elif user_input == 'search':

        movie = input("Input a movie you want to search: ")

        search_movie(movie)

    elif user_input == 'Info':
        title = input("Enter the title of the movie or TV series: ")
        plot = get_plot_by_title(title)
        print("Plot:")
        print(plot)

    elif user_input == 'recommendations':

        user_input_recommendations = input("Do you want to watch a 'movie' or a 'serie'? ")

        if user_input_recommendations == 'movie':

            user_input_genre = input("Enter a genre or type 'exit' to quit: ")
            print("Searching for movies...")
    
            if user_input_genre.lower() in genres:

                recommendations = get_recommendation(user_input_genre)

                if recommendations:

                    print(f"\nHere are 5 movie recommendations in the '{user_input_genre}' genre:")
                    for i, recommendation in enumerate(recommendations, start=1):
                        print(f"{i}. {recommendation}")
            else:
                print(f"No movies found in the '{user_input_genre}' genre.")

        else:
            print("Invalid genre. Please choose from:", ", ".join(genres))
        
    elif user_input_recommendations == 'serie':

        user_input_genre = input("Enter a genre or type 'exit' to quit: ")
    
        if user_input_genre.lower() in genres:
            recommendation = get_recommendation_serie(user_input_genre)
            print(recommendation)
        else:
            print("Invalid genre. Please choose from:", ", ".join(genres))
    else:
        print("Invalid Input")