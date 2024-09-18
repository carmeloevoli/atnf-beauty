import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('gryphon.mplstyle')

import numpy as np

from utils import set_axes, savefig, scale_size
from constants import GYR

def Pdot_from_age(period, age):
    """Calculate period derivative (Pdot) from period and age."""
    return period / (2.0 * age)

def Pdot_from_B(period, B):
    """Calculate period derivative (Pdot) from period and magnetic field strength."""
    B_critical = 3.2e19  # Critical magnetic field strength in Gauss
    return (B / B_critical)**2 / period

def load_data(filename):
    """Load data from a file and handle potential errors."""
    try:
        P0, P1, EDOT = np.loadtxt(filename, usecols=(0, 1, 2), unpack=True)
        return P0, P1, np.log10(EDOT)
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return None, None, None

def plot_age_lines(ax, period):
    """Plot lines of constant age on the P-Pdot diagram."""
    ages = np.array([1e-8, 1e-6, 1e-4, 1e-2, 1, 1e2, 1e4]) * GYR
    for age in ages:
        Pdot = Pdot_from_age(period, age)
        ax.plot(period, Pdot, '--', color='tab:gray', lw=1, zorder=3)

def plot_bfield_lines(ax, period):
    """Plot lines of constant magnetic field strength on the P-Pdot diagram."""
    bfields = np.array([1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14])
    for B in bfields:
        Pdot = Pdot_from_B(period, B)
        ax.plot(period, Pdot, '--', color='tab:gray', lw=1, zorder=3)

def plot_ppdot(filename, output_file='ATNF_PPDOT.pdf', cmap='jet'):
    """Main function to plot the P-Pdot diagram using data from the ATNF pulsar database."""
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(11.0, 8.5))
    set_axes(ax, xlabel='Period [s]', ylabel='Period derivative', xlim=[1e-3, 40], ylim=[1e-22, 1e-9])

    # Load data from file
    P0, P1, EDOT = load_data(filename)
    if P0 is None or P1 is None or EDOT is None:
        print("Failed to load data. Exiting.")
        return

    # Scale the size of dots based on EDOT values
    scaled_sizes = scale_size(EDOT, 29, 38)

    # Create scatter plot with color based on EDOT
    scatter = ax.scatter(P0, P1, s=scaled_sizes, c=EDOT, cmap=cmap, vmin=29, vmax=38,
                         edgecolors='none', alpha=0.7, marker='o', zorder=5)

    # Add a colorbar to indicate log EDOT values
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label(r'log $\dot E$')

    # Define period range for plotting lines
    period = np.logspace(-3, 2, 1000)

    # Plot lines of constant age
    plot_age_lines(ax, period)

    # Plot lines of constant magnetic field strength
    plot_bfield_lines(ax, period)

    # Fill a region based on a specific magnetic field strength (1e10 Gauss)
    Pdot_critical = Pdot_from_B(period, 1e10)
    ax.fill_between(period, Pdot_critical, 1e-2, alpha=0.2, color='tab:gray', zorder=1)

    # Save the figure as a PDF
    savefig(fig, output_file)

if __name__ == "__main__":
    plot_ppdot('atnf.txt')
