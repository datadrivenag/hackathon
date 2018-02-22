## Using Workbench

### Overview

The Workbench system is intended to provide web-based access to pre-configured data and software for the DataDrivenAg hackathon.

### Architecture
Workbench allows users to launch pre-defined Docker containers in a Kubernetes cluster with shared storage mounted via NFS.

### Quota
Each user has a quota of 2 cores and 8GB RAM and 10GB of storage in their `home` directory.

### Applications

* Cloud9 IDE with gcc, Java, Octave and Python including netCDF and GDAL utilities
* Jupyter SciPy environment with Python and Octave kernels including netCDF and GDAL utilities
* RStudio Geospatial environment
* PostgreSQL studio
* Xpra-based OpenBox minimal Linux desktop with QGIS and Panopoly

### Sample data

TERRA-REF sample data is mounted under `/data/terraref/sites/ua-mac/Level_1`:

Directory | Coverage | Description 
--- | --- | ---
`envlog_netcdf` | 6/20-6/21/2017 | PAR, CO2, Skye PRI, Clima Weather station 
`fullfield`|  Varied | Thumbnail RGB and IR full-field images. 50% resolution for 6/20/2017 
`ir_geotiff`| 6/20-6/21/2017 |  
`laser3d_mergedlas`| 6/20-6/21/2017 | 
`rgb_geotiff`| 6/20-6/21/2017 | 
`vnir_netcdf`| 6/18/2017 |  

### Geoserver
A geoserver instance is available to access some sample data:

URL: `http://geoserver.workshop1.nationaldataservice.org`

What's available:
WMS:
* RGB fullfield GeoTiffs

WCS:
* IR and UAV fullfield GeoTiffs

WFS:
* TERRA-REF Season 4 plot boundaries (i.e., BETYdb "sites" table)
