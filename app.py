from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Process form data (we'll implement this later)
        return redirect(url_for("success"))
    return render_template("register.html")


@app.route("/success")
def success():
    return "Post prepared successfully!"


if __name__ == "__main__":
    app.run(debug=True)
