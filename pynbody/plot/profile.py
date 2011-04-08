from .. import analysis
from ..analysis import angmom
from ..analysis import profile
from .. import filt

import pylab as p

def rotation_curve(s, center=True, r_units = 'kpc',
                   v_units = 'km s^-1', disk_height='100 pc', nbins=50,
                   bin_spacing = 'equaln', clear = True, quick=False,
                   filename=None,**kwargs) :
    """Centre on potential minimum, align so that the disk is in the
    x-y plane, then use the potential in that plane to generate and
    plot a rotation curve."""

    if center :
        angmom.faceon(s)

    if 'min' in kwargs :
        min_r = kwargs['min']
    else:
        min_r = s['rxy'].min()
    if 'max' in kwargs :
        max_r = kwargs['max']
    else:
        max_r = s['rxy'].max()

    pro = profile.Profile(s, type=bin_spacing, nbins = nbins,
                          min = min_r, max = max_r)

    r = pro['rbins'].in_units(r_units)
    if quick :
        v = pro['rotation_curve_spherical'].in_units(v_units)
    else :
        v = pro['v_circ'].in_units(v_units)

    if clear : p.clf()

    p.plot(r, v)

    p.xlabel("r / $"+r.units.latex()+"$")
    p.ylabel("v_c / $"+v.units.latex()+'$')
    if (filename): 
        print "Saving "+filename
        p.savefig(filename)


def fourier_profile(sim, center=True, disk_height='100 pc', nbins=50,
                    r_units='kpc', bin_spacing = 'equaln', clear = True,
                    filename=None,**kwargs) :
    """Centre on potential minimum, align so that the disk is in the
    x-y plane, then plot the amplitude of the 2nd fourier mode as a 
    function of radius."""

    if center :
        angmom.faceon(sim)

    if 'min' in kwargs :
        min_r = kwargs['min']
    else:
        min_r = sim['rxy'].min()
    if 'max' in kwargs :
        max_r = kwargs['max']
    else:
        max_r = sim['rxy'].max()

    pro = profile.Profile(sim, type=bin_spacing, nbins = nbins,
                          min = min_r, max = max_r)

    r = pro['rbins'].in_units(r_units)
    fourierprof = pro['fourier']
    a2 = fourierprof['amp'][2]

    if clear : p.clf()

    p.plot(r, a2)

    p.xlabel("r / $"+r.units.latex()+"$")
    p.ylabel("Amplitude of Fourier 2nd")
    if (filename): 
        print "Saving "+filename
        p.savefig(filename)
