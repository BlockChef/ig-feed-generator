import os

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from contentGeneration.generate import generate_instagram_post, revise_instagram_post
from flask_session import Session

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit
app.config["SECRET_KEY"] = "your_secret_key_here"  # Change this to a random secret key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            result = generate_instagram_post(request.form, request.files, app)
            session["post_data"] = result
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"status": "success", "redirect": url_for("preview")})
            else:
                return redirect(url_for("preview"))
        except Exception as e:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"status": "error", "message": str(e)}), 400
            else:
                return render_template("register.html", error=str(e))
    return render_template("register.html")


@app.route("/preview")
def preview():
    post_data = session.get("post_data")
    if not post_data:
        return redirect(url_for("index"))
    return render_template("preview.html", post_data=post_data)


@app.route("/revise", methods=["POST"])
def revise():
    suggestion = request.form.get("suggestion")
    post_data = session.get("post_data")
    if not post_data:
        return jsonify({"status": "error", "message": "No post data found"}), 400

    try:
        revised_result = revise_instagram_post(post_data, suggestion, app)
        session["post_data"] = revised_result
        return jsonify({"status": "success", "redirect": "/preview"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/approve", methods=["POST"])
def approve():
    # Here you would typically save the approved post to a database
    # and set up a task to publish it at the scheduled time
    session.pop("post_data", None)
    return jsonify({"status": "success", "message": "Post approved and scheduled"})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)
