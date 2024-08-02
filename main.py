from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd


popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')
Author_df = pd.read_pickle('Author_df.pkl')
books_new_df = pd.read_pickle('books_new_df2.pkl')
app = Flask(__name__)

popular_df.avg_rating=popular_df.avg_rating.round(2)
new_popular_df=popular_df.head(5)

def load_dataset():
    # Code to load the dataset
    # Replace the following line with your code to load the dataset
    books_new = pd.read_csv("Books.csv")
    return books_new

@app.route('/')
def home():
    return render_template('home.html',
                           book_name=list(new_popular_df['Book-Title'].values),
                           author=list(new_popular_df['Book-Author'].values),
                           image=list(new_popular_df['Image-URL-M'].values),
                           votes=list(new_popular_df['num_ratings'].values),
                           rating=list(new_popular_df['avg_rating'].values)
                           )

@app.route('/top50')
def top50():
    return render_template('top50.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    dataset = load_dataset()
    book_names = dataset['Book-Title'].tolist()
    return render_template('recommend.html', book_names=book_names)


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:17]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/recommend_author')
def recommend_author():
    return render_template('recommend_author.html')

@app.route('/recommend_author_books', methods=['post'])
def recommend_author_books():
    user_input = request.form.get('user_input')
    data = Author_df.get_group(user_input)
    df = []
    final_data = data[["Book-Title", "Book-Author", "Image-URL-M"]].head(8)
    df = final_data.values.tolist()
    return render_template('recommend_author.html', data=df)

if __name__ == '__main__':
    app.run(debug=True)
