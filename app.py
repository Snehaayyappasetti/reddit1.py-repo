from flask import Flask, request, render_template, redirect, url_for
import json  # Required for saving persona

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('persona', username='kojied'))
    return render_template('home.html')

@app.route('/persona/<username>')
def persona(username):
    # Replace this with real persona generation
    persona = {
        "name": "Example User",
        "age": "25-34",
        "occupation": "Software Engineer",
        "traits": ["Curious", "Tech-savvy"],
        "summary": "Enjoys technology, learning, and Reddit discussions.",
        "motivations": ["Learning", "Community engagement"],
        "behavior_and_habits": ["Frequent Reddit poster", "Helpful"],
        "goals_and_needs": ["Career growth", "Knowledge"],
        "frustrations": ["Toxic communities", "Low-quality content"]
    }

    #  Save persona to .txt
    with open(f"static/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(persona, indent=2))

    return render_template('persona.html', username=username, persona=persona)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
