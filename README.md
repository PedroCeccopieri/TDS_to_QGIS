Plugin to retrive data from a THREDDS server and load as a MeshLayer on QGIS.

This plugin allows the user to retrive data from a [THREDDS](https://github.com/Unidata/tds) (Thematic Real-time Environmental Distributed Data Services) server. This type of server is the standard to host environmental forecast and hindcast data, like wind, wave and ocean currents. There were already some previous methods to load these type of data (netCDF) in QGIS using WMS (Web Map Service), but they didn't allow the user the flexibility of easily selecting the desired time, changing the color scale range, etc.
With this plugin the user can select and load a subset of a dataset hosted in a THREDDS server, avoiding downloading the full dataset. Only the desired data is downloaded and stored locally as a netCDF file. The file is then loaded on QGIS using the MeshLayer format. MeshLayer is used in favor of Raster for the capability of display non-orthogonal grids (e.g.: varying latitude and longitude) and non-structured grids (e.g.: common in finit elements models).
The only non standard library needed is the [Xarray](https://pypi.org/project/xarray/), [netCDF4](https://pypi.org/project/netCDF4/) and [h5netcdf](https://pypi.org/project/h5netcdf/) python packages.
