import praw
import openai
from flask import Flask, request, render_template, redirect, url_for, flash
import json
import re

app = Flask(__name__)
# Set up PRAW (read-only is sufficient for public info)
reddit = praw.Reddit(
    client_id="<Qqq5MbxkMovtWILJ5KIBfA>",
    client_secret="<ZjNbDORToeHS8SQH3kOHMwyW9QR2fQ>",
    user_agent="RedditPersonaApp by Sneha"
)

def extract_username(input_str):
    m = re.match(r"https?://(www\.)?reddit\.com/user/([^/]+)/?", input_str)
    return m.group(2) if m else input_str.strip()

def get_user_data(username):
    try:
        user = reddit.redditor(username)
        # Try to force a fetch and trigger error if invalid (e.g. user doesn't exist)
        _ = user.id
        posts = [f"Title: {post.title}\nText: {post.selftext}" for post in user.submissions.new(limit=5)]
        comments = [f"Comment: {comment.body}" for comment in user.comments.new(limit=5)]
        return posts, comments
    except Exception as e:
        return None, None

def create_prompt(posts, comments):
    content = "\n\n".join(posts + comments)
    prompt = f"""Based on these Reddit posts/comments, generate a user persona JSON:
--- POSTS AND COMMENTS ---
{content}
Respond in this JSON format:

{{
  "name": "Optional or leave blank",
  "age": "Estimate or leave blank",
  "occupation": "Guess or leave blank",
  "personality": "Describe tone and personality traits",
  "motivations": ["..."],
  "behavior": ["..."],
  "habits": ["..."],
  "goals_needs": ["..."],
  "frustrations": ["..."],
  "summary": "Overall persona summary",
  "citations": [
    {{
      "category": "Which attribute this citation supports (e.g. motivations)",
      "source": "Short quote or paraphrase",
      "link": "Reddit link"
    }}
  ]
}}
"""
    return prompt

def generate_persona(posts, comments):
    prompt = create_prompt(posts, comments)
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=900
    )
    try:
        persona_json = response.choices[0].message.content
        data = json.loads(persona_json)
        return data
    except Exception as e:
        return {"error": "Failed to parse OpenAI output."}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_val = request.form.get("username")
        username = extract_username(input_val)
        # Validate non-empty username
        if not username:
            flash("Please enter a valid Reddit username or profile URL.")
            return render_template("home.html")
        return redirect(url_for("persona", username=username))
    return render_template("home.html")

@app.route("/persona/<username>")
def persona(username):
    posts, comments = get_user_data(username)
    if posts is None:
        return f"<h2>User '{username}' not found or error fetching data.</h2><a href='/'>Back</a>"
    persona = generate_persona(posts, comments)
    # Save to .txt for download
    with open(f"{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(persona, indent=2))
    return render_template("persona.html", user=username, persona=persona)

if __name__ == "__main__":
    app.run(debug=True)