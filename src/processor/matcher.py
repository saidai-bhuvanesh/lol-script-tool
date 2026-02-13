from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict

class SemanticMatcher:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"Loading local semantic model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def calculate_relevance(self, resume_text: str, job_listings: List[Dict]) -> List[Dict]:
        """
        Calculate semantic similarity between resume and job titles/descriptions.
        Adds a 'semantic_score' key to each job dictionary.
        """
        if not job_listings:
            return []

        print("Calculating semantic match scores...")
        # Prepare job texts for comparison (Title + Company + Location)
        job_texts = [
            f"{job.get('title', '')} at {job.get('company', '')} in {job.get('location', '')}"
            for job in job_listings
        ]

        # Encode resume and jobs
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        job_embeddings = self.model.encode(job_texts, convert_to_tensor=True)

        # Calculate cosine similarity
        cosine_scores = util.cos_sim(resume_embedding, job_embeddings)[0]

        # Update jobs with scores
        for i, job in enumerate(job_listings):
            # Convert similarity (-1 to 1) to a 0-100 scale
            score = float(cosine_scores[i])
            score_percentage = round(max(0, score) * 100, 2)
            job['semantic_score'] = score_percentage
            job['relevance_score'] = int(score_percentage)
            
        print(f"Top local match score: {max([j.get('semantic_score', 0) for j in job_listings])}")
        return job_listings
