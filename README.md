# bcbathymetry
Making rasters and kmls for sfmc (and Glimpse?)

## layers and KMLs for SFMC and maybe glimpse for cproof:

Note rasters are made here with `plotBC_DEM.py` and saved to `cproof/data` or `kmls`.   The `cproof/data` directory needs to be synced to `/usr/local/opt/mapserver/cproof/`.  Note that the file `/usr/local/etc/mapserver.conf` should also be updated to make shortforms for the maps to save typing the whole pathname

Note you need a copy of `british_columbia_3_msl_2013.nc`

## Install mapserver
- install mapserver: `brew install mapserver`

## Get cgi to be able to work
- copy to CGI bin directory and get CGI to work:
	- `sudo cp /usr/local/bin/mapserv /Users/cproof/CGI-Executables/`
	- `sudo chmod 755 /Users/cproof/CGI-Executables/`
	- uncomment `LoadModule cgi_module ...` in `/etc/apache2/httpd.conf`
	- edit `/etc/apache2/extra/httpd-vhosts-le-ssl.conf` to have

```
   ScriptAlias /cgi-bin/ "/Users/cproof/CGI-Executables/"

    <Directory "/Users/cproof/Sites/">
        Options Indexes FollowSymLinks
        AllowOverride All
        Allow from all
        Require all granted
    </Directory>

    <Directory "/Users/cproof/CGI-Executables/">
       AllowOverride None
       Options ExecCGI
       AddHandler cgi-script .cgi .pl
       Require all granted
    </Directory>
```


Phew, seems to work

## get mapserver running
- add `SetEnv MAPSERVER_CONFIG_FILE /usr/local/etc/mapserver.conf` to `httpd.conf` to tell `mapserv` where the config file is.
- Edit `/usr/local/etc/mapserver.conf` to include our map files...
- Make files like `/usr/local/opt/mapserver/cproof/BCNorth0400.map` and add the raster files to go with them.
- Make raster files in `/Users/jklymak/Dropbox/bathy/plotBC_DEM.py`
- To access in QGIS:  `https://cproof.uvic.ca/cgi-bin/mapserv?map=BCNORTH0400&SERVICE=WMS&VERSION=1.3`
	-  same as `https://cproof.uvic.ca/cgi-bin/mapserv?map=/usr/local/opt/mapserver/cproof/BCNorth0400.map&SERVICE=WMS&VERSION=1.3`
	- To get capabilities: `https://cproof.uvic.ca/cgi-bin/mapserv?map=BCNORTH0400&SERVICE=WMS&VERSION=1.3&REQUEST=GetCapabilities`
	- In SFMC:  `https://cproof.uvic.ca/cgi-bin/mapserv?map=BCNORTH0400` is fine, and then use layer `BCNorth0000to0400`
	- TO veiw on web?  `https://cproof.uvic.ca/cgi-bin/mapserv?map=BCNORTH0400&SERVICE=WMS&VERSION=1.3&REQUEST=GetMap&Layers=BCNorth0000to0400&CRS=EPSG:4326&BBOX=-130.0,51.0,-128.0,53.0&FORMAT=png&WIDTH=1000&HEIGHT=700`

