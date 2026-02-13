import asyncio
import os
from dotenv import load_dotenv
from src.scraper.linkedin_scraper import LinkedInScraper
from src.scraper.remoteok_scraper import RemoteOkScraper
from src.processor.ai_processor import AIProcessor
from src.exporter.excel_exporter import ExcelExporter
from src.notifier.email_notifier import EmailNotifier

load_dotenv()

async def main():
    print("--- Starting AI Job Scraper ---")
    
    # 1. Configuration
    roles = os.getenv("TARGET_ROLES", "Software Engineer").split(",")
    locations = os.getenv("TARGET_LOCATIONS", "Germany,Netherlands").split(",")
    resume_path = os.getenv("RESUME_PATH", "")
    
    resume_text = ""
    if resume_path and os.path.exists(resume_path):
        try:
            with open(resume_path, "r", encoding='utf-8') as f:
                resume_text = f.read()
        except:
            resume_text = "Sample Resume: Senior Software Engineer, Python, AWS, React."
    else:
        resume_text = "Sample Resume: Senior Software Engineer, Python, AWS, React."

    # 2. Scraping
    print("Step 1: Scraping Jobs from multiple sources...")
    scrapers = [LinkedInScraper(), RemoteOkScraper()]
    
    raw_jobs = []
    for scraper in scrapers:
        try:
            results = await scraper.scrape(roles, locations)
            raw_jobs.extend(results)
        except Exception as e:
            print(f"Scraper error: {e}")
    
    print(f"Found {len(raw_jobs)} total raw job listings.")

    # 3. AI Processing
    print("Step 2: AI Filtering & Ranking...")
    processor = AIProcessor()
    processed_jobs = await processor.process_jobs(raw_jobs, resume_text)
    print(f"Processed {len(processed_jobs)} jobs.")

    # 4. Exporting
    print("Step 3: Generating Excel Report...")
    exporter = ExcelExporter()
    report_path = exporter.export(processed_jobs)

    # 5. Notifying
    print("Step 4: Sending Email Report...")
    notifier = EmailNotifier()
    notifier.send_report(report_path)

    print("--- Process Completed Successfully ---")

if __name__ == "__main__":
    asyncio.run(main())
