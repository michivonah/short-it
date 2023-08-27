from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

@app.route("/create/<slug>")
def createNew(slug):
    return f"New request registerd for /{slug}"

@app.route("/<slug>")
def shortUrl(slug):
    destination = f"https://www.example.com/{slug}"
    return redirect(destination, code=302)

if __name__ == "__main__":
    app.run(debug=True)

# random base64 string: openssl rand -base64 24