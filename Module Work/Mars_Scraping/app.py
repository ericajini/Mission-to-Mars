# we'll use Flask to render a template, 
# redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# using the scraping code, we will convert from Jupyter notebook to Python
import scraping

# set up flask app

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#  tells Flask what to display when we're looking at the home page
@app.route("/")
# defining the index function- This function is what links our visual representation of our work, our web app, to the code that powers it. 
def index():
# uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. We will also assign that path to themars variable for use later
    mars = mongo.db.mars.find_one()
#  tells Flask to return an HTML template using an index.html file. We'll create this file after we build the Flask routes.
# mars=mars tells Python to use the "mars" collection in MongoDB.
    return render_template("index.html", mars=mars)


@app.route("/scrape")
# creating function
def scrape():
# Then, we assign a new variable that points to our Mongo database
    mars = mongo.db.mars
# we created a new variable to hold the newly scraped data 
    mars_data = scraping.scrape_all()
# upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved
    mars.update_one({}, {"$set":mars_data}, upsert=True)
# finally, we will add a redirect after successfully scraping the data: return redirect('/', code=302). This will navigate our page back to / where we can see the updated content.    
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()

