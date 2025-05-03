import duckdb
import fastf1 as ff1
import pandas as pd
from pathlib import Path
import logging
logging.getLogger('fastf1').setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore")


RACE_NAMES = [
    'Monaco Grand Prix',
    'Italian Grand Prix',
    'Singapore Grand Prix',
    'Belgian Grand Prix',
    'United States Grand Prix'
]

YEAR = 2024

## DATABASE HELPER FUNCTIONS

def get_db_connection():
    db_path = Path(__file__).resolve().parent / 'track_db.duckdb'
    print(f"[DEBUG] Connecting to DuckDB at path: {db_path}")
    return duckdb.connect(str(db_path), read_only=True)

def create_tables(con):
    """
    Creates lap_summary and telemetry tables
    - Table to store information for selected laps
    - lap_category: 'fastest' and 'slowest' for each driver, and 'overall' fastest lap
    """
    con.execute("""
    CREATE TABLE IF NOT EXISTS lap_summary (
        year INTEGER,
        race_name VARCHAR,
        driver_code VARCHAR,
        lap_category VARCHAR,
        lap_number INTEGER,
        lap_time FLOAT            
    )
    """)
    # Table to store telemetry data for each stored lap
    con.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        year INTEGER,
        race_name VARCHAR,
        driver_code VARCHAR,
        lap_category VARCHAR,
        lap_number INTEGER,
        telemetry_index INTEGER,
        X FLOAT,
        Y FLOAT,
        Speed FLOAT,
        Throttle FLOAT,
        nGear INTEGER,
        Brake FLOAT,
        RPM FLOAT,
        Distance FLOAT
    )
    """)

def insert_lap_summary(
        con,
        year,
        race_name,
        driver_code,
        lap_category,
        lap_number,
        lap_time
):
    """
    Insert a single lap summary row
    """
    # Convert Timedelta to seconds if it's a Timedelta object
    if isinstance(lap_time, pd.Timedelta):
        lap_time = lap_time.total_seconds()
    
    con.execute("""
    INSERT INTO lap_summary (year, race_name, driver_code, lap_category, lap_number, lap_time)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [year, race_name, driver_code, lap_category, lap_number, lap_time])

def insert_telemetry(
        con,
        df_tel,
        year,
        race_name,
        driver_code,
        lap_category,
        lap_number
):
    """
    Insert telemetry data from a DataFrame into the telemetry table
    df_tel is expected to have the following columns:
    - X, Y, Speed, Throttle, nGear, Brake, RPM, Distance
    """
    df_tel = df_tel.copy()
    df_tel['year'] = year
    df_tel['race_name'] = race_name
    df_tel['driver_code'] = driver_code
    df_tel['lap_category'] = lap_category
    df_tel['lap_number'] = lap_number
    df_tel['telemetry_index'] = df_tel.index

    # ensure the dataframe follows the desired column order
    columns = ['year', 'race_name', 'driver_code', 'lap_category', 
               'lap_number', 'telemetry_index', 'X', 'Y', 'Speed', 
               'Throttle', 'nGear', 'Brake', 'RPM', 'Distance']
    df_tel = df_tel[columns]

    # Use DuckDB's register method for bulk insert.
    con.register("temp_tel", df_tel)
    con.execute("INSERT INTO telemetry SELECT * FROM temp_tel")
    con.unregister("temp_tel")


## FAST F1 HELPER FUNCTIONS

def load_race_session(year, race_name):
    """
    Load a race session and return a FastF1 Session object
    """
    session = ff1.get_session(year, race_name, 'Race')
    session.load()
    return session

def get_driver_laps(session, driver_code):
    """
    returns the laps for a given driver in the session
    """
    return session.laps.pick_driver(driver_code)

def populate_race_data(year, race_name):
    """
    For a given race, iterate over each driver in the race and store:
        - fastest lap and its telemetry
        - slowest lap and its telemetry
    Also store the overall fastest lap and its telemetry
    """
    con = get_db_connection()
    create_tables(con)

    print(f"Loading session for {race_name}...")
    session = load_race_session(year, race_name)

    # to track the overall fastest lap
    overall_fastest = None

    # process each driver from the race results
    results = session.results
    driver_codes = results['Abbreviation'].tolist()

    for driver in driver_codes:
        driver_laps = get_driver_laps(session, driver)
        # Filter out laps without a valid lap time
        driver_laps = driver_laps[driver_laps['Time'].notna()]
        if driver_laps.empty:
            print(f"No valid laps found for driver {driver}")
            continue

        # --- Driver's fastest lap ---
        try:
            fastest_lap = driver_laps.loc[driver_laps['LapTime'].idxmin()]
            lap_num_fast = fastest_lap['LapNumber']
            lap_time_fast = fastest_lap['LapTime']
            tel_fast = fastest_lap.get_telemetry().add_distance().reset_index(drop=True)
            # Insert driver fastest lap data
            insert_lap_summary(con, year, race_name, driver, 'fastest', lap_num_fast, lap_time_fast)
            insert_telemetry(con, tel_fast, year, race_name, driver, 'fastest', lap_num_fast)

            # --- Driver's slowest lap ---
            slowest_lap = driver_laps.loc[driver_laps['LapTime'].idxmax()]
            lap_num_slow = slowest_lap['LapNumber']
            lap_time_slow = slowest_lap['LapTime']
            tel_slow = slowest_lap.get_telemetry().add_distance().reset_index(drop=True)
            # Insert driver slowest lap data
            insert_lap_summary(con, year, race_name, driver, 'slowest', lap_num_slow, lap_time_slow)
            insert_telemetry(con, tel_slow, year, race_name, driver, 'slowest', lap_num_slow)

            # update overall fastest lap if this driver's fastest lap is faster
            if overall_fastest is None or lap_time_fast < overall_fastest[0]:
                overall_fastest = (lap_time_fast, driver, fastest_lap)
        except Exception as e:
            print(f"Error processing laps for driver {driver}: {str(e)}")
            continue

    # --- Overall fastest lap ---
    if overall_fastest is not None:
        try:
            lap_time_overall, driver_overall, lap_overall = overall_fastest
            lap_num_overall = lap_overall['LapNumber']
            tel_overall = lap_overall.get_telemetry().add_distance().reset_index(drop=True)
            insert_lap_summary(con, year, race_name, driver_overall, 'overall', lap_num_overall, lap_time_overall)
            insert_telemetry(con, tel_overall, year, race_name, driver_overall, 'overall', lap_num_overall)
        except Exception as e:
            print(f"Error processing overall fastest lap: {str(e)}")

    print(f"Data for {race_name} loaded into database")


def populate_all_races():
    """
    Populate the database with all selected races from 2024
    """
    # First, ensure the database and tables exist
    con = get_db_connection()
    create_tables(con)
    con.close()
    
    for race in RACE_NAMES:
        try:
            print(f"\nPopulating data for {race}...")
            populate_race_data(YEAR, race)
            
            # Verify data was inserted
            con = get_db_connection()
            count = con.execute("""
                SELECT COUNT(*) as count 
                FROM lap_summary 
                WHERE year = ? AND race_name = ?
            """, [YEAR, race]).fetchdf()['count'].iloc[0]
            print(f"Inserted {count} records for {race}")
            con.close()
            
        except Exception as e:
            print(f"Error populating data for {race}: {str(e)}")
            continue
            
    print("\nData for all races loaded into database")
    
    # Final verification
    con = get_db_connection()
    total_count = con.execute("""
        SELECT COUNT(*) as count 
        FROM lap_summary 
        WHERE year = ?
    """, [YEAR]).fetchdf()['count'].iloc[0]
    print(f"\nTotal records in database: {total_count}")
    con.close()

if __name__ == "__main__":
    # select distinct driver_codes from monaco grand prix
    con = get_db_connection()
    drivers = con.execute("""
    SELECT DISTINCT driver_code FROM lap_summary
    WHERE year = ? AND race_name = ?
    """, [2024, 'Monaco Grand Prix']).fetchdf()
    print(drivers)
    con.close()




