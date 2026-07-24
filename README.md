# RailPulse SQL Analysis

An interactive Python application for analyzing railway data using SQLite, focused on Belgian rail transportation (SNCB) with SQL queries to extract insights about service patterns, accessibility, and peak hours.

## Overview

RailPulse SQL Analysis retrieves railway transportation data from an API and stores it in a SQLite database, then provides tools to analyze various aspects of the rail network including:

- **Peak hour identification** - Determine when the busiest travel times occur
- **Platform analysis** - Discover the busiest platforms at specific stations
- **Morning destinations** - Identify the most frequently visited destinations during morning hours
- **Service frequency** - Analyze and track service schedules
- **Accessibility audits** - Review accessibility features across the network

## Getting Started

### Prerequisites

- Python 3.x
- SQLite3
- Access to railway data API

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Max96H/railpulse_sql_analysis.git
cd railpulse_sql_analysis
```

2. Install dependencies (if any requirements file exists):
```bash
pip install -r requirements.txt
```

### Usage

Run the application with:
```bash
python main.py
```

The application presents an interactive menu where you can:

1. **Create/Recreate Database Tables** - Initialize or reset the database schema
2. **Extract and Insert Data** - Fetch data from the API and populate the database
3. **Run Analysis Queries**:
   - Peak hour analysis
   - Busiest platforms by station
   - Morning destination patterns
   - Service frequency queries
   - Accessibility audits

#### Interactive Menu Example

```
Do you want to recreate the tables of the database? (y|n)
> y

Do you want to extract and insert data from the API to db? (y|n)
> y

Do you wish to query the peak hour? (y|n)
> y

Do you wish to know the busiest platforms? (y|n)
> y
From which station? (Default: 'Bruxelles-Central')
> Bruxelles-Central
Top how many? (Default: 3)
> 5
```

## Project Structure

```
railpulse_sql_analysis/
├── main.py                      # Main entry point with interactive menu
├── data/
│   └── sncb.db                 # SQLite database file
├── src/
│   ├── creation.py             # Database table creation logic
│   ├── insertion.py            # Data extraction and insertion
│   ├── peak_hour.py            # Peak hour query
│   ├── busy_platforms.py        # Platform analysis queries
│   ├── morning_destinations.py # Morning destination queries
│   ├── service_frequency.py    # Service frequency analysis
│   ├── accessibility.py        # Accessibility audit queries
│   └── diagnosis.py            # Diagnostic utilities
└── README.md
```

## Key Features

- **SQLite Database** - Efficient local storage of railway data
- **Interactive CLI** - User-friendly command-line interface for running analyses
- **Modular Design** - Separate modules for different analysis types
- **API Integration** - Automatic data extraction from railway API
- **Flexible Queries** - Customizable parameters (e.g., station selection, top-N results)

## Database Configuration

The database is configured with:
- **Location**: `./data/sncb.db`
- **Type Detection**: SQLite PARSE_DECLTYPES and PARSE_COLNAMES enabled
- **Comment**: WAL (Write-Ahead Logging) pragma available for performance optimization

## Notes

- The database file is created automatically on first run
- Ensure the `data/` directory exists or is writable
- Some queries accept default values if no input is provided

## License

This project is unlicensed. See LICENSE file for more details.

## Contributing

Feel free to open issues and submit pull requests to improve the analysis capabilities or add new features.

---

**Built with**: Python, SQLite, Railway Data API
