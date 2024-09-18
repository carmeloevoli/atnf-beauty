import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('gryphon.mplstyle')

import numpy as np

from utils import set_axes, savefig, scale_size
from constants import MYR, KYR

def Pdot_from_B(period, B):
    """Calculate period derivative (Pdot) from period and magnetic field strength."""
    B_critical = 3.2e19  # Critical magnetic field strength in Gauss
    return (B / B_critical)**2 / period

def load_data(filename):
    """Load data from the file and handle errors."""
    try:
        P0, P1, EDOT, XX, YY = np.loadtxt(filename, usecols=(0, 1, 2, 3, 4), unpack=True)
        return P0, P1, EDOT, XX, YY
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return None, None, None, None, None

def plot_distance(filename, output_file='ATNF_msp_distance.pdf'):
    """Plot the distance of pulsars in the XY plane with color coded by age."""
    fig, ax = plt.subplots(figsize=(10.0, 8.5))
    set_axes(ax, xlabel='x [kpc]', ylabel='y [kpc]', xscale='linear', yscale='linear', xlim=[-14, 0], ylim=[-10, 10])

    # Load data from file
    P0, P1, EDOT, XX, YY = load_data(filename)
    if P0 is None:
        return  # Exit if data loading failed

    # Calculate age and log10 of age in Myr
    age = P0 / (2.0 * P1)
    log_age = np.log10(age / MYR)
    print(f"Age (log10) range: {min(log_age)}, {max(log_age)}")

    # Select objects below a maximum period derivative (for B = 1e10)
    pdot_max = Pdot_from_B(P0, 1e10)
    selected = P1 < pdot_max

    # Scale the size of dots based on the logarithmic age
    scaled_sizes = scale_size(log_age, 0., 4)

    # Create scatter plot
    scatter = ax.scatter(XX[selected], YY[selected], s=scaled_sizes[selected], c=log_age[selected], cmap='jet',
                         vmin=0, vmax=4, edgecolors='none', alpha=0.7, marker='o')

    # Add colorbar for the age scale
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label(r'log $\tau$ [Myr]')

    # Plot some guide lines and a circular boundary
    ax.hlines(0, -15, 0, lw=1, ls='--', color='tab:gray')
    ax.vlines(-8, -15, 15, lw=1, ls='--', color='tab:gray')
    x = np.linspace(-13, -3, 1000)
    ax.plot(x, np.sqrt(16.0 - (x + 8.0)**2), lw=1, ls='--', color='tab:gray')
    ax.plot(x, -np.sqrt(16.0 - (x + 8.0)**2), lw=1, ls='--', color='tab:gray')

    # Save the figure
    savefig(fig, output_file)

def plot_nearby(filename, output_file='ATNF_msp_nearby.pdf'):
    """Plot a histogram of pulsar periods for nearby objects with age above a threshold."""
    fig, ax = plt.subplots(figsize=(10.0, 8.5))
    set_axes(ax, xlabel='log $B$ [G]', ylabel=r'$\dot E / d^2$ [erg/s/kpc$^2$]', xscale='linear', yscale='linear', xlim=[7, 14], ylim=[1e33, 1e38])

    # Load data from file
    P0, P1, EDOT, XX, YY = load_data(filename)
    if P0 is None:
        return  # Exit if data loading failed

    # Calculate age and distance
    age = P0 / (2.0 * P1)
    B_critical = 3.2e19  # Critical magnetic field strength in Gauss
    B = B_critical * np.sqrt(P0 * P1)
    distance = np.sqrt((XX + 8.0)**2 + YY**2)
    EDOT_D2 = EDOT / distance**2

    # Apply distance and age thresholds
    D_threshold = 5.0  # kpc
    age_threshold = 50.0 * KYR
    mask = (distance < D_threshold) & (age > age_threshold)

    # Filter data based on thresholds
    P0_filtered = P0[mask]
    P1_filtered = P1[mask]
    B_filtered = B[mask]
    EDOT_D2_filtered = EDOT_D2[mask]

    # Plot histogram of log10(P0)
    ax.hist(np.log10(B_filtered), bins=6, range=[7, 10], weights=EDOT_D2_filtered, log='True', color='tab:orange', alpha=0.6)
    ax.hist(np.log10(B_filtered), bins=8, range=[10, 14], weights=EDOT_D2_filtered, log='True', color='tab:purple', alpha=0.6)

    ax.text(8, 3e37, r'$1.1 \times 10^{37}$', color='tab:orange', fontsize=26)
    ax.text(12, 3e37, r'$2.0 \times 10^{37}$', color='tab:purple', fontsize=26)

    # Calculate Pdot threshold for B = 1e10 and count pulsars
    pdot_max = Pdot_from_B(P0_filtered, 1e10)
    less_than_threshold = P1_filtered < pdot_max
    more_than_threshold = P1_filtered > pdot_max

    msp_count = np.sum(EDOT_D2_filtered[less_than_threshold])
    normal_count = np.sum(EDOT_D2_filtered[more_than_threshold])

    print(f'msp (millisecond pulsars) : {msp_count}')
    print(f'normal pulsars : {normal_count}')

    # Save the figure
    savefig(fig, output_file)

if __name__ == "__main__":
    plot_distance('atnf.txt')
    plot_nearby('atnf.txt')
