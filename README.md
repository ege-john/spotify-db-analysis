# Spotify Most Streamed Songs – Data Analysis & Database Project 🎵

This project analyzes Spotify’s most streamed songs using Python and SQL. It provides a structured database, data loading scripts, an ER diagram, and a simple Command-Line Interface (CLI) tool for running insightful queries about song trends, musical attributes, and global streaming habits.

## 📁 Files Included

- `DB & Big Data Project.pdf` — Full project report
- `README.md` — Project documentation
- `Spotify ER Diagram.png` — ER diagram of the database structure
- `Spotify Most Streamed Songs.csv` — Dataset
- `spotifydb_project.py` — Main Python application

---

## 📊 Project Overview

- **Dataset:** Contains detailed information and attributes of Spotify's most streamed songs.
- **Database:** The data is imported into a MySQL database with tables for Artists, Tracks, Platform Status, and relationships between them.
- **Analysis:** Python and SQL are used together to offer interactive data analysis and reveal trends about top tracks, artists, danceability, energy, and more.

## ✨ Features

- Imports CSV data into a normalized SQL database.
- Runs interactive CLI tool for data analysis.
- Answers questions like:
  - Top songs by year
  - Most streamed tracks
  - Trends in danceability, energy, and tempo
  - High valence (positive) songs
- Includes ER diagram and detailed documentation.

## 🚀 Instructions of Python Application

Once you run the code in `spotifydb_project.py`, the code will ask you for your MySQL credentials. You should be careful not to input wrong username or password. In case of a wrong input, it will ask you to input again.

After inputting correct credentials, the code will create database and tables. In case those steps are already done before, it will just skip them. Then, it will ask you if you want to load the data into the tables or not. Based on your decision, it will either load or skip this part as well.

Then the application will give you six data analysis queries and one exit option. If you input "0" it will stop running.

To see the results that you want, just input the number of that command and the application will give you the output. After that, it will ask you again until you exit the application.

**Here are the commands you can give:**
1. Yearly Trends: Top Song Per Year by Streams and Danceability
2. Top 5 High Valence Songs
3. Top 3 High Energy Years (>80%)
4. Top 10 Most Streamed Songs
5. Average Danceability by Release Year     
6. BPM Distribution on Each Decade  
0. Exit

e.g.: To see the "Top 5 High Valence Songs", input `2`.

If you enter an invalid command, it will give an error message and ask you to give a new command. 

---

*For more details, see the PDF report included in this repository.*
