from flask import Flask, jsonify
from scraper_tennis import scraper_tennis

app = Flask(__name__)

@app.route("/")
def accueil():
    return "✅ API de scraping pour le Tennis est en ligne."

@app.route("/api/tennis", methods=["GET"])
def tennis():
    try:
        data = scraper_tennis()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
