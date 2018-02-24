## Using Workbench

### Overview

The Workbench system is intended to provide web-based access to pre-configured data and software for the DataDrivenAg hackathon.

### System requirements
The Workbench system can be used on systems with most modern browsers. 

### Architecture
Workbench allows users to launch pre-defined Docker containers in a Kubernetes cluster with shared storage mounted via NFS.

### Quota
Each user has a quota of 2 cores and 8GB RAM and 10GB of storage in their `home` directory.

### Applications

* Cloud9 IDE with gcc, Java, Octave and Python including netCDF and GDAL utilities
* Jupyter SciPy environment with Python and Octave kernels including netCDF, GDAL, cartopy, and rasterio.
* [RStudio Geospatial](https://github.com/rocker-org/geospatial) environment
* PostgreSQL studio for accessing the BETYdb Postgres database
* Xpra-based OpenBox minimal Linux desktop with QGIS and Panopoly

### Sample data

TERRA-REF sample data is mounted under `/data/terraref/sites/ua-mac/Level_1` in any running application:

Directory | Coverage | Description 
--- | --- | ---
`envlog_netcdf` | 6/20-6/21/2017 | PAR, CO2, Skye PRI, Clima Weather station 
`fullfield`|  Varied | Thumbnail RGB and IR full-field images. 50% resolution onlyfor 6/20/2017 
`ir_geotiff`| 6/20-6/21/2017 |  Full-resolution data from the FLIR camera
`laser3d_mergedlas`| 6/20-6/21/2017 | 
`rgb_geotiff`| 6/20-6/21/2017 | Full-resolution data from the RGB (stereoTop) camera
`vnir_netcdf`| 6/18/2017 |  Sample of hyperspectral data from the VNIR sensor
`uav` | 5/24, 6/6, 7/21 | Sample of RedEdgeand Sequoia UAV fullfield images

The data is mounted under `/data` in all Workbench applications or available via https://data.workshop1.nationaldataservice.org (note: some files are very large).

### Geoserver
A geoserver instance is available to access a subset of the some data:

Connection information:
Service | URL
--- | ---
WMS | http://geoserver.workshop1.nationaldataservice.org/geoserver/wms?tiled=true
WCS | http://geoserver.workshop1.nationaldataservice.org/geoserver/wcs
WFS | http://geoserver.workshop1.nationaldataservice.org/geoserver/wfs


What's available:
WMS:
* 2% resolution RGB fullfield GeoTiffs
* 50% resolution RGB GeoTiff for 6/20/2017

WCS:
* IR and UAV fullfield GeoTiffs

WFS:
* TERRA-REF Season 4 plot boundaries (i.e., BETYdb "sites" table)


### Visualization tools (Xpra)
The "Visualization Tools" application provides a no-frills Linux remote desktop environment to use desktop applications such as QGIS and Panopoly.  This is based on the OpenBox Linux distribution.  All applications are launched via xterm and accessed via the Xpra HTML5 client.  While this is in some ways convenient, there are many limitations (such as inability to copy-paste). The following video demonstrates how to launch QGIS via the browser and load sample GeoTIFFs.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=6UYWpS9lzxs" target="_blank"><img src="http://img.youtube.com/vi/6UYWpS9lzxs/0.jpg"  alt="Using Workbench" width="240" height="180" border="10" /></a>
