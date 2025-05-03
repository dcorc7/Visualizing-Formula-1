from track_db import *

def test_track_db():
    # Test with just one race to keep it quick
    test_race = 'Monaco Grand Prix'
    test_year = 2024
    
    # Run the population function
    populate_race_data(test_year, test_race)
    
    # Verify the data was inserted correctly
    con = get_db_connection()
    
    # Check lap_summary table
    lap_summary = con.execute("""
        SELECT * FROM lap_summary 
        WHERE year = ? AND race_name = ?
    """, [test_year, test_race]).fetchdf()
    
    print("\nLap Summary Data:")
    print(lap_summary)
    
    # Check telemetry table
    telemetry = con.execute("""
        SELECT * FROM telemetry 
        WHERE year = ? AND race_name = ?
        LIMIT 5
    """, [test_year, test_race]).fetchdf()
    
    print("\nSample Telemetry Data:")
    print(telemetry)
    
    # Close the connection
    con.close()

def cleanup_test_data():
    con = get_db_connection()
    con.execute("DELETE FROM lap_summary WHERE year = 2024 AND race_name = 'Monaco Grand Prix'")
    con.execute("DELETE FROM telemetry WHERE year = 2024 AND race_name = 'Monaco Grand Prix'")
    con.close()
    print("Test data cleaned up")

if __name__ == "__main__":
    test_track_db()
    cleanup_test_data()