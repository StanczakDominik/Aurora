'''
Script to test functionality from namelist creation to run and postprocessing.

It is recommended to run this in IPython.
'''

import numpy as np
import matplotlib.pyplot as plt
plt.ion()
import omfit_eqdsk, omfit_gapy
import sys
from scipy.interpolate import interp1d

# Make sure that package home is added to sys.path
import sys
sys.path.append('../')
import aurora

# read in default Aurora namelist
namelist = aurora.default_nml.load_default_namelist()

# Use gfile and statefile in local directory:
geqdsk = omfit_eqdsk.OMFITgeqdsk('example.gfile')
inputgacode = omfit_gapy.OMFITgacode('example.input.gacode')

# save kinetic profiles on a rhop (sqrt of norm. pol. flux) grid
kp = namelist['kin_profs']
kp['Te']['rhop'] = kp['ne']['rhop'] = np.sqrt(inputgacode['polflux']/inputgacode['polflux'][-1])
kp['ne']['vals'] = inputgacode['ne']*1e13 # 1e19 m^-3 --> cm^-3
kp['Te']['vals'] = inputgacode['Te']*1e3  # keV --> eV

# set impurity species and sources rate
imp = namelist['imp'] = 'Ar'
namelist['source_type'] = 'const'
namelist['Phi0'] = 2e20  # particles/s

# load impurity source time history from a file on disk:
#namelist['source_type'] = 'file'
#namelist['source_file'] = '/home/sciortino/BITE/1101014030/source_function_1101014030.dat.0'

# Change radial resolution from default:
#namelist['dr_0']=0.2
#namelist['dr_1']=0.02

# Change time resolution from default:
#namelist['timing']['dt_increase'] = np.array([1.001, 1.0, 1.])
#namelist['timing']['dt_start'] = np.array([1e-5, 5e-5, 0.001])
#namelist['timing']['steps_per_cycle'] = np.array([1,1,1])
#namelist['timing']['times'] = np.array([0.,0.05,0.2])

# Now get aurora setup
asim = aurora.core.aurora_sim(namelist, geqdsk=geqdsk)

# check radial grid:
_ = aurora.create_radial_grid(namelist,plot=True)

# check time grid:
_ = aurora.create_time_grid(namelist['timing'], plot=True)

# set time-independent transport coefficients (flat D=1 m^2/s, V=-2 cm/s)
D_z = 1e4 * np.ones(len(asim.rvol_grid))  # cm^2/s
V_z = -2e2 * np.ones(len(asim.rvol_grid)) # cm/s

# run Aurora forward model and plot results
out = asim.run_aurora(D_z, V_z, plot=True)

# extract densities and particle numbers in each simulation reservoir
nz, N_wall, N_div, N_pump, N_ret, N_tsu, N_dsu, N_dsul, rcld_rate, rclw_rate = out

# add radiation
asim.rad = aurora.compute_rad(imp, nz.transpose(2,1,0), asim.ne, asim.Te,
                              prad_flag=True, thermal_cx_rad_flag=False, 
                              spectral_brem_flag=False, sxr_flag=False)

# plot radiation profiles over radius and time
aurora.slider_plot(asim.rvol_grid, asim.time_out, asim.rad['line_rad'].transpose(1,2,0),
                              xlabel=r'$r_V$ [cm]', ylabel='time [s]', zlabel=r'Line radiation [$MW/m^3$]',
                              labels=[str(i) for i in np.arange(0,nz.shape[1])],
                              plot_sum=True, x_line=asim.rvol_lcfs)


# plot Delta-Zeff profiles over radius and time
asim.calc_Zeff()

# plot variation of Zeff due to simulated impurity:
aurora.slider_plot(asim.rvol_grid, asim.time_out, asim.delta_Zeff.transpose(1,0,2),
                              xlabel=r'$r_V$ [cm]', ylabel='time [s]', zlabel=r'$\Delta$ $Z_{eff}$',
                              labels=[str(i) for i in np.arange(0,nz.shape[1])],
                              plot_sum=True,x_line=asim.rvol_lcfs)



# plot expected centrifugal asymmetry from finite rotation
rhop_gacode = aurora.rad_coord_transform(inputgacode['rho'],'rhon','rhop', asim.geqdsk)

# omega appears unreliable near axis in input.gacode
omega = interp1d(rhop_gacode[3:], inputgacode['omega0'][3:],
                 bounds_error=False,fill_value='extrapolate')(asim.rhop_grid)

# obtain net Zeff in this discharge (exclude last point, unreliable)
Zeff = interp1d(rhop_gacode[:-1], inputgacode['z_eff'][:-1],
                 bounds_error=False,fill_value='extrapolate')(asim.rhop_grid)

# Obtain estimates for centrifigal asymmetry and plot expected 2D distribution inside LCFS
asim.centrifugal_asym(omega, Zeff, plot=True)
