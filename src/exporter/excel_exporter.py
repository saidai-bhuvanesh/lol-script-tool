import pandas as pd
from datetime import datetime
import os

class ExcelExporter:
    @staticmethod
    def export(jobs: list, output_dir: str = "data") -> str:
        if not jobs:
            print("No jobs to export.")
            return ""
            
        df = pd.DataFrame(jobs)
        
        # Ensure all columns exist even if AI processing was skipped
        required_cols = ["visa_sponsorship", "salary", "relevance_score", "summary", "cover_letter"]
        for col in required_cols:
            if col not in df.columns:
                if col == "salary":
                    df[col] = "Not Specified"
                else:
                    df[col] = "N/A"

        # Select and rename columns for the final report
        cols = [
            "visa_sponsorship", "salary", "title", "company", "location", "link", 
            "summary", "cover_letter", "relevance_score"
        ]
        df = df[cols]
        df.columns = [
            "Visa Sponsorship", "Salary Range", "Job Role", "Company Name", "Location", 
            "Apply Link", "Job Summary", "Custom Cover Letter", "Match Score"
        ]
        
        print("\n--- Preview of Exported Data ---")
        print(df[["Job Role", "Match Score"]].head())
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"Daily_Abroad_Jobs_{timestamp}.xlsx"
        filepath = os.path.join(output_dir, filename)
        
        df.to_excel(filepath, index=False)
        print(f"Report generated: {filepath}")
        return filepath
