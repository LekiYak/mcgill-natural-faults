import numpy as np
import matplotlib.pyplot as plt

# define constants
A    = 0.3 * 0.1 # area in m^2
G    = 1.74*10**(8) # Shear modulus in Pa
G_sd = 45*10**(6) # Shear modulus error in Pa
d_c  = 5*10**(-6) # critical slip distance in m
u    = 0.05 # stress drop magnitude in friction coefficient
y_force = 10*1000 # load in N
L_c  = 0.058 # critical nucleation length in m
C    = 1 # shape constant

# define the length scale as a function of the normal load
def length_scale(load, G):
    # print(f'Normal stress: {load / A / 10**6} Pa')
    L = (C * G * d_c) / ((load / A) * u) * 100
    return L

print(length_scale(y_force, G))

# define the normal load range
load_range = np.linspace(1000, 100*1000, 1000)

# plot the length scale as a function of the normal load (xlog)
fig, ax = plt.subplots()

ax.plot(load_range, length_scale(load_range, G), color='blue', label='C = 1')
ax.plot(load_range, (4/(3 * np.pi)) * length_scale(load_range, G), color='red', label='C = 4/3π')

# confidence interval
ax.fill_between(load_range, length_scale(load_range, G) - length_scale(load_range, G_sd), length_scale(load_range, G) + length_scale(load_range, G_sd), color='blue', alpha=0.2)

# confidence interval
ax.fill_between(load_range, (4/(3 * np.pi)) * length_scale(load_range, G) - length_scale(load_range, G_sd), (4/(3 * np.pi)) * length_scale(load_range, G) + length_scale(load_range, G_sd), color='red', alpha=0.2)

# sample spacings
spacings = [13, 23.2, 11.6, 7.7, 5.8, 4.6, 3.4, 2.2]
spacing_labels = [3, 4, 6, 8, 10, 12, 16, 24]
for i, spacing in enumerate(spacings):
    ax.axhline(y=spacing, color='black', linestyle='--', alpha=0.5)
    ax.text(35100, spacing, f'{spacing_labels[i]}', color='black', verticalalignment='center')

# dimple strength
max_load = 1250 * np.array(spacing_labels)
ax.plot(max_load, np.array(spacings), 'o', color='black', label='Dimple strength')

ax.set_ylabel('Length scale (cm)')
ax.set_xlabel('Normal load (kN)')
ax.set_xticks(np.arange(0, 35000, 2500))
ax.set_xticklabels(np.arange(0, 35, 2.5))
ax.set_xlim(0, 35000)
ax.set_yticks(np.arange(0, 25, 1))
ax.set_ylim(0, 25)
plt.grid()
plt.legend()
plt.title('G = 174 MPa (sd = 45 MPa), d_c = 5 µm, Δu = 0.05')
plt.show()


