

# Class for API wrapper
"""
CRITICAL:
- 2009 to 2024

METHODS:
- Meetings
    - circuit_key: unique track identifier
    - meeting_key: unique meeting/event identifier (use latest to identify latest 
    or current meeting)
    - year: year of the event

################################################################################
ARCHITECTURE:
################################################################################

Client
- hold base url https://api.openf1.org/v1/
- Weather for each meeting, telemetry for each session
- Methods should accept explicit IDs (keys) or human-friendly 
identifiers for filtering by year, event, session, driver, and lap


Retrieval & Formatting
- each endpoints fetches JSON by default
- Convert JSON to pandas DataFrame

### MVP ###
- Fetch location data
- Fetch car telemetry data
- Identify sessions using year, event, and session type
- Mapping, mapping, mapping

################################################################################
NOTES
################################################################################

- Pull Meetings
- Use meeting_key to get sessions
    - filter for sessions with session_type = 'Race'

WEATHER DF
- use filtered sessions to get weather data
- left join weather data onto sessions data by session_key

CAR DATA DF
- use filtered sessions to get car data
- left join car data onto sessions data by session_key

RACE CONTROL DF
- use filtered sessions to get race control data
- left join race control data onto sessions data by session_key

"""




from urllib.request import urlopen
from urllib.parse import urlencode
import json
import pandas as pd
from typing import Optional

BASE_URL = 'https://api.openf1.org/v1/'

class OpenF1Client:
    def __init__(self):
        pass # No need to manage sessions for urlopen

    def get(self, endpoint: str, params: Optional[dict] = None) -> pd.DataFrame:
        """
        Generic method for fetching data from the API
        """
        query = f"?{urlencode(params)}" if params else ""
        url = BASE_URL + endpoint + query
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return pd.DataFrame(data)
    


    def get_meetings(self, year: int) -> pd.DataFrame:
        """
        Returns all meetings for a given year
        """
        return self.get('meetings', {'year': year})
    
    def get_sessions(self, meeting_key: str) -> pd.DataFrame:
        """
        Returns all sessions for a given meeting key
        - Consider only sessions with session_type = 'Race'
        """
        return self.get('sessions', {'meeting_key': meeting_key})
    
    def get_session_key(self, year: int, event_name: str, session_name: str) -> Optional[int]:
        meetings_df = self.get_meetings(year)
        matching_meeting = meetings_df[meetings_df['meeting_name'].str.contains(event_name, case=False, na=False)]
        if matching_meeting.empty:
            print(f"No meeting found for {event_name} in {year}")
            return None
        
        meeting_key = matching_meeting.iloc[0]['meeting_key']
        sessions_df = self.get_sessions(meeting_key)
        matching_session = sessions_df[sessions_df['session_name'].str.contains(session_name, case=False, na=False)]
        if matching_session.empty:
            print(f"No session found for {session_name} in {event_name} in {year}")
            return None
        
        return matching_session.iloc[0]['session_key']
    
    # Get weather data for a given session key
    def get_weather(self, session_key: int) -> pd.DataFrame:
        return self.get('weather', {'session_key': session_key})
    
    # Get car data for a given session key
    def get_car_data(self, session_key: int) -> pd.DataFrame:
        return self.get('car_data', {'session_key': session_key})
    
    # get race control data for a given session key
    def get_race_control(self, session_key: int) -> pd.DataFrame:
        return self.get('race_control', {'session_key': session_key})


"""
Log

What I've tested so far:
- Get all meetings for every year in the range
- Get all sessions for every meeting key in all_meetings_df
- Get weather data for every session in all_sessions_df

Notes
- Goal, specify data extraction by individual session
"""