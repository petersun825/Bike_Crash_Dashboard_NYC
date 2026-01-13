import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="NYC Bike Crash Dashboard",
    page_icon="🚲",
    layout="wide",
)

DATA_URL = "sample_csv.csv"

def _clean_column_names(columns: pd.Index) -> pd.Index:
    """Normalize column names for easier querying."""
    return columns.str.strip().str.lower().str.replace(" ", "_", regex=False)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load and clean the crash dataset."""
    data = pd.read_csv(DATA_URL)
    data.columns = _clean_column_names(data.columns)

    # Build a combined datetime column and coerce invalid rows to NaT for safe filtering.
    data["date/time"] = pd.to_datetime(
        data["crash_date"].str.strip() + " " + data["crash_time"].str.strip(),
        errors="coerce",
    )

    # Keep only rows with mappable coordinates and a valid timestamp.
    data = data.dropna(subset=["latitude", "longitude", "date/time"])

    # Numeric safety for filters and metrics.
    numeric_cols = ["number_of_cyclist_injured", "number_of_cyclist_killed"]
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Convenience columns for filtering and display.
    data["hour"] = data["date/time"].dt.hour
    data["year"] = data["date/time"].dt.year
    return data


def borough_filter(data: pd.DataFrame) -> pd.DataFrame:
    boroughs = sorted(data["borough"].dropna().unique())
    selected = st.multiselect("Filter by borough", boroughs, default=boroughs)
    if selected:
        data = data[data["borough"].isin(selected)]
    return data


def cyclists_filter(data: pd.DataFrame) -> pd.DataFrame:
    injuries_max = int(data["number_of_cyclist_injured"].max()) if not data.empty else 0
    threshold = st.slider(
        "Minimum cyclists injured",
        min_value=0,
        max_value=injuries_max,
        value=0,
        step=1,
    )
    return data[data["number_of_cyclist_injured"] >= threshold]


def hour_filter(data: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    if data.empty:
        st.info("No rows match the current filters; choose an hour to explore.")
        min_hour, max_hour = 0, 23
    else:
        min_hour, max_hour = int(data["hour"].min()), int(data["hour"].max())
    selected_hour = st.slider("Hour of day", min_hour, max_hour, value=min_hour)
    return data[data["hour"] == selected_hour], selected_hour


def render_map(data: pd.DataFrame, title: str) -> None:
    st.subheader(title)
    if data.empty:
        st.info("No crash records to display on the map.")
        return

    midpoint = (data["latitude"].mean(), data["longitude"].mean())
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position="[longitude, latitude]",
        get_radius=40,
        get_fill_color="[255, 0, 0, 140]",
        pickable=True,
        auto_highlight=True,
    )
    view_state = pdk.ViewState(
        longitude=midpoint[1],
        latitude=midpoint[0],
        zoom=10,
        pitch=40,
    )
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            layers=[layer],
            initial_view_state=view_state,
        )
    )


def render_hourly_histogram(data: pd.DataFrame) -> None:
    st.subheader("Collisions by hour")
    if data.empty:
        st.info("No data available for histogram.")
        return

    counts = data["hour"].value_counts().sort_index()
    st.bar_chart(counts, height=200)


def main() -> None:
    st.title("NYC Bike Crash Dashboard")
    st.caption("Explore collisions involving cyclists across New York City")

    data_load_state = st.empty()
    data_load_state.info("Loading crash data...")
    data = load_data()
    data_load_state.success(f"Loaded {len(data):,} rows")

    st.sidebar.header("Filters")
    filtered = borough_filter(data)
    filtered = cyclists_filter(filtered)
    filtered_by_hour, hour = hour_filter(filtered)

    col1, col2 = st.columns(2)
    with col1:
        render_map(filtered, "All crashes (after filters)")
    with col2:
        render_map(filtered_by_hour, f"Crashes at {hour:02d}:00")

    st.markdown("---")
    col3, col4 = st.columns([2, 1])
    with col3:
        render_hourly_histogram(filtered)
    with col4:
        st.subheader("Key metrics")
        st.metric("Cyclists injured", int(filtered["number_of_cyclist_injured"].sum()))
        st.metric("Cyclists killed", int(filtered["number_of_cyclist_killed"].sum()))
        st.metric("Total crashes", len(filtered))

    if st.checkbox("Show raw data"):
        st.dataframe(filtered.sort_values("date/time", ascending=False))


if __name__ == "__main__":
    main()
