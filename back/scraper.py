import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
from db import DatabaseManager





class Scraper:
    """
    Scraper for Hacker News (https://news.ycombinator.com/).
    """
    BASE_URL = "https://news.ycombinator.com/"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.db = DatabaseManager()

    def fetch_page(self, page: int = 1) -> BeautifulSoup | None:
        url = self.BASE_URL if page == 1 else f"{self.BASE_URL}?p={page}"
        response = self.session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        stories = soup.find_all("tr", class_="athing")
        return soup if stories else None

    def parse_page(self, soup: BeautifulSoup) -> List[Dict]:
        results = []
        stories = soup.find_all("tr", class_="athing")

        for story in stories:
            title_tag = story.find("span", class_="titleline").find("a")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            link = title_tag["href"] if title_tag else "N/A"

            subtext = story.find_next_sibling("tr").find("td", class_="subtext")

            points_tag = subtext.find("span", class_="score") if subtext else None
            points = int(points_tag.get_text().replace(" points", "")) if points_tag else 0

            time_tag = subtext.find("span", class_="age") if subtext else None
            date_created = None
            if time_tag:
                raw_date = time_tag.get("title")
                if raw_date:
                    try:
                        iso_part = raw_date.split()[0]  # strip off the Unix timestamp
                        date_created = datetime.strptime(iso_part, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        date_created = None

            results.append({
                "title": title,
                "link": link,
                "points": points,
                "date_created": date_created
            })

        return results

    def scrape_all(self) -> List[Dict]:
        all_results = []
        page = 1

        while True:
            soup = self.fetch_page(page)
            if not soup:
                break

            page_results = self.parse_page(soup)
            if not page_results:
                break

            all_results.extend(page_results)
            page += 1
        self.db.insert_stories(all_results)
        return all_results

    def update_points(self) -> None:
        stories = self.scrape_all()
        self.db.update_story_points(stories)
        

if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape_all()
    counter = 1
    for story in data:
        print(f"[{counter}]",story["title"], f"[{story["points"]} points]", story["date_created"])
        counter += 1
    print(f"Total stories fetched: {len(data)}")
