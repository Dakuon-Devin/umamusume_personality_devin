import base64
import os
from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

load_dotenv()


class CharacterScraper:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    def _take_screenshot(self, url: str) -> bytes:
        """Take a screenshot of the character page."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            # Wait for the character profile section to load
            page.wait_for_selector(".character-profile", timeout=10000)
            screenshot = page.screenshot(full_page=True)
            browser.close()
            return screenshot
    def _encode_image(self, image_bytes: bytes) -> str:
        """Encode the image bytes to base64."""
        return base64.b64encode(image_bytes).decode("utf-8")
    def _extract_character_info(self, image_bytes: bytes) -> Dict[str, str]:
        """Extract character information using OpenAI's Vision API."""
        base64_image = self._encode_image(image_bytes)

        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "この画像からウマ娘のキャラクター情報を抽出してください。"
                                "キャラクターの名前と性格の特徴を日本語で説明してください。"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        # Extract the character information from the response
        character_info = response.choices[0].message.content

        # Parse the response to extract name and personality
        # This is a simple implementation and might need to be improved
        lines = character_info.split("\n")
        name = lines[0].replace("名前：", "").strip()
        personality = "\n".join(lines[1:]).strip()

        return {
            "name": name,
            "profile": personality,
        }
    def scrape_character(self, url: str) -> Dict[str, str]:
        """Scrape character information from the given URL."""
        try:
            screenshot = self._take_screenshot(url)
            character_info = self._extract_character_info(screenshot)
            character_info["url"] = url
            return character_info
        except Exception as e:
            print(f"Error scraping character from {url}: {str(e)}")
            return None
    def scrape_characters(self, urls: List[str]) -> List[Dict[str, str]]:
        """Scrape multiple characters from the given URLs."""
        characters = []
        for url in urls:
            character = self.scrape_character(url)
            if character:
                characters.append(character)
        return characters
