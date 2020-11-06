
using PyCall, BenchmarkTools

py"""
import numpy as np
import matplotlib.pyplot as plt
import omfit_eqdsk, omfit_gapy
import sys

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
namelist['Phi0'] = 1e24

# Now get aurora setup
asim = aurora.core.aurora_sim(namelist, geqdsk=geqdsk)

# set time-independent transport coefficients (flat D=1 m^2/s, V=-2 cm/s)
D_z = 1e4 * np.ones(len(asim.rvol_grid))  # cm^2/s
V_z = -2e2 * np.ones(len(asim.rvol_grid)) # cm/s

# run Aurora forward model
out = asim.run_aurora(D_z, V_z)

# extract densities of each charge state:
nz = out[0]

# Check particle conservation
_ = asim.check_conservation()

# plot charge state distributions over radius and time
aurora.plot_tools.slider_plot(asim.rvol_grid, asim.time_out, nz.transpose(1,0,2),
                              xlabel=r'$r_V$ [cm]', ylabel='time [s]', zlabel='nz [A.U.]',
                              labels=[str(i) for i in np.arange(0,nz.shape[1])],
                              plot_sum=True, x_line=asim.rvol_lcfs)

# add radiation
asim.rad = aurora.radiation.compute_rad(imp, nz.transpose(2,1,0), asim.ne, asim.Te,
                                        prad_flag=True, thermal_cx_rad_flag=False, 
                                        spectral_brem_flag=False, sxr_flag=False, 
                                        main_ion_brem_flag=False)

# plot radiation profiles over radius and time
aurora.plot_tools.slider_plot(asim.rvol_grid, asim.time_out, asim.rad['line_rad'].transpose(1,2,0),
                              xlabel=r'$r_V$ [cm]', ylabel='time [s]', zlabel='Total radiation [A.U.]',
                              labels=[str(i) for i in np.arange(0,nz.shape[1])],
                              plot_sum=True, x_line=asim.rvol_lcfs)


# plot Delta-Zeff profiles over radius and time
asim.calc_Zeff()

# plot variation of Zeff due to simulated impurity:
aurora.plot_tools.slider_plot(asim.rvol_grid, asim.time_out, asim.delta_Zeff.transpose(1,0,2),
                              xlabel=r'$r_V$ [cm]', ylabel='time [s]', zlabel=r'$\Delta$ $Z_{eff}$',
                              labels=[str(i) for i in np.arange(0,nz.shape[1])],
                              plot_sum=True,x_line=asim.rvol_lcfs)
"""



