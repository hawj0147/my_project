from flask import Flask, render_template, request
from main import get_movie_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    movie_list = get_movie_data(keyword)
    
    return render_template(
        "search.html", 
        keyword=keyword, 
        movies=enumerate(movie_list)
    )

if __name__ == "__main__":
    app.run(debug=True)