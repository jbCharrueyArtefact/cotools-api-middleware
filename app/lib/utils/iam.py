from app.models.iam import HistoricalIamDetails
from datetime import datetime


def get_interval_historical_data(interval: HistoricalIamDetails):
    max_date = (
        interval.end_date.strftime("%Y-%m-%d") if interval.end_date else None
    )
    min_date = (
        interval.start_date.strftime("%Y-%m-%d")
        if interval.start_date
        else None
    )
    time_filters = []
    if max_date:
        time_filters.append(f"timestamp < '{max_date}'")
    if min_date:
        time_filters.append(f"timestamp > '{min_date}'")
    return " AND ".join(time_filters) if time_filters else None
