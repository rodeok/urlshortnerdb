from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import string
import random
import os

app = Flask(__name__)
CORS(app)  # Enable CORS



BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')


url_mappings = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    if short_url in url_mappings:
        return generate_short_url()
    return short_url

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json['longUrl']
    short_url = generate_short_url()
    url_mappings[short_url] = long_url
    short_url_with_base = f'{BASE_URL}/{short_url}'
    return jsonify({'shortUrl': short_url_with_base}), 201

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    if short_url in url_mappings:
        long_url = url_mappings[short_url]
        return redirect(long_url, code=302)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)