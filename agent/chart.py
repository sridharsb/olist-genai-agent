"""
Enhanced chart visualization with colorful, modern styling.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from typing import Optional

# Set modern style
plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

# Color palette
COLORS = {
    'primary': '#6366f1',
    'secondary': '#8b5cf6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
}


def get_gradient_colors(n: int) -> list:
    """Generate gradient colors for bars."""
    if n <= len(COLORS['gradient']):
        return COLORS['gradient'][:n]
    
    # Generate more colors using interpolation
    colors = []
    base_colors = COLORS['gradient']
    for i in range(n):
        idx = (i * (len(base_colors) - 1)) / (n - 1) if n > 1 else 0
        low_idx = int(idx)
        high_idx = min(low_idx + 1, len(base_colors) - 1)
        t = idx - low_idx
        
        # Simple color interpolation (RGB)
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        
        def rgb_to_hex(rgb):
            return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"
        
        c1 = hex_to_rgb(base_colors[low_idx])
        c2 = hex_to_rgb(base_colors[high_idx])
        interpolated = tuple(c1[j] + t * (c2[j] - c1[j]) for j in range(3))
        colors.append(rgb_to_hex(interpolated))
    
    return colors


def plot(df, x_col: str, y_col: str, figsize: Optional[tuple] = None) -> plt.Figure:
    """
    Enhanced intelligent plotting with colorful styling:
    - Horizontal bars for categorical data with gradients
    - Vertical line chart for time series with smooth curves
    - Auto-resizes based on data
    - Modern, colorful design
    """
    # Number of rows
    n = len(df)
    
    # Auto figure size
    if figsize is None:
        height = max(5, min(n * 0.5, 12))
        figsize = (12, height)
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    
    # Detect time series
    is_time_series = any(keyword in x_col.lower() for keyword in ["month", "year", "date", "time"])
    
    # ----------------------------
    # Time series → line chart
    # ----------------------------
    if is_time_series:
        # Sort by x_col for proper line plotting
        df_sorted = df.sort_values(x_col)
        
        ax.plot(
            df_sorted[x_col],
            df_sorted[y_col],
            marker="o",
            markersize=8,
            linewidth=3,
            color=COLORS['primary'],
            markerfacecolor=COLORS['secondary'],
            markeredgecolor='white',
            markeredgewidth=2,
            label=y_col.replace("_", " ").title()
        )
        
        # Fill under curve with gradient
        ax.fill_between(
            df_sorted[x_col],
            df_sorted[y_col],
            alpha=0.3,
            color=COLORS['primary']
        )
        
        ax.set_xlabel(x_col.replace("_", " ").title(), fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col.replace("_", " ").title(), fontsize=12, fontweight='bold')
        ax.set_title(f"{y_col.replace('_', ' ').title()} Over Time", fontsize=14, fontweight='bold', pad=20)
        
        # Rotate labels if many points
        if n > 6:
            plt.xticks(rotation=45, ha="right")
        
        ax.legend(loc='best', framealpha=0.9)
    
    # ----------------------------
    # Categorical → horizontal bar
    # ----------------------------
    else:
        # Sort by y_col for better visualization
        df_sorted = df.sort_values(y_col, ascending=True)
        
        # Get gradient colors
        colors = get_gradient_colors(n)
        
        bars = ax.barh(
            df_sorted[x_col],
            df_sorted[y_col],
            color=colors,
            edgecolor='white',
            linewidth=2,
            height=0.7
        )
        
        # Add value labels on bars
        for i, (idx, row) in enumerate(df_sorted.iterrows()):
            value = row[y_col]
            label_x = value + (max(df_sorted[y_col]) * 0.01)  # Small offset
            ax.text(
                label_x,
                i,
                f"{value:,.0f}" if isinstance(value, (int, float)) else str(value),
                va='center',
                fontsize=10,
                fontweight='bold',
                color='#1f2937'
            )
        
        ax.set_xlabel(y_col.replace("_", " ").title(), fontsize=12, fontweight='bold')
        ax.set_ylabel(x_col.replace("_", " ").title(), fontsize=12, fontweight='bold')
        ax.set_title(f"{y_col.replace('_', ' ').title()} by {x_col.replace('_', ' ').title()}", 
                    fontsize=14, fontweight='bold', pad=20)
    
    # ----------------------------
    # Number formatting
    # ----------------------------
    if "revenue" in y_col.lower() or "value" in y_col.lower():
        if is_time_series:
            ax.yaxis.set_major_formatter(
                mtick.FuncFormatter(lambda x, _: f"R$ {x:,.0f}")
            )
        else:
            ax.xaxis.set_major_formatter(
                mtick.FuncFormatter(lambda x, _: f"R$ {x:,.0f}")
            )
    elif "units" in y_col.lower() or "count" in y_col.lower():
        if is_time_series:
            ax.yaxis.set_major_formatter(
                mtick.FuncFormatter(lambda x, _: f"{int(x):,}")
            )
        else:
            ax.xaxis.set_major_formatter(
                mtick.FuncFormatter(lambda x, _: f"{int(x):,}")
            )
    
    # Enhanced grid
    ax.grid(axis="x" if not is_time_series else "y", 
            linestyle="--", 
            alpha=0.3,
            color='#9ca3af',
            linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e5e7eb')
    ax.spines['bottom'].set_color('#e5e7eb')
    
    # Set background color
    ax.set_facecolor('#fafafa')
    
    plt.tight_layout()
    return fig
