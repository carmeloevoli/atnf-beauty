import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple


def savefig(fig: plt.Figure, filename: str, dpi: int = 300, bbox_inches: str = 'tight', pad_inches: float = 0.1, transparent: bool = False) -> None:
    """
    Save the given matplotlib figure to a file with enhanced options for better quality.
    
    Parameters:
    - fig: The matplotlib Figure object to save.
    - filename: The file name or path where the figure will be saved.
    - dpi: The resolution in dots per inch (default is 300 for high-quality).
    - bbox_inches: Adjusts bounding box ('tight' will minimize excess whitespace).
    - pad_inches: Amount of padding around the figure when bbox_inches is 'tight' (default is 0.1).
    - transparent: Whether to save the plot with a transparent background (default is False).
    """
    try:
        fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches, transparent=transparent, format='pdf')
        print(f'Plot successfully saved to {filename} with dpi={dpi}, bbox_inches={bbox_inches}, pad_inches={pad_inches}, transparent={transparent}')
    except Exception as e:
        print(f"Error saving plot to {filename}: {e}")


def _calculate_errors(err_sta_lo: np.ndarray, err_sta_up: np.ndarray, err_sys_lo: np.ndarray, err_sys_up: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate combined statistical and systematic errors.
    
    Parameters:
    - err_sta_lo: Statistical lower error.
    - err_sta_up: Statistical upper error.
    - err_sys_lo: Systematic lower error.
    - err_sys_up: Systematic upper error.
    
    Returns:
    - Combined lower and upper errors.
    """
    err_tot_lo = np.sqrt(err_sta_lo**2 + err_sys_lo**2)
    err_tot_up = np.sqrt(err_sta_up**2 + err_sys_up**2)
    return err_tot_lo, err_tot_up


def _normalize_data(x: np.ndarray, y: np.ndarray, err_tot_lo: np.ndarray, err_tot_up: np.ndarray, slope: float, norm: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Normalize data values by given slope and normalization factor.
    
    Parameters:
    - x: Data points on x-axis.
    - y: Data points on y-axis.
    - err_tot_lo: Combined lower error.
    - err_tot_up: Combined upper error.
    - slope: Slope value for scaling.
    - norm: Normalization factor.
    
    Returns:
    - Normalized x, y, and error values.
    """
    x_norm = x / norm
    scaling = norm * np.power(x_norm, slope)
    y_norm = scaling * y
    y_err_lo_norm = scaling * err_tot_lo
    y_err_up_norm = scaling * err_tot_up
    return x_norm, y_norm, y_err_lo_norm, y_err_up_norm


def plot_data(ax: plt.Axes, filename: str, slope: float, norm: float, fmt: str, color: str, label: str, zorder: int = 1) -> None:
    """
    Load data from file, normalize, and plot with error bars.
    
    Parameters:
    - ax: Matplotlib Axes object to plot on.
    - filename: The path to the data file.
    - slope: The power to which the data should be scaled.
    - norm: Normalization factor for the data.
    - fmt: Format string for the plot markers.
    - color: Color of the plot markers and lines.
    - label: Label for the plot legend.
    - zorder: Z-order for layering the plot.
    """
    try:
        x, y, err_sta_lo, err_sta_up, err_sys_lo, err_sys_up = np.loadtxt(f'../data/{filename}', usecols=(0, 1, 2, 3, 4, 5), unpack=True)
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return
    
    # Calculate combined errors
    err_tot_lo, err_tot_up = _calculate_errors(err_sta_lo, err_sta_up, err_sys_lo, err_sys_up)
    
    # Normalize data
    x_norm, y_norm, y_err_lo_norm, y_err_up_norm = _normalize_data(x, y, err_tot_lo, err_tot_up, slope, norm)
    
    # Plot the data with error bars
    ax.errorbar(x_norm, y_norm, yerr=[y_err_lo_norm, y_err_up_norm], fmt=fmt, markeredgecolor=color, color=color,
                label=label, capsize=4.5, markersize=7, elinewidth=2.2, capthick=2.2, zorder=zorder)


def set_axes(ax: plt.Axes, xlabel: str, ylabel: str, xscale: str = 'log', yscale: str = 'log', xlim: Optional[Tuple[float, float]] = None, ylim: Optional[Tuple[float, float]] = None) -> None:
    """
    Set the properties for the axes of a plot.
    
    Parameters:
    - ax: Matplotlib Axes object.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    - xscale: Scale of the x-axis ('linear' or 'log').
    - yscale: Scale of the y-axis ('linear' or 'log').
    - xlim: Limits for the x-axis (tuple of min, max).
    - ylim: Limits for the y-axis (tuple of min, max).
    """
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # Validate and set x-axis scale
    if xscale in ['linear', 'log']:
        ax.set_xscale(xscale)
    else:
        print(f"Invalid xscale '{xscale}', defaulting to 'log'.")
        ax.set_xscale('log')

    # Validate and set y-axis scale
    if yscale in ['linear', 'log']:
        ax.set_yscale(yscale)
    else:
        print(f"Invalid yscale '{yscale}', defaulting to 'log'.")
        ax.set_yscale('log')
        
    # Set axis limits if provided
    if xlim:
        ax.set_xlim(xlim)
    else:
        print(f"No xlim provided, using default xlim.")
        
    if ylim:
        ax.set_ylim(ylim)
    else:
        print(f"No ylim provided, using default ylim.")


def scale_size(value: float, value_min: float, value_max: float, smin: float = 10., smax: float = 120.) -> float:
    """
    Scale a value to a size between a specified minimum and maximum.
    
    Parameters:
    - value: The value to scale.
    - value_min: The minimum value in the dataset.
    - value_max: The maximum value in the dataset.
    - smin: Minimum size (default is 10).
    - smax: Maximum size (default is 120).
    
    Returns:
    - Scaled size.
    """
    if value_max == value_min:
        raise ValueError("value_max and value_min cannot be the same.")
    return (value - value_min) / (value_max - value_min) * (smax - smin) + smin
