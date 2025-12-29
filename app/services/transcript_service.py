"""
Service for fetching and processing YouTube transcripts with Selenium fallback.
"""
import time
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import HTTPException
from app.utils.helpers import extract_video_id_from_url

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app.core.logging_config import logger


class TranscriptService:
    def __init__(self):
        pass

    def fetch_transcript(self, video_url: str, languages: list = None) -> str:
        if languages is None:
            languages = ['en', 'hi', 'ur']
        
        video_id = extract_video_id_from_url(video_url)
        logger.info(f"Attempting API fetch for video_id={video_id}")

        # --- OPTION 1: Try YouTube Transcript API ---
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            transcript = " ".join([item['text'] for item in transcript_list])
            if transcript.strip():
                logger.info("Transcript successfully fetched via API")
                return transcript
        except Exception as e:
            logger.warning(f"API fetch failed for video_id={video_id}. Error: {str(e)}. Switching to Selenium fallback.")

        # --- OPTION 2: Fallback to Selenium Scraping ---
        scraped_text = self._scrape_transcript_fallback(video_url)
        
        # Validation: Ensure we didn't just get headers or empty strings
        if scraped_text and len(scraped_text) > 200:
            logger.info("Transcript successfully fetched via Selenium scraper")
            return scraped_text
        
        logger.error("Transcript unavailable. API failed and Scraper returned insufficient data.")
        raise HTTPException(
            status_code=404,
            detail="Transcript unavailable. API failed and Scraper returned insufficient data."
        )

    def _scrape_transcript_fallback(self, youtube_url: str) -> str:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Uses the newer, more stable headless engine
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logger.debug("Chrome WebDriver initialized")

        try:
            driver.get("https://tactiq.io/tools/youtube-transcript")
            wait = WebDriverWait(driver, 30)
            
            # 1. Enter URL
            input_field = wait.until(EC.element_to_be_clickable((By.ID, "yt-2")))
            input_field.send_keys(youtube_url)
            logger.debug("YouTube URL entered into transcript tool")

            # 2. Submit
            btn = driver.find_element(By.CSS_SELECTOR, "input[value='Get Video Transcript']")
            driver.execute_script("arguments[0].click();", btn)  # JS click is more reliable
            logger.debug("Transcript request submitted")

            # 3. Wait for the 'Copy' button to signal completion
            wait.until(EC.presence_of_element_located((By.ID, "copy")))
            time.sleep(3)  # Essential: Wait for JS to finish rendering
            logger.debug("Waited for transcript to render")

            # 4. Extract transcript
            transcript_result = ""
            elements = driver.find_elements(By.CSS_SELECTOR, "[data-astro-cid-puhxsgk4]")
            
            if len(elements) > 5:
                transcript_result = "\n".join([el.text for el in elements if len(el.text) > 2])
            else:
                try:
                    anchor = driver.find_element(By.XPATH, "//*[contains(text(), '00:00')]")
                    parent = anchor.find_element(By.XPATH, "./..")
                    transcript_result = parent.text
                except Exception:
                    logger.warning("Fallback extraction failed; no timestamp anchor found")

            logger.info(f"Transcript extracted with length={len(transcript_result)} characters")
            return transcript_result.strip()

        except Exception as e:
            logger.error(f"Selenium scraper error: {e}")
            return ""
        finally:
            logger.debug("Closing Chrome WebDriver")
            driver.quit()
