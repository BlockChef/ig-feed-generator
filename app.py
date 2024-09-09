from flask import Flask, render_template, request, jsonify, send_from_directory
from contentGeneration.generate import generate_instagram_post
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            result = generate_instagram_post(request.form, request.files, app)
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    return render_template("register.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/success")
def success():
    return "Post prepared successfully!"

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)