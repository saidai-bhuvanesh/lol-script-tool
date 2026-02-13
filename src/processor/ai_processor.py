import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv
from .matcher import SemanticMatcher
from src.scraper.utils import fetch_job_description

load_dotenv()

class AIProcessor:
    def __init__(self):
        # 1. Initialize Local Semantic Matcher (Always available)
        self.matcher = SemanticMatcher()
        
        # 2. Initialize Gemini (Optional cloud AI)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY not found. Detailed cloud AI features will be limited.")
            self.model = None
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def process_jobs(self, jobs: List[Dict], resume_text: str) -> List[Dict]:
        # Step A: Local Semantic Matching (Fast)
        jobs = self.matcher.calculate_relevance(resume_text, jobs)

        if not self.model:
            print("Skipping detailed Cloud AI Processing (No API Key). Using local scores.")
            # Sort by local semantic score if no Gemini
            jobs.sort(key=lambda x: x.get("semantic_score", 0), reverse=True)
            return jobs[:50]

        processed_jobs = []
        # Step B: Gemini Detailed Analysis
        print(f"Top matches identified. Starting detailed AI analysis for top {min(len(jobs), 50)} jobs...")
        
        # Sort by semantic score first to prioritize what Gemini analyzes
        jobs.sort(key=lambda x: x.get("semantic_score", 0), reverse=True)
        top_jobs = jobs[:30] # Limit to top 30 for speed/token efficiency during deep fetch

        for job in top_jobs:
            print(f"Step B.1: Fetching full details for {job['title']} at {job['company']}...")
            # Automatically fetch the actual data from the job page
            full_description = await fetch_job_description(job['link'])
            
            print(f"Step B.2: AI Analysis & Cover Letter Generation for {job['company']}...")
            
            prompt = f"""
            Analyze this job opportunity for a candidate with this resume:
            
            Candidate Resume: {resume_text[:2000]}
            
            Job Details:
            Title: {job['title']}
            Company: {job['company']}
            Location: {job['location']}
            Full Job Content (Fetched): {full_description[:4000]} 
            
            Task:
            1. Determine if this job likely offers visa sponsorship (High/Medium/Low/Unknown).
            2. Extract or estimate the Salary Range.
            3. Rate relevance to candidate (0-100) based on specific skills in the Fetched Job Content.
            4. Provide a 2-sentence summary of why this is a good match.
            5. Generate a high-quality, professional, and personalized cover letter (3-4 paragraphs) 
               that mentions specific requirements found in the "Full Job Content".
            
            Output strictly in JSON format:
            {{
                "visa_sponsorship": "string",
                "salary": "string",
                "relevance_score": int,
                "summary": "string",
                "cover_letter": "string"
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                # Clean the response to ensure it's valid JSON
                text = response.text.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                
                import json
                analysis = json.loads(text)
                
                job.update(analysis)
                processed_jobs.append(job)
            except Exception as e:
                print(f"Error processing with AI: {e}")
                job.update({
                    "visa_sponsorship": "Unknown",
                    "salary": "Not Specified",
                    "relevance_score": 0,
                    "summary": "N/A",
                    "cover_letter": "N/A"
                })
                processed_jobs.append(job)
                
        # Sort by: 
        # 1. Visa Sponsorship (High first)
        # 2. Match Score (High first)
        processed_jobs.sort(key=lambda x: (x.get("visa_sponsorship") == "High", x.get("relevance_score", 0)), reverse=True)
        return processed_jobs[:50] # Return top 50
