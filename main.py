from flask import Flask, request, jsonify, redirect, render_template
import dbfunctions as db
import re
import random
import string

app = Flask(__name__)

defaultpage = "https://example.com"

@app.route("/")
def home():
    return redirect(defaultpage, code=302)

@app.route("/CREATE")
def createNew():
    token = request.args.get("token")
    dest = request.args.get("to")
    slug = request.args.get("slug")
    if token: # Check if token was used
        if checkString(token): # Check if token matches RegEx
            getToken = db.executeQuery(f'SELECT "name" FROM "user" WHERE "token" = \'{token}\';')
            if getToken: # Provided token exists and is valid
                if dest:
                    if not slug:
                        slug = generateSlug(6)
                    return createUrl(slug, dest)
                else:
                    return createError("No destination, please provide a destination url")
            else:
                return createError("Not allowed - please provide a existing authentication token")
        else:
            return createError("Not allowed - please provide a valid authentication token")
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

def createUrl(slug, dest):
    if not checkString(slug): # Reset string
        slug = generateSlug(6)
    while db.executeQuery(f'SELECT "slug" FROM "url" WHERE "slug" = \'{str.lower(slug)}\';'): # Generates a string until its not in use
        slug = generateSlug(6)
    db.executeWithoutFetch(f'INSERT INTO "url" ("slug", "destination") VALUES (\'{slug}\', \'{dest}\');') # Adds the string to db
    report = {
        "message":"Short url created",
        "slug":slug,
        "destination":dest
    }
    return jsonify(report), 200

def checkString(string):
    pattern = "^[0-9a-zA-Z]*$"
    valid = re.search(pattern, string)
    return valid

def generateSlug(lenght):
    symbolList = "abcdefghijklmnopqrstuvwxyz0123456789"
    newSlug = ''.join(random.choice(symbolList) for i in range(lenght))
    return newSlug

if __name__ == "__main__":
    app.run(debug=True)

# random base64 string: openssl rand -base64 24
# ADD: Make any answer a restful json