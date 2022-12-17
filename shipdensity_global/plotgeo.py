from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import matplotlib.colors as mcolors

def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

if False:
    im = Image.open('./shipdensity_global.tif')
    w, h = im.size
    lon = np.arange(-180.0128112750, 180.012811, 0.005)
    lat = np.arange(85.0001479370, -85.0001479370, -0.005)
    lat = lat[:h]
    inlon = np.argwhere((lon>-145) & (lon<-124)).flatten()
    inlat = np.argwhere((lat>47) & (lat <54)).flatten()

    print(len(inlon), len(inlat), np.shape(inlon))
    im = im.crop((inlon[0], inlat[0], inlon[-1]+1, inlat[-1]+1))
    data = np.asanyarray(im)
    print(np.shape(data))
    data = rebin(data, (int(350/2), int(1050/2)))
    dpi = 200

    lon = lon[inlon[4::8]]
    lat = lat[inlat[4::8]]

    ds = xr.DataArray(dims=['lat', 'lon'],
                    coords={'lat':('lat', lat),
                            'lon':('lon', lon)},
                    data=data)
    ds.to_netcdf('shipden.nc')


with xr.open_dataarray('shipden.nc') as ds:
    dpi = 200
    M, N = np.shape(ds.data)

    datacrs = ccrs.PlateCarree()
    crsout = ccrs.PlateCarree()
    fig = plt.figure(figsize=(N/dpi, M/dpi))
    ax = fig.add_axes([0., 0., 1, 1], projection=crsout)
    ax.set_facecolor('none')
    ax.axis('off')
    fig.set_facecolor('none')
    #ds = ds.where(ds.data<=0, 1e-4)
    #ds = ds.where(np.isnan(ds.data), 1e-4)
    print(ds.data)
    norm = mcolors.LogNorm(100, 3e7)
    pc = ax.pcolormesh(ds.lon, ds.lat, ds, transform=datacrs,
                  norm=norm, cmap='Reds')
    #fig.colorbar(pc)
    print(ds.lon[0], ds.lat[0], ds.lon[-1], ds.lat[-1])
    print(ds)
    fig.savefig('../cproof/data/BCShipDens.png')
    plt.show()
