from dataclasses import dataclass
import argparse
import math
import os
import sys
from typing import List, Optional

import pandas as pd


@dataclass
class Movie:
    """Represents a single movie record."""
    id: str
    title_type: str
    title: str
    start_year: Optional[int]
    runtime_minutes: Optional[float]
    genres: List[str]
    rating: Optional[float]
    num_votes: Optional[int]


class MovieParser:
    """Loads the Excel sheet and converts rows to Movie objects."""

    def __init__(self, file_path: str, sheet_name: str = "title.basics"):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.movies: List[Movie] = []

    def load_data(self) -> None:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

        df["startYear"] = pd.to_numeric(df.get("startYear"), errors="coerce")
        df["runtimeMinutes"] = pd.to_numeric(
            df.get("runtimeMinutes"), errors="coerce")
        df["rating"] = pd.to_numeric(df.get("rating"), errors="coerce")
        df["numVotes"] = pd.to_numeric(df.get("numVotes"), errors="coerce")

        for _, row in df.iterrows():
            genres_field = row.get("genres", "")
            if isinstance(genres_field, str):
                genres = [g.strip()
                          for g in genres_field.split(",") if g.strip()]
            else:
                genres = []

            movie = Movie(
                id=str(row.get("id", "")),
                title_type=str(row.get("titleType", "")),
                title=str(row.get("originalTitle",
                          row.get("primaryTitle", ""))),
                start_year=int(row["startYear"]) if not pd.isna(
                    row["startYear"]) else None,
                runtime_minutes=float(row["runtimeMinutes"]) if not pd.isna(
                    row["runtimeMinutes"]) else None,
                genres=genres,
                rating=float(row["rating"]) if not pd.isna(
                    row["rating"]) else None,
                num_votes=int(row["numVotes"]) if not pd.isna(
                    row["numVotes"]) else None,
            )
            self.movies.append(movie)


class MovieReports:
    """Generate requested reports from a list of Movie objects."""

    def __init__(self, movies: List[Movie]):
        self.movies = movies

    def report_by_year(self, year: int) -> None:
        filtered = [m for m in self.movies if m.start_year ==
                    year and m.rating is not None]
        if not filtered:
            print(f"No movies found for year {year}")
            return

        highest = max(filtered, key=lambda m: (m.rating, m.num_votes or 0))
        lowest = min(filtered, key=lambda m: (m.rating, -(m.num_votes or 0)))

        runtimes = [
            m.runtime_minutes for m in filtered if m.runtime_minutes is not None]
        avg_runtime = sum(runtimes) / len(runtimes) if runtimes else 0.0

        print(f"Highest rating: {highest.rating:.1f} - {highest.title}")
        print(f"Lowest rating: {lowest.rating:.1f} - {lowest.title}")
        print(f"Average mean minutes: {avg_runtime:.1f}")

    def report_by_genre(self, genre: str) -> None:
        genre_lower = genre.strip().lower()
        filtered = [m for m in self.movies if any(
            g.lower() == genre_lower for g in m.genres) and m.rating is not None]
        if not filtered:
            print(f"No movies found for genre '{genre}'")
            return

        avg_rating = sum(m.rating for m in filtered) / len(filtered)
        print(f"Movies found: {len(filtered)}")
        print(f"Average mean rating: {avg_rating:.1f}")

    def top_rated_by_year_with_likes(self, year: int) -> None:
        filtered = [m for m in self.movies if m.start_year ==
                    year and m.rating is not None and m.num_votes]
        if not filtered:
            print(f"No movies found for year {year}")
            return

        sorted_movies = sorted(
            filtered, key=lambda m: (-m.rating, -(m.num_votes or 0)))[:10]
        max_votes = sorted_movies[0].num_votes or 0

        likes_divisor = max(1, math.ceil(max_votes / 80))

        for m in sorted_movies:
            votes = m.num_votes or 0
            smiles = math.ceil(votes / likes_divisor) if votes > 0 else 0
            smiles = min(smiles, 80)
            emoji_str = "😀" * smiles
            print(m.title)
            print(f"{emoji_str} {votes}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate movie reports from dataset.")
    parser.add_argument("-r", "--year_report", type=int,
                        help="Report (highest/lowest rating + avg runtime) for given year")
    parser.add_argument("-g", "--genre_report", type=str,
                        help="Report (count + avg rating) for given genre")
    parser.add_argument("-v", "--votes_report", type=int,
                        help="Top 10 highest rated movies for given year (shows votes as 😀)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not (args.year_report or args.genre_report or args.votes_report):
        print("At least one report option must be provided. Use -h for help.")
        sys.exit(1)

    file_path = os.getenv("MOVIES_FILE_PATH")
    if not file_path:
        print("Environment variable MOVIES_FILE_PATH is not set. Please set it to the Excel file path.")
        sys.exit(2)

    try:
        parser = MovieParser(file_path=file_path)
        parser.load_data()
    except Exception as exc:
        print(f"Failed to load data: {exc}")
        sys.exit(3)

    reports = MovieReports(parser.movies)

    if args.year_report:
        reports.report_by_year(args.year_report)
    if args.genre_report:
        reports.report_by_genre(args.genre_report)
    if args.votes_report:
        reports.top_rated_by_year_with_likes(args.votes_report)


if __name__ == "__main__":
    main()
