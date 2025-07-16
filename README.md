# Reddit Persona Generator
This project scrapes a Reddit user's public profile and uses the OpenAI API to generate a user persona based on their posts and comments. It also cites the exact posts/comments used to build each trait in the persona.
# Features:
Input a Reddit user URL
Scrapes recent posts and comments
Generates a psychological user persona
Cites the Reddit activity for each trait
Provides web interface via Flask
Outputs persona to a .txt file
Files Overview
`app.py` — Main Flask backend to serve the web pages
`home.html` — HTML page where users enter Reddit handles or interests
`persona.html` — Displays the generated Reddit persona
`reddit_persona.py` — Core logic that interacts with the OpenAI API
# How to Run This Project Locally
# Install Dependencies
Make sure you have Python installed. Then install Flask. 
after running the codes it will displays the http://127.0.0.1:5000
it will show the reddit user info viewer where we have to give the url(as mentioned in the assignment).
it will displays the Username: kojied
Post Karma: 216
Comment Karma: 1823
Cake Day: Fri Jan 03 2020
Recent Posts and comments. and other url (as mentioned in the assignment) username: Hungry-Move-6603 and it will displays the same details.
