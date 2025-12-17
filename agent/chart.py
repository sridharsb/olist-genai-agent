import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot(df, x_col, y_col):
    """
    Intelligent plotting:
    - Horizontal bars for categorical data
    - Vertical line chart for time series
    - Auto-resizes based on data
    - Prevents label collision
    """

    # Number of rows
    n = len(df)

    # Auto figure size
    height = max(4, n * 0.4)
    fig, ax = plt.subplots(figsize=(10, height))

    # Detect time series
    is_time_series = "month" in x_col.lower() or "year" in x_col.lower()

    # ----------------------------
    # Time series → line chart
    # ----------------------------
    if is_time_series:
        ax.plot(df[x_col], df[y_col], marker="o")
        ax.set_xlabel(x_col.replace("_", " ").title())
        ax.set_ylabel(y_col.replace("_", " ").title())

        # Rotate labels if many points
        if n > 6:
            plt.xticks(rotation=45, ha="right")

    # ----------------------------
    # Categorical → horizontal bar
    # ----------------------------
    else:
        ax.barh(df[x_col], df[y_col])
        ax.set_ylabel(x_col.replace("_", " ").title())
        ax.set_xlabel(y_col.replace("_", " ").title())
        ax.invert_yaxis()  # highest at top

    # ----------------------------
    # Number formatting
    # ----------------------------
    if "revenue" in y_col.lower():
        ax.xaxis.set_major_formatter(
            mtick.FuncFormatter(lambda x, _: f"{int(x):,}")
        )
    elif "units" in y_col.lower():
        ax.xaxis.set_major_formatter(
            mtick.FuncFormatter(lambda x, _: f"{int(x):,}")
        )

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    return fig
