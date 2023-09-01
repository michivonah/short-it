from flask import Flask, request, jsonify, redirect, render_template
import dbfunctions as db
import re # RegEx
import random

app = Flask(__name__)

defaultpage = "https://example.com"

@app.route("/")
def home():
    return redirect(defaultpage, code=302)

@app.route("/CREATE")
def createNew():
    token = request.args.get("token", default="ANONYMUS")
    dest = request.args.get("to")
    slug = request.args.get("slug", default=generateSlug(6))
    if checkString(token): # Check if token matches RegEx
        validateToken = db.executeQuery(f'SELECT "name" FROM "user" WHERE "token" = \'{token}\';')
        if validateToken and checkString(dest, "url"): # Provided token & destination is valid
            return createUrl(slug, dest)
        else:
            return createError("Creation failed - please provide a valid authentication token and a destination url")
    else:
        return createError("Not allowed - please provide a valid authentication token")

@app.route("/<slug>")
def shortUrl(slug):
    if checkString(slug):
        destination = db.executeQuery(f'SELECT "destination" FROM "url" WHERE "slug" = \'{str.lower(slug)}\';')
        if destination:
            destination = destination[0][0]
        else:
            destination = defaultpage
        return redirect(destination, code=302)
    else:
        return render_template("error.html")
    
def createError(message="No message provided"):
    error = jsonify({
            "message":message
        })
    return error, 200

def createUrl(slug, dest):
    if not checkString(slug): slug = generateSlug()
    while db.executeQuery(f'SELECT "slug" FROM "url" WHERE "slug" = \'{str.lower(slug)}\';'): # Generates a string until its not in use
        slug = generateSlug()
    db.executeWithoutFetch(f'INSERT INTO "url" ("slug", "destination") VALUES (\'{slug}\', \'{dest}\');') # Adds the string to db
    report = {
        "message":"Short url created",
        "slug":slug,
        "destination":dest
    }
    return jsonify(report), 200

def checkString(string="sometext", type="alphanumeric"):
    match type:
        case "url":
            pattern = "^(https?:\/\/)?[0-9a-zA-Z:\/+\- %?=&.]+$"
        case "alphanumeric" | _:
            pattern = "^[0-9a-zA-Z]*$"
    valid = re.search(pattern, string)
    return valid

def generateSlug(lenght=6):
    symbolList = "abcdefghijklmnopqrstuvwxyz0123456789"
    newSlug = ''.join(random.choice(symbolList) for i in range(lenght))
    return newSlug

if __name__ == "__main__":
    app.run(debug=True)

# ADD: Make any answer a restful json