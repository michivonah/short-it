from flask import Flask, request, jsonify, redirect, render_template
import dbfunctions as db
import re

app = Flask(__name__)

@app.route("/create/<slug>")
def createNew(slug):
    return f"New request registerd for /{slug}"

@app.route("/<slug>")
def shortUrl(slug):
    defaultpage = "https://example.com"
    if re.search("^[0-9a-zA-Z]*$", slug):
        destination = db.executeQuery(f'SELECT "destination" FROM "url" WHERE "slug" = \'{str.lower(slug)}\';')
        if destination:
            destination = destination[0][0]
        else:
            destination = defaultpage
        return redirect(destination, code=302)
    else:
        return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)

# random base64 string: openssl rand -base64 24