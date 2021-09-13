import flask
from flask import request, jsonify
import sqlite3

#iniating Flask application object
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#defining our SQLlite object
DB = "music.db"

def dict_factory(cursor, row):
    """Convert DB items into dictionary objects.
    
    This function convert items from the db in the form of a dictionary instead than of a list. 
    It ensure a proper jsonification of the items.
    
    """
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# routing home page 
@app.route('/', methods=["GET"])
def home():
    return '''<h1>\m/ Top Metal Album Archive \m/</h1>
    <p> Access the archive with our API └[◍!◎]┘ </p> '''

#routing error page 404
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>OOPS</h1> <p> Page not found </p>", 404

#routing full view of albums list
@app.route('/api/v1/resources/album/all', methods=["GET"])
def api_all():
    conn = sqlite3.connect(DB)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_album = cur.execute("SELECT * FROM album;").fetchall()
    
    return jsonify(all_album)
    
#routing api connection to album db
@app.route("/api/v1/resources/album", methods=["GET"])
def api_filter():
    """API items availables at the date
    
    Currently the following parameters have been instantiated: id_key (primary key), artist, album and genre.
    
    """
    query_parameters = request.args
    
    id_key = query_parameters.get("id")
    artist = query_parameters.get("artist")
    album = query_parameters.get("album")
    genre = query_parameters.get("genre")
    
    #building our SQL query
    query = "SELECT * FROM album WHERE"
    to_filter = []
    
    if id_key:
        query += ' id=? AND'
        to_filter.append(id_key)
    if artist:
        query += ' artist=? AND'
        to_filter.append(artist)
    if album:
        query += ' album=? AND'
        to_filter.append(album)
    if genre:
        query += ' genre=? AND'
        to_filter.append(genre)
    if not (id_key or artist or album or genre):
        return page_not_found(404)
    
    #this is needed to clean the SQL query after the last item is added; basically it removes the " AND" and add a ";"
    query = query[:-4] + ";"
    
    conn = sqlite3.connect(DB)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

#run the app
if __name__ == '__main__':
    app.run(use_reloader=False)
