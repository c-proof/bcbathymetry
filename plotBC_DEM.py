"""
Example script to plot the Cascaade DEM
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import xarray as xr

import simplekml

import cartopy.crs as ccrs

# +lon_0=-124.5 +lat_1=41.5 +lat_2=50.5 +lat_0=38.0 +ellps=clrk66"


savedir = './cproof/data/'
kmldir = './kmls'
lims = {}
lims['North'] = [slice(-133, -126-25/60), slice(50, 53)]
lims['South'] = [slice(-129+36/60, -124-33/60), slice(47, 50)]
kmllevels = [50, 100, 200, 1000]
vmin = -400
vmax = 0
todo = 'South'
with xr.open_dataset('british_columbia_3_msl_2013.nc') as ds:
    print(ds.attrs)
    print(ds.lon.values[0], ds.lat.values[0], ds.lon.values[-1], ds.lat.values[-1])
    dpi=1000

    dd = ds.sel(lon=lims[todo][0], lat=lims[todo][1]).fillna(1)
    dlon = dd.lon[-1] - dd.lon[0]
    dlat = dd.lat[-1] - dd.lat[0]
    aspect = dlon * np.cos(51*np.pi/180) / dlat
    print(aspect)
    print(dd.Band1.values)
    N = len(dd.lon)
    M = len(dd.lat)
    sub=1

    datacrs = ccrs.PlateCarree()
    crsout = ccrs.PlateCarree()
    fig = plt.figure(figsize=(N/dpi/sub, M/dpi/sub))
    ax = fig.add_axes([0., 0., 1, 1], projection=crsout)
    ax.set_facecolor('none')
    ax.axis('off')
    fig.set_facecolor('none')

    cmap = plt.get_cmap('Blues_r').copy()
    cmap.set_over('g')
    cmap.set_under('none')

    if False:
        ax.pcolormesh(dd.lon[::sub], dd.lat[::sub], dd.Band1[::sub, ::sub],
                  vmin=-400, vmax=0, cmap=cmap,
                  transform=datacrs)
    ax.contourf(dd.lon[::sub], dd.lat[::sub], dd.Band1[::sub, ::sub], rasterized=True,
               levels=np.unique(np.hstack([-5000, np.linspace(vmin, vmax-1, 20), 10])), vmax=vmax, vmin=vmin, cmap=cmap)
    fig.savefig(f'{savedir}BC{todo}{np.abs(vmax):04d}to{np.abs(vmin):04d}.png', dpi=dpi, pad_inches=0)
    print(dd.lon.values[0], dd.lat.values[0], dd.lon.values[-1], dd.lat.values[-1])

# now make KMLs:
with xr.open_dataset('british_columbia_3_msl_2013.nc') as ds:
    dd = ds.sel(lon=lims[todo][0], lat=lims[todo][1]).fillna(1)
    dlon = dd.lon[-1] - dd.lon[0]
    dlat = dd.lat[-1] - dd.lat[0]
    aspect = dlon * np.cos(51*np.pi/180) / dlat
    fig = plt.figure(figsize=(24, 24/aspect))
    ax = fig.add_axes([0, 0, 1, 1])
    sub=2
    #ax.pcolormesh(dd.lon[::sub], dd.lat[::sub], dd.Band1[::sub, ::sub], rasterized=True,
    #              vmin=-400, vmax=400, cmap='RdBu_r')
    cc = ax.contour(dd.lon[::sub], dd.lat[::sub], -dd.Band1[::sub, ::sub], rasterized=True,
               levels=kmllevels, colors='r', linewidths=0.06)

colors = [simplekml.Color.red, simplekml.Color.yellow, simplekml.Color.greenyellow, simplekml.Color.cyan ]
colors = ['#00FF55EE', '#55AA00EE', '#BB8800EE', '#DD2200EE',]
for nlevel, level in enumerate(cc.allsegs):
    kml = simplekml.Kml()
    sharedstyle = simplekml.Style()
    sharedstyle.linestyle.color = colors[nlevel]  # Red
    sharedstyle.linestyle.width = 1

    for nseg, seg in enumerate(cc.allsegs[nlevel]):
        print(nseg)
        ls = kml.newlinestring(name=f'{nlevel} {nseg}')
        data = np.asarray(seg)
        data = np.round(data*1e4)/1e4
        ls.coords=data
        ls.style = sharedstyle
        #if nlevel==0:
        #    ls.style.linestyle.color=simplekml.Color.orangered
    kml.save(f'Contours{todo}{kmllevels[nlevel]:04d}.kml', format=False)