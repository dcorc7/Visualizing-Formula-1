# Formula 1 Data Analysis and Visualization Project

**Group 25**
<br>
David Corcoran, Yashwanth Devabathini, Sean Morris, Hung Tran

## Project Overview

This project provides a comprehensive visual analysis of Formula 1 racing, exploring the intricate factors that influence race outcomes and team performance. Through interactive visualizations and data-driven insights, we examine:

- **Track-Level Influences**: Analysis of iconic circuits like Monaco, Monza, Singapore, Spa-Francorchamps, and Circuit of the Americas, showcasing how each track's unique characteristics affect racing strategies and outcomes.
- **Team-Level Dynamics**: Examination of pit stop strategies, car development, and team performance over time.
- **Driver Performance**: Analysis of individual driver statistics, lap times, and race strategies.

The project features interactive visualizations that allow users to:
- Explore detailed track telemetry data
- Compare driver performances across different circuits
- Analyze team strategies and pit stop timing
- Visualize lap time evolution throughout races

This analysis aims to provide both F1 enthusiasts and newcomers with deeper insights into the technical and strategic aspects that make Formula 1 the pinnacle of motorsport.

# Project Setup Guide

## Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/gu-dsan5200/dsan5200-spring2025-project-group-25.git
   cd dsan5200-spring2025-project-group-25
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python3 -m venv 5200-project
   
   # Activate the environment
   # On macOS/Linux:
   source 5200-project/bin/activate
   # On Windows:
   .\5200-project\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. The project uses the following directory structure:
   - `code/`: Contains all source code
   - `data/`: Contains data files (raw, processed, analytical)
   - `img/`: Contains external images
   - `website/`: Contains the deployed website

5. To run the project:
   - Navigate to the appropriate directory based on what you want to run
   - Follow the specific instructions in the relevant subdirectory

## Running Streamlit Application Locally 

1. From the top directory, navigate to the `tracks/` directory:
    ```bash
    cd code/visualizations/tracks
    ```

2. Run the script using:
    ```bash
    streamlit run streamlit/app.py
    ```

    - This will call `init_db.py` from `database/` 
    - From there, the script will create and populate a .duckdb object using FastF1 API calls
    - The app uses this local db to update the plots much quicker than it would when trying to call the API dynamically



Georgetown University Domains-hosted fully rendered website is available for viewing [here](https://corcoran.georgetown.domains/5200-final/)