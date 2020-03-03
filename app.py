from flask import Flask, render_template, redirect
import scrape_mars
import pymongo

CONN = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONN)
db = client.mars_db

app = Flask(__name__)

@app.route("/")
def query_data():
    mars = db.mars_col.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    db.mars_col.remove({})
    data = scrape_mars.scrape()
    db.mars_col.insert_one(data)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
