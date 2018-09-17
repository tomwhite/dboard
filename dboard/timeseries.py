import datetime
import numpy as np
import pandas as pd
import traces


def read_entries_df(csv_file):
    """
    Read entries from CSV exported from Nightscout
    :param csv_file: a CSV file with columns dateString, type, sgv and/or mgb
    :return: a Pandas dataframe with columns ts, type, bg
    """
    entries_df = pd.read_csv(csv_file, parse_dates=["dateString"])
    # create a new 'bg' column that uses either 'sgv' or 'mbg' column, and turns into mmol/l
    entries_df["bg"] = (
        np.where(pd.notna(entries_df["sgv"]), entries_df["sgv"], entries_df["mbg"])
        / 18.0
    )
    # rename, reorder, drop columns
    entries_df = entries_df.rename(columns={"dateString": "ts"})
    entries_df = entries_df[["ts", "type", "bg"]]
    # sort by timestamp, since data from device may not be in chronological order
    entries_df = entries_df.sort_values(by=["ts"])
    return entries_df


def get_traces_ts(entries_df):
    # use the traces library to generate a time series for interpolation
    return traces.TimeSeries([tuple(x) for x in entries_df[["ts", "bg"]].values])


def get_day_range(entries_ts, weeks_back=3):
    # first and last days in data, normalized to midnight
    first_day = entries_ts.first_key().normalize()
    last_day = entries_ts.last_key().normalize()

    # start and end days we want to show
    # go back at least this many weeks
    start_day = last_day - pd.Timedelta(weeks=weeks_back)
    # go back to Monday before
    start_day = start_day - pd.Timedelta(days=start_day.weekday())
    # make sure start day is not before first day in data
    start_day = max(first_day, start_day)
    end_day = last_day
    return pd.date_range(start=start_day, end=end_day).tolist()


def get_interpolated_points(entries_ts, day):
    if entries_ts.last_key().date() == day.date():  # stop at last entry of last day
        day_end = entries_ts.last_key()
    else:
        day_end = day + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    # interpolate bg to every minute
    entries_ts_interpolated = traces.TimeSeries(
        entries_ts.sample(
            sampling_period=datetime.timedelta(minutes=1),
            start=day,
            end=day_end,
            interpolate="linear",
        )
    )
    points = [(k.hour * 60 + k.minute, v) for (k, v) in entries_ts_interpolated.items()]
    return zip(*points)


def get_daily_series(days, days_to_points, fn):
    return pd.Series(
        [fn(days_to_points[day]) for day in days], index=pd.DatetimeIndex(days)
    )


def get_weekly_series(days, days_to_points, fn):
    return get_daily_series(days, days_to_points, fn).resample("7D").mean()


def get_days_in_week(days):
    return pd.Series(days, index=pd.DatetimeIndex(days))\
        .resample("7D")\
        .aggregate(lambda x: tuple(x))

