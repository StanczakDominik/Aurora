'''Functions to provide default ADAS files for Aurora modelling, including capabilities to fetch
these files remotely from the OPEN-ADAS website.
'''

import urllib
import shutil,os

# location of the "adas_data" directory relative to this script:
adas_data_dir = os.path.dirname(os.path.realpath(__file__))+'/../adas_data/adf11/'

def get_adas_file_loc(filename):
    '''Find location of requested atomic data file for the indicated ion. 
    The search proceeds with the following attempts, in this order:

    #. If the file is available in Aurora/adas_data/adf11, always use this data.

    #. If the environmental variable "AURORA_ADAS_DIR" is defined, attempt to find the file there and copy it to Aurora/adas_data/adf11.

    #. Attempt to fetch the file remotely via open.adas.ac.uk and save it in Aurora/adas_data/adf11/. 

    Args:
        filename : str
            Name of the ADAS ADF11 file of interest, e.g. 'plt89_ar.dat'
    
    Returns:
        file_loc : str
            Full path to the requested file. 
    '''

    if os.path.exists(adas_data_dir+filename):
        # file is available in adas_data:
        pass
    
    elif 'AURORA_ADAS_DIR' in os.environ:
        if os.path.exists(os.environ['AURORA_ADAS_DIR']+'/'+filename):
            # copy file to adas_data_dir:
            shutil.copyfile(os.environ['AURORA_ADAS_DIR']+'/'+filename, adas_data_dir+filename)
            pass
        else:
            # File could not be found. Download it and save it in adas_data:
            fetch_adf11_file(filename)        
    else:
        # File could not be found. Download it and save it in adas_data:
        fetch_adf11_file(filename)

    return adas_data_dir+filename


def fetch_adf11_file(filename):
    '''Download ADF11 file from the OPEN-ADAS website and store it in the 'adas_data'
    directory. 

    Args:
        filename : str
            Name of ADF11 file to be downloaded, e.g. 'plt89_ar.dat'.
    '''
    url = 'https://open.adas.ac.uk/download/adf11/'
    str1 =  filename.split('_')[0]
    local_filename,headers = urllib.request.urlretrieve(url+str1+'/'+filename, filename)
    os.replace(filename,adas_data_dir+filename)


def adas_files_dict():
    '''Selections for ADAS files for Aurora runs and radiation calculations.
    This function can be called to fetch a set of default files, which can then be modified (e.g. to 
    use a new file for a specific SXR filter) before running a calculation. 

    Returns:
        files : dict
            Dictionary with keys equal to the atomic symbols of many of the most common ions of
            interest in fusion research. For each ion, a sub-dictionary contains recommended file 
            names for the relevant ADAS data types. Not all files types are available for all ions. 
            Files types are usually a subset of 
            'acd','scd','prb','plt','ccd','prc','pls','prs','fis','brs','pbs',prc'
            Refer to :py:func:`~aurora.atomic.get_adas_file_types` for a description of the meaning of 
            each file.
    '''
            
    files={}
    files["H"] = {}   #1
    files["H"]['acd'] = "acd96_h.dat"
    files["H"]['scd'] = "scd96_h.dat"
    files["H"]['prb'] = "prb96_h.dat"
    files["H"]['plt'] = "plt96_h.dat"
    files["H"]['ccd'] = "ccd96_h.dat"
    files["H"]['prc'] = "prc96_h.dat"
    files["H"]['pls'] = "pls_H_14.dat"
    files["H"]['prs'] = "prs_H_14.dat"
    files["H"]['fis'] = "sxrfil14.dat"
    files["H"]['brs'] = "brs05360.dat"
    files["H"]["pbs"] = "pbsx7_h.dat"
    files["H"]["prc"] = "prc89_h.dat"
    files["He"] = {}   #2
    files["He"]['acd'] = "acd96_he.dat"
    files["He"]['scd'] = "scd96_he.dat"
    files["He"]['prb'] = "prb96_he.dat"
    files["He"]['plt'] = "plt96_he.dat"
    files["He"]['ccd'] = "ccd07_he.dat"
    files["He"]['pls'] = "pls_He_14.dat"
    files["He"]['prs'] = "prs_He_14.dat"
    files["He"]['fis'] = "sxrfil14.dat"
    files["He"]['brs'] = "brs05360.dat"
    files["He"]["pbs"] = "pbsx5_he.dat"
    files["He"]['prc'] = "prc96_he.dat"
    files["Li"] = {}   #3
    files["Li"]['acd'] = "acd96_li.dat"
    files["Li"]['scd'] = "scd96_li.dat"
    files["Li"]['ccd'] = "ccd89_li.dat"
    files["Li"]['prb'] = "prb96_li.dat"
    files["Li"]['plt'] = "plt96_li.dat"
    files["Li"]['prc'] = "prc89_li.dat"
    files["Li"]['pls'] = "pls89_li.dat"
    files["Li"]["pbs"] = ''
    files["Li"]["prc"] = "prc89_li.dat"
    files["Be"] = {}   #4
    files["Be"]['acd'] = "acd96_be.dat"
    files["Be"]['scd'] = "scd96_be.dat"
    files["Be"]['prb'] = "prb96_be.dat"
    files["Be"]['plt'] = "plt96_be.dat"
    files["Be"]['ccd'] = "ccd89_be.dat"
    files["Be"]['prc'] = "prc89_be.dat"
    files["Be"]['pls'] = "plsx5_be.dat"
    files["Be"]['prs'] = "prsx5_be.dat"
    files["Be"]["pbs"] = "pbsx5_be.dat"
    files["Be"]["prc"] = "prc89_be.dat"
    files["B"] = {}   #5
    files["B"]['acd'] = "acd89_b.dat"
    files["B"]['scd'] = "scd89_b.dat"
    files["B"]['ccd'] = "ccd89_b.dat"
    files["B"]['prb'] = "prb89_b.dat"
    files["B"]['plt'] = "plt89_b.dat"
    files["B"]['prc'] = "prc89_b.dat"
    files["B"]['pls'] = "plsx5_b.dat"
    files["B"]['prs'] = "prsx5_b.dat"
    files["B"]["pbs"] = "pbsx5_b.dat"
    files["B"]["prc"] = "prc89_b.dat"
    files["C"] = {}    #6
    files["C"]['acd'] = "acd96_c.dat"
    files["C"]['scd'] = "scd96_c.dat"
    files["C"]['prb'] = "prb96_c.dat"
    files["C"]['plt'] = "plt96_c.dat"
    files["C"]['ccd'] = "ccd96_c.dat"
    files["C"]['pls'] = "pls_C_14.dat"
    files["C"]['prs'] = "prs_C_14.dat"
    files["C"]['fis'] = "sxrfil14.dat"
    files["C"]['brs'] = "brs05360.dat"
    files["C"]["pbs"] = "pbsx5_c.dat"
    files["C"]['prc'] = "prc96_c.dat"
    files["N"] = {}    #7
    files["N"]['acd'] = "acd96_n.dat"
    files["N"]['scd'] = "scd96_n.dat"
    files["N"]['ccd'] = "ccd89_n.dat"
    files["N"]['prb'] = "prb96_n.dat"
    files["N"]['plt'] = "plt96_n.dat"
    files["N"]['pls'] = "plsx8_n.dat"
    files["N"]['prs'] = "prsx8_n.dat"
    files["N"]['fis'] = "sxrfilD1.dat"
    files["N"]['brs'] = "brs05360.dat"
    files["N"]['ccd'] = "ccd96_n.dat"
    files["N"]["pbs"] = "pbsx5_n.dat"
    files["N"]["prc"] = "prc89_n.dat"
    files["O"] = {}    #8
    files["O"]['acd'] = "acd96_o.dat"
    files["O"]['scd'] = "scd96_o.dat"
    files["O"]['ccd'] = "ccd89_o.dat"
    files["O"]['prb'] = "prb96_o.dat"
    files["O"]['plt'] = "plt96_o.dat"
    files["O"]['pls'] = "plsx5_o.dat"
    files["O"]['prs'] = "prsx5_o.dat"
    files["O"]["pbs"] = "pbsx5_o.dat"
    files["O"]["prc"] = "prc89_o.dat"
    files["F"] = {}    #9
    files["F"]['acd'] = "acd89_f.dat"
    files["F"]['scd'] = "scd89_f.dat"
    files["F"]['ccd'] = "ccd89_f.dat"
    files["F"]['prb'] = "prb89_f.dat"
    files["F"]['plt'] = "plt89_f.dat"
    files["F"]['fis'] = "sxrfil14.dat"
    files["F"]['brs'] = "brs05360.dat"
    files["F"]['pls'] = "pls_F_14.dat"
    files["F"]['prs'] = "prs_F_14.dat"
    files["F"]["pbs"] = "pbsx5_f.dat"
    files["F"]['prc'] = "prc89_f.dat"
    files["Ne"] = {}   #10
    files["Ne"]['acd'] = "acd96_ne.dat"
    files["Ne"]['scd'] = "scd96_ne.dat"
    files["Ne"]['prb'] = "prb96_ne.dat"
    files["Ne"]['plt'] = "plt96_ne.dat"
    files["Ne"]['ccd'] = "ccd89_ne.dat"
    files["Ne"]['pls'] = "plsx8_ne.dat"
    files["Ne"]['prs'] = "prsx8_ne.dat"
    files["Ne"]['fis'] = "sxrfilD1.dat"
    files["Ne"]['brs'] = "brs05360.dat"
    files["Ne"]["pbs"] = "pbsx5_ne.dat"
    files["Ne"]['prc'] = "prc89_ne.dat"
    files["Al"] = {}    #13
    files["Al"]['acd'] = "acd00_al.dat"
    files["Al"]['scd'] = "scd00_al.dat"
    files["Al"]['prb'] = "prb00_al.dat"
    files["Al"]['plt'] = "plt00_al.dat"
    files["Al"]['ccd'] = "ccd89_al.dat"
    files["Al"]['pls'] = "pls_Al_14.dat"
    files["Al"]['prs'] = "prs_Al_14.dat"
    files["Al"]['fis'] = "sxrfil14.dat"
    files["Al"]['brs'] = "brs05360.dat"
    files["Al"]['pbs'] = "pbsx5_al.dat"
    files["Al"]['prc'] = "prc89_al.dat"
    files["Si"] = {}     #14
    files["Si"]['acd'] = "acd00_si.dat"
    files["Si"]['scd'] = "scd00_si.dat"
    files["Si"]['prb'] = "prb00_si.dat"
    files["Si"]['plt'] = "plt97_si.dat"
    files["Si"]['pls'] = "pls_Si_14.dat"
    files["Si"]['prs'] = "prs_Si_14.dat"
    files["Si"]['fis'] = "sxrfil14.dat"
    files["Si"]['brs'] = "brs05360.dat"
    files["Si"]['ccd'] = "ccd89_si.dat"
    files["Si"]["pbs"] = "pbsx5_si.dat"
    files["Si"]["prc"] = "prc89_si.dat"
    files["Ar"] = {}     #18
    files["Ar"]['acd'] = "acd89_ar.dat"
    files["Ar"]['scd'] = "scd89_ar.dat"
    files["Ar"]['prb'] = "prb89_ar.dat"
    files["Ar"]['plt'] = "plt89_ar.dat"
    files["Ar"]['ccd'] = "ccd89_ar.dat"
    files["Ar"]['prc'] = "prc89_ar.dat"
    files["Ar"]['pls'] = "pls_Ar_14.dat"
    files["Ar"]['prs'] = "prs_Ar_14.dat"
    files["Ar"]['fis'] = "sxrfil14.dat"
    files["Ar"]['brs'] = "brs05360.dat"
    files["Ar"]["pbs"] = "pbsx5_ar.dat"
    files["Ar"]["prc"] = "prc89_ar.dat"
    files["Ca"] = {}     #20
    files["Ca"]['acd'] = "acd85_ca.dat"
    files["Ca"]['scd'] = "scd85_ca.dat"
    files["Ca"]['ccd'] = "ccd89_w.dat"  # file not available, use first 20 ion stages using Foster scaling
    files["Ca"]['prb'] = "prb85_ca.dat"  # not public on OPEN-ADAS, must request 
    files["Ca"]['plt'] = "plt85_ca.dat"    # not public on OPEN-ADAS, must request 
    files["Ca"]['pls'] = "pls_Ca_14.dat"
    files["Ca"]['prs'] = "prs_Ca_14.dat"
    files["Ca"]['fis'] = "sxrfil14.dat"
    files["Ca"]['brs'] = "brs05360.dat"
    files["Ca"]["pbs"] = ""
    files["Ca"]["prc"] = ""
    files["Fe"] = {}     #26
    files["Fe"]['acd'] = "acd89_fe.dat"
    files["Fe"]['scd'] = "scd89_fe.dat"
    files["Fe"]['prb'] = "prb89_fe.dat"
    files["Fe"]['plt'] = "plt89_fe.dat"
    files["Fe"]['pls'] = "pls_Fe_14.dat"
    files["Fe"]['prs'] = "prs_Fe_14.dat"
    files["Fe"]['fis'] = "sxrfil14.dat"
    files["Fe"]['brs'] = "brs05360.dat"
    files["Fe"]['ccd'] = "ccd89_fe.dat"
    files["Fe"]["pbs"] = "pbsx5_fe.dat"
    files["Fe"]["prc"] = "prc89_fe.dat"
    files["Ni"] = {}     #28
    files["Ni"]['acd'] = "acd00_ni.dat"
    files["Ni"]['scd'] = "scd00_ni.dat"
    files["Ni"]['prb'] = "prb00_ni.dat"
    files["Ni"]['plt'] = "plt00_ni.dat"
    files["Ni"]['pls'] = "pls_Ni_14.dat"
    files["Ni"]['prs'] = "prs_Ni_14.dat"
    files["Ni"]['fis'] = "sxrfil14.dat"
    files["Ni"]['brs'] = "brs05360.dat"
    files["Ni"]['ccd'] = "ccd89_ni.dat"
    files["Ni"]["pbs"] = "pbsx5_ni.dat"
    files["Ni"]["prc"] = "prc89_ni.dat"
    files["Kr"] = {}     #36
    files["Kr"]['acd'] = "acd89_kr.dat"
    files["Kr"]['scd'] = "scd89_kr.dat"
    files["Kr"]['ccd'] = "ccd89_kr.dat"
    files["Kr"]['prb'] = "prb89_kr.dat"
    files["Kr"]['plt'] = "plt89_kr.dat"
    files["Kr"]['pls'] = "plsx5_kr.dat"
    files["Kr"]['prs'] = "prsx5_kr.dat"
    files["Kr"]["pbs"] = ""
    files["Kr"]["prc"] = "prc89_kr.dat"
    files["Mo"] = {}     #42
    files["Mo"]['acd'] = "acd89_mo.dat"
    files["Mo"]['scd'] = "scd89_mo.dat"
    files["Mo"]['ccd'] = "ccd89_mo.dat"
    files["Mo"]['plt'] = "plt89_mo.dat"
    files["Mo"]['prb'] = "prb89_mo.dat"
    files["Mo"]["pbs"] = ""
    files["Mo"]['prc'] = "prc89_mo.dat"
    files["Xe"] = {}     #56
    files["Xe"]['acd'] = "acd89_xe.dat"
    files["Xe"]['scd'] = "scd89_xe.dat"
    files["Xe"]['ccd'] = "ccd89_xe.dat"
    files["Xe"]['plt'] = "plt89_xe.dat"
    files["Xe"]['prb'] = "prb89_xe.dat"
    files["Xe"]['prs'] = "prsx1_xe.dat"
    files["Xe"]['pls'] = "prsx1_xe.dat"
    files["Xe"]["pbs"] = ""
    files["Xe"]['prc'] = "prc89_xe.dat"
    files["W"] = {}     #74
    files["W"]['acd'] = "acd89_w.dat"
    files["W"]['scd'] = "scd89_w.dat"
    files["W"]['prb'] = "prb89_w.dat"
    files["W"]['plt'] = "plt89_w.dat"
    files["W"]['fis'] = "sxrfil14.dat"
    files["W"]['brs'] = "brs05360.dat"
    files["W"]['pls'] = "pls_W_14.dat"
    files["W"]['prs'] = "prs_W_14.dat"
    files["W"]['ccd'] = "ccd89_w.dat"
    files["W"]["pbs"] = "pbsx5_w.dat"
    files["W"]['prc'] = "prc89_w.dat"

    return files
