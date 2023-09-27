import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
#from kivy.uix.scrollview import ScrollView
from imdb import IMDb
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import random

kivy.require('2.0.0')

#Genres List for the recommendations feature
genres = ["action", "comedy", "drama", "sci-fi", "horror", "adventure", "romance", 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 
            'family', 'fantasy', 'film-noir', 'history', 'music', 'musical', 'mystery', 'short', 'sport',
             'thriller', 'war', 'western' ]


class IMDBLovers(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reviews = {}
        self.result_label = Label()  
        self.load_reviews()

    def build(self):
        self.imdb = IMDb()

        self.layout = BoxLayout(orientation='vertical')

        self.layout = GridLayout(cols=2, padding=20, spacing=20)

        Window.size = (1000, 600)

        self.show_main_menu()

        return self.layout
        

    def show_main_menu(self):
# Clear the current screen - for each different screen
        self.layout.clear_widgets()

        #main_menu_label = Label(text='Main Menu', size_hint=(None, None), font_size=30)

        #self.layout.add_widget(main_menu_label)

        #Left side layout

        left_side_layout = BoxLayout(orientation='vertical')

        # Main Menu
        main_menu_label = Label(text='IMDB Lovers Menu', font_size=30)
        left_side_layout.add_widget(main_menu_label)

        # Feature Descriptions
        descriptions_label = Label(
            text=(
                "1. Get Movies Recommendations by Genre\n\n"
                "2. Get Movie/Series Plot by Title\n\n"
                "3. Find Movies/Series by Keywords\n\n"
                "4. Insert/View Reviews"
            ),
            font_size=16,
        )
        left_side_layout.add_widget(descriptions_label)

        self.layout.add_widget(left_side_layout)

        # Right Side (Feature Input Fields and Buttons)
        right_side_layout = BoxLayout(orientation='vertical')
        
        # Feature 1 - Movie recommendations by genre
        recommend_button = Button(text='Recommend Movies by Genre', font_size=20)
        recommend_button.bind(on_press=self.recommendation_screen)
        right_side_layout.add_widget(recommend_button)
        
        # Feature 2 - Get movie plot by title
        plot_button = Button(text='Get Movie/Series Plot by Title', font_size=20)
        plot_button.bind(on_press=self.plot_screen)
        right_side_layout.add_widget(plot_button)
        
        # Feature 3- Find movies by keywords
        search_button = Button(text='Get Movie/Series by keywords', font_size=20)
        search_button.bind(on_press=self.search_screen)
        right_side_layout.add_widget(search_button)

        #Feature 4 - Reviews
        reviews_button = Button(text='Reviews', font_size=20)
        reviews_button.bind(on_press=self.reviews_screen)
        right_side_layout.add_widget(reviews_button)

        self.layout.add_widget(right_side_layout)
        
        return self.layout
    
    def recommendation_screen(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Enter a genre:', font_size=20, halign='center'))
        genre_input = TextInput(hint_text='Enter a genre', size_hint=(0.5,0.5))
        self.layout.add_widget(genre_input)
        recommend_button = Button(text='Recommend Movies', font_size=20, halign='center')
        recommend_button.bind(on_press=lambda x: self.recommend_movies(genre_input.text))
        self.layout.add_widget(recommend_button)
        self.movie_results_label = Label(text="", font_size=16)
        self.layout.add_widget(self.movie_results_label)
        back_button = Button(text='Back to Main Menu', font_size=20)
        back_button.bind(on_press=lambda x: self.show_main_menu())
        self.layout.add_widget(back_button)
        self.result_label = Label(text='', size_hint=(None, None), font_size=20, halign='center')
        self.layout.add_widget(self.result_label)


    def recommend_movies(self, genre):

        movies = self.imdb.get_top50_movies_by_genres(genre)

        if genre not in genres:
            self.result_label.text = f"No movies found in the {genre} genre."
    
        else:
            random.shuffle(movies)
            recommended_movies = [movie['title'] for movie in movies[:5]]
            self.result_label.text = f"Recommended Movies in {genre}: {', '.join(recommended_movies)}"

    def plot_screen(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Enter title:', font_size=20, halign='center'))
        title_input = TextInput(hint_text='Enter title', size_hint=(0.5,0.5))
        self.layout.add_widget(title_input)
        plot_button = Button(text='Get Movie Plot', font_size=20, halign='center')
        plot_button.bind(on_press=lambda x: self.find_plot(title_input.text))
        self.layout.add_widget(plot_button)
        back_button = Button(text='Back to Main Menu', font_size=20)
        back_button.bind(on_press=lambda x: self.show_main_menu())
        self.layout.add_widget(back_button)
        self.plot_label = Label(text='', size_hint=(0.5,0.25), font_size=20, halign='center')
        self.layout.add_widget(self.plot_label)

    def find_plot(self, title_input):
        search_results = self.imdb.search_movie(title_input)

        if not search_results:
            return "No results found for the given title."

        first_result = search_results[0]
        self.imdb.update(first_result, info=['plot'])
    
        if 'plot' in first_result:
            self.plot_label.text = f"Plot: {first_result['plot'][0]}"
        else:
            self.plot_label.text = f"Plot not found"

    def search_screen(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Enter a keyword:', font_size=20, halign='center'))
        keywords_input = TextInput(hint_text='Enter a keyword', size_hint=(0.5,0.5))
        self.layout.add_widget(keywords_input)
        search_button = Button(text='Find movies', font_size=20, halign='center')
        search_button.bind(on_press=lambda x: self.search_movies_by_keywords(keywords_input.text))
        self.layout.add_widget(search_button)
        back_button = Button(text='Back to Main Menu', font_size=20)
        back_button.bind(on_press=lambda x: self.show_main_menu())
        self.layout.add_widget(back_button)
        self.search_label = Label(text='', size_hint=(0.5,0.5), font_size=20, halign='center')
        self.layout.add_widget(self.search_label)
        
    def search_movies_by_keywords(self, keywords_input):
        movies = self.imdb.search_movie(keywords_input)

        for keywords_input in movies:
            title = keywords_input['title']
            year = keywords_input['year']
            self.search_label.text = f"{title} - {year}"

    def reviews_screen(self, instance):
        self.layout.clear_widgets()
        add_review_button = Button(text='Add reviews', font_size=20, halign='center')
        add_review_button.bind(on_press=lambda x: self.add_review_screen())
        self.layout.add_widget(add_review_button)
        view_review_button = Button(text='View reviews', font_size=20, halign='center')
        view_review_button.bind(on_press=lambda x: self.view_review_screen())
        self.layout.add_widget(view_review_button)

        back_button = Button(text='Back to Main Menu', font_size=20)
        back_button.bind(on_press=lambda x: self.show_main_menu())
        self.layout.add_widget(back_button)

    def add_review_screen(self):
        self.layout.clear_widgets()
        self.add_label = Label(text="Movie/Series Title:")
        self.add_input = TextInput(hint_text='Enter a title', size_hint=(0.5,0.5))
        self.layout.add_widget(self.add_input)
        self.review_label = Label(text="Movie Review:")
        self.review_input = TextInput(hint_text='Enter a Review', size_hint=(0.5,0.5))
        self.layout.add_widget(self.review_input)
        self.add_button = Button(text="Add Review")
        self.add_button.bind(on_press=self.add_review)
        self.layout.add_widget(self.add_button)
        back_button = Button(text='Back to Main Menu', font_size=20)
        back_button.bind(on_press=lambda x: self.show_main_menu())
        self.layout.add_widget(back_button)

    def view_review_screen(self):
        self.layout.clear_widgets()
        self.view_label = Label(text="Search by Title:")
        self.view_input = TextInput(hint_text='Enter a Title', size_hint=(0.5,0.5))
        self.layout.add_widget(self.view_input)
        self.view_button = Button(text="Search Reviews")
        self.view_button.bind(on_press=lambda x: self.search_reviews(x))
        self.layout.add_widget(self.view_button)
        self.result_label = Label()
        self.layout.add_widget(self.result_label)
        back_button = Button(text='Back to Main Menu', font_size=20)
        back_button.bind(on_press=lambda x: self.show_main_menu())
        self.layout.add_widget(back_button)


    def add_review(self, instance):
        title = self.add_input.text
        review = self.review_input.text

        if title and review:
            self.reviews[title] = review
            self.add_input.text = ""
            self.review_input.text = ""
            self.result_label.text = "Review added successfully."
            self.save_reviews()
        else:
            self.result_label.text = "Please enter both title and review."

    def search_reviews(self, instance):
        title_to_search = self.view_input.text
        self.save_reviews()
        if title_to_search in self.reviews:
            self.result_label.text = f"Review for '{title_to_search}':\n{self.reviews[title_to_search]}"
        else:
            self.result_label.text = "Movie not found in reviews."

    def save_reviews(self):
        with open("reviews.txt", "w") as file:
            for title, review in self.reviews.items():
                file.write(f"{title}:{review}\n")

    def load_reviews(self):
        try:
            with open("reviews.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) == 2:
                        title, review = parts[0], parts[1]
                        self.reviews[title] = review
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    IMDBLovers().run()