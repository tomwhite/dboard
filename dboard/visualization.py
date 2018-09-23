import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from functools import partial
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from dboard.files import *
from dboard.stats import *
from dboard.timeseries import *

# based on https://stackoverflow.com/a/30125761
def threshold_plot(ax, x, y, threshv, color, overcolor):
    """
    Helper function to plot points above a threshold in a different color

    Parameters
    ----------
    ax : Axes
        Axes to plot to
    x, y : array
        The x and y values

    threshv : float
        Plot using overcolor above this value

    color : color
        The color to use for the lower values

    overcolor: color
        The color to use for values over threshv

    """
    x, y = np.asarray(x), np.asarray(y)

    # Create a colormap for red, green and blue and a norm to color
    # f' < -0.5 red, f' > 0.5 blue, and the rest green
    cmap = ListedColormap([color, overcolor])
    norm = BoundaryNorm([np.min(y), threshv, np.max(y)], cmap.N)

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be numlines x points per line x 2 (x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(y)

    ax.add_collection(lc)
    lc.set_linewidth(0.9)
    return lc


def daily_plot(points, bg_range, day, out_dir):
    """Produce a daily BG plot"""
    x, y = points

    fig, ax = plt.subplots(1, 1, figsize=(2, 1.7), dpi=100)

    # Create a threshold plot where anything below lower BG range is red, and the rest is black
    threshold_plot(ax, x, y, bg_range[0], "r", "k")

    # Add an 'in-range' rectangle (with default blue colour)
    r = matplotlib.patches.Rectangle(
        (0, bg_range[0]), 60 * 24, bg_range[1] - bg_range[0]
    )
    r.set_alpha(0.6)
    ax.add_artist(r)

    # Don't show right, top, or bottom axes
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # Set x and y limits
    ax.set_xlim(0, 60 * 24)
    ax.set_ylim(0, 21)

    # Set ticks and labels
    ax.set_xticks([0, 12 * 60])
    ax.set_xticklabels(["00:00", "12:00"])
    # don't show a tick line, since we have dotted lines
    ax.tick_params(axis="x", width=0, labelsize=7)
    ax.set_yticks([3, 9, 15, 21])
    ax.tick_params(axis="y", labelsize=7)

    # Draw vertical dotted lines at 6 hour intervals
    for i in range(1, 5):
        ax.axvline(i * 6 * 60, color="k", ls=":", alpha=0.5, linewidth=0.8)

    day_str = str(day).split(" ")[0]  # TODO: use proper date formatting
    day_dir = day_str.replace("-", "/")
    filename = "{}/{}/plot.png".format(out_dir, day_dir)
    with open_file(filename, "wb") as figfile:
        # pad_inches will remove padding around the image
        plt.savefig(figfile, format="png", bbox_inches="tight", pad_inches=0)
        plt.close()
    return '<img src="{}/plot.png"/>'.format(day_dir)


def create_json_index(csv_file, out_dir, bg_range):
    index_json = open_file("{}/index.json".format(out_dir), "w")

    entries_df = read_entries_df(csv_file)
    entries_ts = get_traces_ts(entries_df)
    days = get_day_range(entries_ts, weeks_back=10)

    days_to_points = {
        day: list(get_interpolated_points(entries_ts, day)) for day in days
    }

    weekly_tir = get_weekly_series(
        days, days_to_points, partial(time_in_range, bg_range=bg_range)
    )
    weekly_avg = get_weekly_series(days, days_to_points, mean)
    weekly_est_hba1c = get_weekly_series(days, days_to_points, estimated_hba1c)

    weekly_days = get_days_in_week(days)

    all_data = []
    for day, values in weekly_days.iteritems():
        all_data.append(
            {
                "week_start": day.strftime("%d/%m/%Y"),
                "plots": [day.strftime("%Y/%m/%d/plot.png") for day in values],
                "range_low": bg_range[0],
                "range_high": bg_range[1],
                "tir": "%.1f%%" % weekly_tir[day],
                "average_bg": "%.1f" % weekly_avg[day],
                "est_hba1c": "%.1f" % weekly_est_hba1c[day],
            }
        )

    print(json.dumps(all_data, indent=4), file=index_json)

    for day in days:
        daily_plot(days_to_points[day], bg_range, day, out_dir)
