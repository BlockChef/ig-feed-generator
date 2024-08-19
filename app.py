from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def input_form():
    if request.method == 'POST':
        # Process form data (we'll implement this later)
        return redirect(url_for('success'))

    return render_template('inputForm.html')

@app.route('/success')
def success():
    return "Post prepared successfully!"

if __name__ == '__main__':
    app.run(debug=True)