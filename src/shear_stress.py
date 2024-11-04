"""
This script computes and plots the shear modulus, critical slip distance, and friction drop for a given displacement range.

"""

### Importing libraries
# requires pandas, numpy, matplotlib, scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.stats import linregress

### Define variables
# bounds for analysis
min_disp        = 0 # mm
max_disp        = 100 # mm

# sample metadata
sample_name     = 'x spheres'
sample_length   = 300 # mm
sample_width    = 100 # mm
sample_area     = sample_length * sample_width # mm^2, multiply by 10^-6 to get m^2

# file paths
kn_csv_path     = 'path/to/kn.csv'
mm_csv_path     = 'path/to/mm.csv'
save_dir        = 'save/to/dir/' # directory, filename is set by the script

# peak finding parameters
prominence      = 0.003 # prominence of peaks (units of friction, in this case)
distance        = 100 # minimum distance between peaks in data points (in this case, 100 data points)

### Defining functions
def csv_to_dataframe(kn_csv, mm_csv):
    """
    Combines the force and mm csv files into a single dataframe for easier processing.
    """
    
    # read in the csv files
    force_df    = pd.read_csv(kn_csv, 
                                header=1, 
                                names=['x_force', 'y_force'], # only read in the force columns
                                usecols=[1,2])

    combined_df = pd.read_csv(mm_csv, 
                                header=1, 
                                names=['time', 'x_disp', 'y_disp', 'y_motor_disp', 'x_motor_disp'], 
                                usecols=[0,1,2,3,4])

    # add x_force and y_force to the main dataframe
    combined_df['x_force'] = force_df['x_force']
    combined_df['y_force'] = force_df['y_force']

    # add friction to the main dataframe
    combined_df['friction'] = -combined_df['x_force'] / combined_df['y_force']

    # zero the motor displacement
    combined_df['x_motor_disp'] = combined_df['x_motor_disp'] - combined_df['x_motor_disp'].iloc[0]

    # add x_speed to the main dataframe
    # this is the speed measured by the motor, not the transducer
    combined_df['x_speed'] = np.gradient(combined_df['x_motor_disp'], combined_df['time']) # mm/s
    combined_df['x_speed'] = combined_df['x_speed'].rolling(200).median() # smooth the data

    return combined_df

def make_patch_spines_invisible(ax):
    """
    Function to make the spines of a twinx axis invisible. APPLICABLE TO MATPLOTLIB ONLY. 
    MATLAB users need not apply.
    """
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

### Load data
# load the data
dataframe_full = csv_to_dataframe(kn_csv=kn_csv_path, mm_csv=mm_csv_path)

# filter the data to only include the desired displacement range 
dataframe = dataframe_full[(dataframe_full['x_motor_disp'] > min_disp) & (dataframe_full['x_motor_disp'] < max_disp)]
mean_load = round(dataframe['y_force'].mean(), 1) # mean load during this displacement range in kN, for plotting later

### Find peaks and troughs
# find the peaks in the friction data
peaks, _ = find_peaks(dataframe['friction'], # saved to array called "peaks"
                      prominence=prominence, 
                      distance=distance)

# find the troughs in the friction data
troughs, _ = find_peaks(-dataframe['friction'],  # find troughs by inverting the friction data
                        prominence=prominence,   # saved to array called "troughs"
                        distance=distance)

### Clean up the peaks and troughs
# if the first peak has a smaller index than the first trough, remove it
# we want the dataset to start with a trough and end with a peak
if peaks[0] < troughs[0]:
        peaks = peaks[1:]

# if the last trough has a larger index than the last peak, remove it
if troughs[-1] > peaks[-1]:
        troughs = troughs[:-1]

# use this to debug the peak and trough picking
# these should be the same length
print(f'Picked {len(troughs)} troughs, {len(peaks)} peaks')

### Calculate the shear modulus, critical slip distance, and friction drop
# initialize lists to store the slopes (shear modulus), slip distances, and friction drops
slope_list      = []
slip_list       = []
friction_drops  = []

# FOR DEBUGGING
intercepts = []
i = 0

## Calculate the shear modulus
# iterature through each peak and trough pair (trough and the peak after it)
for peak, trough in zip(peaks, troughs):
        
        # get the data between the peak and trough (peaks and troughs are indexes, so we need to use iloc)
        cut_data = dataframe.iloc[trough:peak]

        ## Calculate the shear stress and strain at each point in the cut data
        # shear stress is the x_force divided by the sample area
        shear_stress = (-cut_data['x_force'] * 1000) / (sample_area * 10**(-6)) # x_force in N divided by area in m^2, Pa

        # calculate the slip deficit and shear strain
        # shear strain is based on the transducer displacement, assuming the sample doesn't move during loading
        sample_deformation = cut_data['x_disp'] - cut_data['x_disp'].iloc[0] # difference between the first x_disp and each x_disp
        shear_strain = sample_deformation / sample_length # deficit in mm divided by sample length in mm

        ## Curve fitting and storing the results
        # fit a line through the loading path, now expressed in shear stress and strain
        slope, intercept, r_value, p_value, std_err = linregress(shear_strain, shear_stress)
        
        # add the slope of this trough/peak pair to the list
        slope_list.append(slope)

        #add the intercept to the list
        intercepts.append(intercept)

        i += 1

## Calculate the slip distance and friction drop
# iterating through each peak
for i in range(len(peaks)): 
        if i == 0: # skip the first peak
                continue
        
        # find the difference in x_disp (transducer) between each stress peak and subsequent trough
        # as well as the difference in friction between each peak and subsequent trough
        # these give the slip distance and the friction drop over each event
        slip_list.append(dataframe['x_disp'].iloc[troughs[i]] - dataframe['x_disp'].iloc[peaks[i-1]])
        friction_drops.append(dataframe['friction'].iloc[peaks[i-1]] - dataframe['friction'].iloc[troughs[i]])

## Calculate and print mean values
# calculate the mean values of the shear modulus, critical slip distance, and friction drop
G           = round(np.mean(slope_list) * 10**(-6), 0) # Convert from Pa to MPa
G_error     = round(np.std(slope_list) * 10**(-6), 0)
d_c         = round(np.mean(slip_list) * 1000, 2) # Convert from m to um
d_c_error   = round(np.std(slip_list) * 1000, 1)
d_mu        = round(np.mean(friction_drops), 3)
d_mu_error  = round(np.std(friction_drops), 3)

# print the mean parameters with one standard deviation
print(f'Mean G: {G} +/- {G_error} MPa')
print(f'Mean d_c: {d_c} +/- {d_c_error} um')
print(f'Mean d_mu: {d_mu} +/- {d_mu_error}')

### Plot the data
# initialize the plot
fig, ax1 = plt.subplots(figsize=(10, 6)) # friction
ax2 = ax1.twinx() # G points
ax3 = ax1.twinx() # x_speed
ax4 = ax1.twinx() # friction drop

# plot data
ax1.plot(dataframe['x_motor_disp'], # friction
         dataframe['friction'], 
         'r-', 
         linewidth=0.2)

ax2.plot(dataframe['x_motor_disp'].iloc[peaks], # Shear moduli
         np.array(slope_list)*(10**(-6)),       # plotted at the peak which ends the loading path
         'o-', 
         color='k', 
         markersize=3)

ax3.plot(dataframe['x_motor_disp'], # x_speed
         dataframe['x_speed'], 
         'g-')

ax4.plot(dataframe['x_motor_disp'].iloc[troughs[1:]], # friction drop
         friction_drops,                              # plotted at the trough which ends the slip
         'o-', 
         color='b', 
         markersize=3)

# axis controls
ax3.spines['left'].set_position(("axes", -0.13))
make_patch_spines_invisible(ax3)
ax3.spines["left"].set_visible(True)
ax3.yaxis.set_label_position('left')
ax3.yaxis.set_ticks_position('left')

ax4.spines['right'].set_position(("axes", 1.13))
make_patch_spines_invisible(ax4)
ax4.spines["right"].set_visible(True)
ax4.yaxis.set_label_position('right')
ax4.yaxis.set_ticks_position('right')

ax1.set_xlabel('Displacement (mm)')
ax1.set_ylabel('Friction Coefficient', color='r')
ax2.set_ylabel('Shear Modulus (MPa)', color='k')
ax3.set_ylabel('Velocity (mm/s)', color='g')
ax4.set_ylabel('Friction Drop', color='b')

# set title with sample metadata and mean values of G, d_c, and d_mu
plt.title(fr"{sample_name}, {mean_load} kN, {min_disp} - {max_disp} mm, G = {G} $\pm$ {G_error} MPa, $\delta_c$ = {d_c} $\pm$ {d_c_error} $\mu$m, $\delta \mu$ = {d_mu} $\pm$ {d_mu_error}")

plt.savefig(f'{save_dir}/{sample_name}spheres_{mean_load}kN.png', dpi=400, bbox_inches='tight')
