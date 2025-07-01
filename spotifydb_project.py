import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd

# MySQL DB credentials
while True:
    try:
        user = input("Enter your MySQL username: ")
        password = input("Enter your MySQL password: ")
        db = mysql.connect(host="localhost", user=user, passwd=password)
        break
    except Error as e:
        print("Error: Invalid username or password. Please try again.")


# Database Creation
def createdb(user:str, passw:str):
    db = mysql.connect(host="localhost", user=user, passwd=passw)
    curs = db.cursor()

    databasecreation = """
                        CREATE DATABASE SpotifyDB
                    """

    curs.execute(databasecreation)

# Table Creation
def creattables(user: str, passw: str):
    db = mysql.connect(host="localhost", user=user, passwd=passw, database="SpotifyDB")
    curs = db.cursor()

    name_table_1 = """
        CREATE TABLE Artist (
            artist_id VARCHAR(255) PRIMARY KEY,
            artist_name VARCHAR(255) NOT NULL,
            artist_count INT
        );
    """

    name_table_2 = """
        CREATE TABLE Track (
            track_id VARCHAR(255) PRIMARY KEY,
            track_name VARCHAR(255) NOT NULL,
            released_year INT,
            released_month INT,
            released_day INT,
            streams BIGINT,
            bpm FLOAT,
            song_key VARCHAR(5),
            song_mode VARCHAR(10),
            danceability FLOAT,
            valence FLOAT,
            energy FLOAT,
            acousticness FLOAT,
            instrumentalness FLOAT,
            liveness FLOAT,
            speechiness FLOAT,
            cover_url TEXT
        );
    """

    name_table_3 = """
        CREATE TABLE Platform_Status (
            song_id VARCHAR(255) PRIMARY KEY,
            in_spotify_playlist BIGINT,
            in_spotify_charts BIGINT,
            in_apple_playlist BIGINT,
            in_apple_charts BIGINT,
            in_deezer_playlist BIGINT,
            in_deezer_charts BIGINT,
            in_shazam_charts BIGINT
        );
    """

    name_table_4 = """
        CREATE TABLE Performs (
            artist_id VARCHAR(255),
            track_id VARCHAR(255),
            PRIMARY KEY (artist_id, track_id),
            FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
            FOREIGN KEY (track_id) REFERENCES Track(track_id)
        );
    """

    name_table_5 = """
        CREATE TABLE Appears (
            track_id VARCHAR(255),
            song_id VARCHAR(255),
            PRIMARY KEY (track_id, song_id),
            FOREIGN KEY (track_id) REFERENCES Track(track_id),
            FOREIGN KEY (song_id) REFERENCES Platform_Status(song_id)
        );
    """

    curs.execute(name_table_1)
    curs.execute(name_table_2)
    curs.execute(name_table_3)
    curs.execute(name_table_4)
    curs.execute(name_table_5)


# Dataloading
def dataload(user: str, passw: str):
    datafile = "Spotify Most Streamed Songs.csv"
    db = mysql.connect(host="localhost", user=user, passwd=passw, database="SpotifyDB")
    curs = db.cursor()

    data = pd.read_csv(datafile, index_col=False, delimiter=",", encoding="UTF-8")

    # Inserting data into all tables
    for index, row in data.iterrows():

        row = row.where(pd.notnull(row), None)  # Converting NaN values to None

        # Artist table
        artist_names = row['artist(s)_name'].split(', ')
        artist_id = index # Using the row number for ID
        artist_count = len(artist_names)
        artist_query = """
                        INSERT IGNORE INTO Artist (artist_id, artist_name, artist_count) VALUES (%s, %s, %s)
                    """
        curs.execute(artist_query, (artist_id, ', '.join(artist_names), artist_count))

        # Track table
        track_id = index
        track_query = """
                    INSERT IGNORE INTO Track (track_id, track_name, released_year, released_month, released_day, streams, bpm, song_key, song_mode, danceability, valence, energy, acousticness, instrumentalness, liveness, speechiness, cover_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        curs.execute(track_query, (
            track_id, row['track_name'], row['released_year'], row['released_month'], row['released_day'],
            row['streams'], row['bpm'], row['key'], row['mode'], row['danceability_%'],
            row['valence_%'], row['energy_%'], row['acousticness_%'],
            row['instrumentalness_%'], row['liveness_%'], row['speechiness_%'], row['cover_url']
        ))

        # Platform_Status table
        song_id = index
        platform_status_query = """
                                INSERT IGNORE INTO Platform_Status (song_id, in_spotify_playlist, in_spotify_charts, in_apple_playlist, in_apple_charts, in_deezer_playlist, in_deezer_charts, in_shazam_charts)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """
        curs.execute(platform_status_query, (
            song_id, row['in_spotify_playlists'], row['in_spotify_charts'], row['in_apple_playlists'],
            row['in_apple_charts'], row['in_deezer_playlists'], row['in_deezer_charts'], row['in_shazam_charts']
        ))

        # Performs table
        performs_query = """
                        INSERT IGNORE INTO Performs (artist_id, track_id) VALUES (%s, %s)
                    """
        curs.execute(performs_query, (artist_id, track_id))

        # Appears table
        appears_query = "INSERT IGNORE INTO Appears (track_id, song_id) VALUES (%s, %s)"
        curs.execute(appears_query, (track_id, song_id))

    db.commit()
    db.close()


# User Query Interface
def user_interface():
    db = mysql.connect(host="localhost", user=user, passwd=password, database="SpotifyDB")
    curs = db.cursor()

    print("\n Welcome to Spotify Data Analysis!")

    while True:
        print("\n Choose an option to analyze:")
        print("1. Yearly Trends: Top Song Per Year by Streams and Danceability")
        print("2. Top 5 High Valence Songs")
        print("3. Top 3 High Energy Years (>80%)")
        print("4. Top 10 Most Streamed Songs")
        print("5. Average Danceability by Release Year")
        print("6. BPM Distribution on Each Decade")   
        print("0. Exit.")
            
        choice = int(input("\n Enter your choice: "))

        if choice == 1:
            query = """
                        WITH YearlyTopSongs AS (
                        SELECT 
                            released_year, 
                            track_name, 
                            streams,
                            danceability,
                            ROW_NUMBER() OVER (PARTITION BY released_year ORDER BY streams DESC) AS `rank`
                        FROM track
                    )
                    SELECT released_year, track_name, streams, danceability
                    FROM YearlyTopSongs
                    WHERE `rank` = 1;
                """
            curs.execute(query)
            results = curs.fetchall()
            # DataFrame for better visualization
            df = pd.DataFrame(results, columns=['Released Year', 'Track Name', 'Streams', 'Danceability'])
            print("\n Yearly Trends: Top Song Per Year by Streams and Danceability: \n")
            print(df.to_string(index=False))  # Display DataFrame without the index

        elif choice == 2:
            query = """
                    SELECT track_name, streams, valence
                    FROM track
                    WHERE valence > 0.7
                    ORDER BY valence DESC
                    LIMIT 5;
                """
            curs.execute(query)
            results = curs.fetchall()
            df = pd.DataFrame(results, columns=['Track Name', 'Streams', 'Valence'])
            print("\n Top 5 High Valence Songs: \n")
            print(df.to_string(index=False))

        elif choice == 3:
            query = """
                    SELECT released_year, COUNT(*) AS high_energy_songs
                    FROM track
                    WHERE energy > 0.8
                    GROUP BY released_year
                    ORDER BY high_energy_songs DESC
                    LIMIT 3;
                """
            curs.execute(query)
            results = curs.fetchall()
            df = pd.DataFrame(results, columns=['Released Year', 'High Energy Songs'])
            print("\n Top 3 High Energy Years (>80%): \n")
            print(df.to_string(index=False))

        elif choice == 4:
            query = """
                    SELECT track_name, streams
                    FROM track
                    ORDER BY streams DESC
                    LIMIT 10;
                """
            curs.execute(query)
            results = curs.fetchall()
            df = pd.DataFrame(results, columns=['Track Name', 'Streams'])
            print("\n Top 10 Most Streamed Songs: \n")
            print(df.to_string(index=False))

        elif choice == 5:
            query = """
                    SELECT released_year, AVG(danceability) AS avg_danceability
                    FROM track
                    GROUP BY released_year
                    ORDER BY released_year;
                """ 
            curs.execute(query)
            results = curs.fetchall()
            df = pd.DataFrame(results, columns=['Released Year', 'Average Danceability'])
            df['Average Danceability'] = df['Average Danceability'].map('{:.2f}'.format)
            print("\n Average Danceability by Release Year: \n")
            print(df.to_string(index=False))

        elif choice == 6:
            query = """
                    WITH BPM_Categories AS (
                        SELECT 
                            FLOOR(released_year / 10) * 10 AS decade,
                            bpm,
                            CASE 
                                WHEN bpm < 100 THEN 'Slow'
                                WHEN bpm BETWEEN 100 AND 120 THEN 'Moderate'
                                WHEN bpm BETWEEN 120 AND 150 THEN 'Fast'
                                ELSE 'Very Fast'
                            END AS bpm_category
                        FROM track
                    ),
                    DecadeBPMAnalysis AS (
                        SELECT 
                            decade,
                            bpm_category,
                            AVG(bpm) AS avg_bpm
                        FROM BPM_Categories
                        GROUP BY decade, bpm_category
                    ),
                    RankedCategories AS (
                        SELECT 
                            decade,
                            bpm_category,
                            avg_bpm,
                            ROW_NUMBER() OVER (PARTITION BY decade ORDER BY avg_bpm DESC) AS `rank`
                        FROM DecadeBPMAnalysis
                    )
                    SELECT decade, bpm_category, avg_bpm
                    FROM RankedCategories
                    WHERE `rank` = 1
                    ORDER BY decade;
                """
            curs.execute(query)
            results = curs.fetchall()
            df = pd.DataFrame(results, columns=['Decade', 'BPM Category', 'Average BPM'])
            df['Average BPM'] = df['Average BPM'].map('{:.2f}'.format)
            print("\n BPM Distribution on Each Decade: \n")
            print(df.to_string(index=False))

        elif choice == 0:
            print("\n Exiting... Goodbye! \n")
            break

        else:
            print("\n Invalid choice. Try again. \n")


# Main Function
def main():

    try:
        print("Creating the database...")
        createdb(user=user, passw=password)
        print("--> Database created successfully.")
    except Error as e:
        print("--> The database already exists.")

    try:
        print("Defining tables...")
        creattables(user=user, passw=password)
        print("--> Tables created successfully.")
    except Error as e:
        print("--> The tables already exist.")

    try:
        while True:
            load_choice = input("Do you want to load the dataset? (y/n): ").strip().lower()

            if load_choice == 'y':
                dataload(user=user, passw=password)
                print("--> Dataset loaded successfully.")
                break
            elif load_choice == 'n':
                print("--> Skipped dataset loading.")
                break
            else:    
                print("--> Invalid input. Try again.")
    except Error as e:
        print("--> There is an error occurred while loading the dataset.")

    # Running the user interface
    user_interface()

if __name__ == "__main__":
    main()