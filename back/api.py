from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import Scraper
from db import DatabaseManager

class HackerNewsAPI:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app) 
        self.db = DatabaseManager()
        self.scraper = Scraper()
        self._register_routes()

    def _register_routes(self):
        @self.app.route("/stories", methods=["GET"])
        def get_stories():
            """
            Return all stories in the DB.
            Optional query param: limit
            """
            limit = request.args.get("limit", type=int)
            stories = self.db.fetch_all_stories()
            if limit:
                stories = stories[:limit]
    
            for s in stories:
                if s["date_created"]:
                    s["date_created"] = s["date_created"].isoformat()
            return jsonify(stories)

        @self.app.route("/stories/refresh", methods=["GET"])
        def refresh_stories():
            """
            Scrape latest stories, update points, and insert new ones.
            """
            scraped = self.scraper.scrape_all()
            self.db.update_story_points(scraped)
            return jsonify({
                "updated": len(scraped) 
            })

    def run(self, host="0.0.0.0", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    api = HackerNewsAPI()
    api.run()
