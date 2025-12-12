# recommendation.py
"""
Task 3 - Content-based Movie Recommendation (CodSoft AI Internship)

Run: python recommendation.py
Designed to run in VS Code terminal (CPU friendly).

Features:
- Uses TF-IDF on movie 'description' + 'genres'
- Computes cosine similarity to recommend similar movies
- If no dataset found, creates a small sample movies CSV automatically
- Saves recommendation results for demo in `rec_results.jsonl`
"""

import os
import json
from datetime import datetime

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MOVIES_FILE = "movies_sample.csv"
RESULTS_FILE = "rec_results.jsonl"

SAMPLE_MOVIES = [
    {"movieId": 1, "title": "The Shawshank Redemption", "genres": "Drama", "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption."},
    {"movieId": 2, "title": "The Godfather", "genres": "Crime|Drama", "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
    {"movieId": 3, "title": "The Dark Knight", "genres": "Action|Crime|Drama", "description": "When the menace known as the Joker wreaks havoc, Batman must accept one of the greatest psychological and physical tests."},
    {"movieId": 4, "title": "Pulp Fiction", "genres": "Crime|Drama", "description": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption."},
    {"movieId": 5, "title": "Forrest Gump", "genres": "Drama|Romance", "description": "The presidencies of Kennedy and Johnson, Vietnam, Watergate and other history unfold through the perspective of an Alabama man."},
    {"movieId": 6, "title": "Inception", "genres": "Action|Sci-Fi|Thriller", "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."},
    {"movieId": 7, "title": "Interstellar", "genres": "Adventure|Drama|Sci-Fi", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
    {"movieId": 8, "title": "The Matrix", "genres": "Action|Sci-Fi", "description": "A hacker discovers the world is a simulated reality and joins a rebellion to free humanity."},
    {"movieId": 9, "title": "The Lion King", "genres": "Animation|Adventure|Drama", "description": "A young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery."},
    {"movieId": 10, "title": "Fight Club", "genres": "Drama", "description": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much more."}
]

def ensure_movies_file():
    if not os.path.isfile(MOVIES_FILE):
        print(f"[Info] '{MOVIES_FILE}' not found — creating sample dataset.")
        df = pd.DataFrame(SAMPLE_MOVIES)
        df.to_csv(MOVIES_FILE, index=False)
    else:
        print(f"[Info] Using dataset: {MOVIES_FILE}")

def load_movies():
    df = pd.read_csv(MOVIES_FILE)
    # Ensure needed columns
    if "description" not in df.columns:
        df["description"] = df.get("overview", "")  # try common alt name
    # Fill NaNs
    df["description"] = df["description"].fillna("")
    df["genres"] = df["genres"].fillna("").astype(str)
    # Create a combined text field
    df["combined"] = (df["title"].astype(str) + " " + df["genres"].replace("|", " ") + " " + df["description"].astype(str))
    return df

def build_tfidf_matrix(series):
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
    mat = tfidf.fit_transform(series)
    return tfidf, mat

def compute_similarity_matrix(tfidf_matrix):
    sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return sim

def recommend_movies(df, sim_matrix, title, top_n=5):
    title = title.strip().lower()
    # Find index
    matches = df[df["title"].str.lower() == title]
    if matches.empty:
        # try partial match
        matches = df[df["title"].str.lower().str.contains(title)]
    if matches.empty:
        return None, f"No movie found for title query: '{title}'"

    idx = matches.index[0]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # skip first (itself)
    top_indices = [i for i, score in sim_scores[1: top_n+1]]
    recommendations = df.iloc[top_indices][["movieId", "title", "genres", "description"]].to_dict(orient="records")
    return recommendations, None

def save_result_log(query_title, recommendations):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query_title,
        "recommendations": recommendations
    }
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def interactive_loop(df, sim_matrix):
    print("\n=== Content-based Movie Recommender ===")
    print("Type a movie title to get recommendations (e.g., 'Inception').")
    print("Type 'list' to see available movie titles.")
    print("Type 'exit' to quit.\n")

    while True:
        q = input("Enter movie title / command: ").strip()
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            print("Exiting recommender. Good luck with the internship!")
            break
        if q.lower() == "list":
            print("\nAvailable titles:")
            for t in df["title"].tolist():
                print(" -", t)
            print()
            continue

        recommendations, err = recommend_movies(df, sim_matrix, q, top_n=5)
        if err:
            print("Error:", err)
            # try fuzzy suggestion: show top 5 titles that contain the query substring
            suggestions = df[df["title"].str.lower().str.contains(q.lower())]["title"].tolist()
            if suggestions:
                print("Did you mean:")
                for s in suggestions[:6]:
                    print("  >", s)
            continue

        print(f"\nTop recommendations for '{q}':")
        for i, rec in enumerate(recommendations, start=1):
            print(f"{i}. {rec['title']}  ({rec['genres']})")
            # print a short description (first 140 chars)
            desc = rec.get("description", "")
            if desc:
                print("    ", desc[:140] + ("..." if len(desc) > 140 else ""))
        print()
        save_result_log(q, recommendations)
        print(f"[Saved] Recommendations appended to {RESULTS_FILE}\n")

def main():
    ensure_movies_file()
    df = load_movies()
    tfidf, matrix = build_tfidf_matrix(df["combined"])
    sim = compute_similarity_matrix(matrix)
    interactive_loop(df, sim)

if __name__ == "__main__":
    main()