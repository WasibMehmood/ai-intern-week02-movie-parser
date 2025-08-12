# Movies Parser 🎬

A simple Python CLI app that generates movie reports from an Excel dataset.  
Reports include:
- Highest/lowest rated movies for a given year.
- Average runtime for a year.
- Genre-based movie count and average rating.
- Top 10 highest-rated movies for a year with vote-based likes.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/WasibMehmood/movies-parser.git
   cd movies-parser

## Activate Virtual Env
```bash
movie-gen\Scripts\Activate
```
### Install Necessary Dependencies
```bash
pip install pandas
pip install pandas openpyxl
```
### Set Movie Path
```bash
set MOVIES_FILE_PATH = Moviesdataset.xlsx
```
# Run the Output
```bash
- python movies_parser.py -r 1903
- python movies_parser.py -g Comedy
- python movies_parser.py -v 1892
- python movies_parser.py -r 1903 -g Comedy -v 1895
```
