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

user_inputs = ['recommendations', 'info', 'search', 'reviews',  'q']

reviews = {}

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
            recommendations.append(f"{title} ({year} , rating: {rating})")
    
        return recommendations

    else:
        return "Sorry, I couldn't find any recommendations for that genre."
    
def get_recommendation_serie(genre_tv):
    # Search for top-rated series in the specified genre
    series = ia.get_top50_tv_by_genres(user_input_genre)
    genre_tv = [serie for serie in series if genre_tv.lower() in [g.lower() for g in serie.data['genres']]]

    if genre_tv:
        random_series = random.sample(series, min(5, len(series)))
        recommendations_tv = []
        for serie in random_series:
            ia.update(serie)
            title = serie.get('title', 'N/A')
            year = serie.get('year', 'N/A')
            rating = serie.get('rating', 'N/A')
            recommendations_tv.append(f"{title} ({year} , rating: {rating})")
    
        return recommendations_tv
    
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
        return "Plot not available for this title."
    
def get_reviews():
    title = input("Enter the title of the movie or series: ")
    rating = float(input("Enter your rating (1-10): "))
    review_text = input("Write your review: ")

    if title in reviews:
        reviews[title]['ratings'].append(rating)
        reviews[title]['reviews'].append(review_text)
    else:
        reviews[title] = {'ratings': [rating], 'reviews': [review_text]}

def view_reviews():
    title = input("Enter the title of the movie or series to view reviews: ")

    if title in reviews:
        print(f"Reviews for {title}:")
        for i, (rating, review) in enumerate(zip(reviews[title]['ratings'], reviews[title]['reviews'])):
            print(f"Review {i + 1}:")
            print(f"Rating: {rating}")
            print(f"Review Text: {review}")
            print()
    else:
        print(f"No reviews found for {title}.")

# Main menu
print("Hello, I'm a chatbot and I know everything about cinema and TV series.\n")

print("You can ask for recommendations or info about a movie or Tv serie. \n")

while True:
    user_input = input ("\nInput one of the following: 'recommendations', 'info', 'search' 'reviews' or press 'q' to quit': \n")
    
    if user_input not in user_inputs:
        print("Sorry. I was not build for that! :( , I still have to learn other functionalities!\nBe patient and in the meanwhile, just input one of the following: 'recommendations', 'Info', 'search' or press 'q' to quit'\n")
        continue

    if user_input.lower() == "q":
        print("Already want to go? I hope to talk with you again!\n")
        print("Have a nice day! Bye Bye.\n")
        break

    if user_input == 'search':
        print("With the 'search' input, you can find a movie or Tv serie you are searching for:\n ")

        movie = input("Input a keyword: \n")
        print("Loading information...\n")
        search_movie(movie)

    if user_input == 'info':
        print("As I told you, I know everything about cinema,\n but at the moment I can just tell you the plot.")
        title = input("Enter the title of a movie or a TV serie and I will share with you the plot: \n")
        plot = get_plot_by_title(title)
        print("Here is the plot: \n")
        print(plot)

    if user_input == 'reviews':
        print("This is a new feature. You can see reviews or write a review for a movie or series, so that everyone could see them!\n")
        nickname = input("what is your name? ")
        print(f"What do you want to do {nickname}: ?")
        print("\nOptions:")
        print("1. Add a review")
        print("2. View reviews")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            get_reviews()
        elif choice == '2':
            view_reviews()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    if user_input == 'recommendations':
        print("With the 'recommendations' feature, I can advice you what to watch tonight, you will not be disappointed!\n ")
        user_input_recommendations = input("Do you want to watch a 'movie' or a 'serie'? \n")

        if user_input_recommendations == 'movie':

            user_input_genre = input("Enter a genre or type 'exit' to return to the main menu: \n")

            if user_input_genre == 'exit':
                continue
            else:
                print("Searching for movies...\n")
    
                if user_input_genre.lower() in genres:

                    recommendations = get_recommendation(user_input_genre)

                if recommendations:

                    print(f"\nHere are 5 movie recommendations in the '{user_input_genre}' genre:")
                    for i, recommendation in enumerate(recommendations, start=1):
                        print(f"{i}. {recommendation}")
                else:
                    print(f"No movies found in the '{user_input_genre}' genre.\n")
                    continue
        
        if user_input_recommendations == 'serie':

            if user_input_recommendations == 'q':
                print("Goodbye!")

            user_input_genre = input("Enter a genre or type 'exit' to quit: ")

            if user_input_genre == 'exit':
                continue
            
            else:
                print("Searching for series...")
    
                if user_input_genre.lower() in genres:
                
                    recommendations_tv = get_recommendation_serie(user_input_genre)
                
                    if recommendations_tv:
                
                        print(f"\nHere are 5 serie recommendations in the '{user_input_genre}' genre:")
                        for i, recommendation_tv in enumerate(recommendations_tv, start=1):
                            print(f"{i}. {recommendation_tv}")
                    else:
                        print(f"No series found in the '{user_input_genre}' genre.")
                        continue