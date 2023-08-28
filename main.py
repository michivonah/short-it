from flask import Flask, request, jsonify, redirect, render_template
import dbfunctions as db
import re

app = Flask(__name__)

defaultpage = "https://example.com"

@app.route("/")
def home():
    return redirect(defaultpage, code=302)

@app.route("/create/<slug>")
def createNew(slug):
    token = request.args.get("token")
    dest = request.args.get("to")
    if token:
        if dest:
            db.executeWithoutFetch(f'INSERT INTO "url" ("slug", "destination") VALUES (\'{slug}\', \'{dest}\');')
            report = {
                "message":"Short url created",
                "slug":slug,
                "destination":dest
            }
            return jsonify(report), 200
        else:
            return createError("No destination, please provide a destination url")
    else:
        return createError("Not allowed - please provide a authentication token")

@app.route("/<slug>")
def shortUrl(slug):
    if re.search("^[0-9a-zA-Z]*$", slug):
        destination = db.executeQuery(f'SELECT "destination" FROM "url" WHERE "slug" = \'{str.lower(slug)}\';')
        if destination:
            destination = destination[0][0]
        else:
            destination = defaultpage
        return redirect(destination, code=302)
    else:
        return render_template("error.html")
    
def createError(message):
    error = jsonify({
            "message":message
        })
    return error, 200

if __name__ == "__main__":
    app.run(debug=True)

# random base64 string: openssl rand -base64 24