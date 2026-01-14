# NYC Bike Crash Dashboard

An interactive dashboard for exploring bike crash data across New York City.

## Features

- **Interactive Maps**: Visualize crash locations on an interactive map with PyDeck
- **Borough Filtering**: Filter crashes by NYC boroughs
- **Time Analysis**: Explore crashes by hour of day with interactive sliders
- **Injury Metrics**: Filter by number of cyclists injured
- **Data Visualization**: Hourly histograms and key metrics display
- **Raw Data Access**: Toggle to view the underlying dataset

## Live Demo

Deploy this dashboard to Streamlit Cloud for free!

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone this repository:
```bash
git clone https://github.com/petersun825/Bike_Crash_Dashboard_NYC.git
cd Bike_Crash_Dashboard_NYC
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

1. Fork or push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select this repository
6. Set the main file path to `app.py`
7. Click "Deploy"

Your dashboard will be live in minutes!

## Data Source

The dashboard uses NYC bike crash data with the following key fields:
- Crash date and time
- Location (latitude, longitude, borough)
- Number of cyclists injured/killed
- Contributing factors
- Vehicle types involved

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **PyDeck**: WebGL-powered map visualizations
- **Python**: Core programming language

## License

MIT License
