from .infoWindow import infoWindow

from .windowModel import windowModel
from .windowView import windowView

from qgis.utils import iface
from qgis.core import QgsMeshLayer, QgsProject, QgsLayerTreeLayer

import xarray as xr
import numpy as np
import datetime

class windowControl():

	def __init__(self):

		self.wnd = infoWindow()

		self.model = windowModel()
		self.view = windowView(self.wnd)

		# All triggers connections to their functions #

		self.wnd.OKButton.clicked.connect(self.run)
		self.wnd.jsonBrowseButton.clicked.connect(self.view.browseJson)
		self.wnd.jsonSelectButton.clicked.connect(self.selectJson)
		self.wnd.tempBrowseButton.clicked.connect(self.view.browseTempDir)
		self.wnd.comboBox.currentIndexChanged.connect(self.setBoxesLimits)
		self.wnd.checkBox.toggled.connect(self.toggleUseCheckBox)

		self.desableBoxes()

		self.view.showWindow()

	def desableBoxes(self, boxes = [True,True,True,True]):

		if (boxes[0]):
			self.view.setDateTimeEnabled(False)
			self.view.setDateTimeZero()
		if (boxes[1]):
			self.view.setLongitudeEnabled(False)
			self.view.setLongitudeZero()
		if (boxes[2]):
			self.view.setLatitudeEnabled(False)
			self.view.setLatitudeZero()
		if (boxes[3]):
			self.view.setDepthEnabled(False)
			self.view.setDepthZero()

	def selectJson(self):

		if not (self.model.openJson(self.view.getJsonUrl())):

			self.desableBoxes()

		self.view.addNamesComboBox(self.model.getDatasetsNames())

	def setBoxesLimits(self):

		name = self.view.getCurrentDatasetName()

		if (name):

			url = self.model.getDatasetUrl(name)
			
			dateTime, latitude, longitude, depth, dVars = self.model.getData(url)

			if (dateTime is not None):

				minDate = min(dateTime).astype("datetime64[s]").item().strftime("%Y-%m-%dT%H:%M:%SZ")
				maxDate = max(dateTime).astype("datetime64[s]").item().strftime("%Y-%m-%dT%H:%M:%SZ")
			
				self.view.setDateTimeEnabled(True)
				self.view.setDateTimeLimits(minDate,maxDate)

			else:

				self.view.setDateTimeZero()
				self.view.setDateTimeEnabled(False)

			if (longitude is not None and not self.view.getCheckBoxState()):

				minLon = min(longitude)
				maxLon = max(longitude)

				self.view.setLongitudeEnabled(True)
				self.view.setLongitudeLimits(minLon,maxLon)

			else:

				self.view.setLongitudeZero()
				self.view.setLongitudeEnabled(False)

			if (latitude is not None and not self.view.getCheckBoxState()):

				minLat = min(latitude)
				maxLat = max(latitude)

				self.view.setLatitudeEnabled(True)
				self.view.setLatitudeLimits(minLat,maxLat)

			else:

				self.view.setLatitudeZero()
				self.view.setLatitudeEnabled(False)

			if (depth is not None and not self.view.getCheckBoxState()):
				
				minDep = min(depth)
				maxDep = max(depth)

				self.view.setDepthEnabled(True)
				self.view.setDepthLimits(minDep,maxDep)

			else:

				self.view.setDepthZero()
				self.view.setDepthEnabled(False)

			self.view.setVariablesClear()
			if not (dVars is None):
		
				self.view.setVariblesNames(dVars)

	def run(self):

		name = self.view.getCurrentDatasetName()
		url = self.model.getDatasetUrl(name)

		if (url is None):
			print("No dataset found")
			return

		style = self.model.getDatasetStyle(name)
		time = [self.view.getMinDateTime().toPyDateTime(), self.view.getMaxDateTime().toPyDateTime()]
		var = self.view.getVariables()
		var = [i.text() for i in var] if var != [] else None

		if (self.view.getCheckBoxState()): # To use the canvas lon/lat
            
			aux = iface.mapCanvas().extent()
			lon = [aux.xMinimum(), aux.xMaximum()]
			lat = [aux.yMinimum(), aux.yMaximum()]
			dep = None

		else:

			lon = [self.view.getMinLongitude(), self.view.getMaxLongitude()]
			lat = [self.view.getMinLatitude(), self.view.getMaxLatitude()]
			dep = [self.view.getMinDepth(), self.view.getMaxDepth()] if self.view.isDepthEnable() else None
			
		existDataset = self.createTempFile(name, url, [time,lon,lat,dep,var])

		if (existDataset):
			temp, dt_actual = existDataset
			self.createMeshLayer(name, temp, dt_actual, style)

	def createTempFile(self, name, url, extent): # extent = [[minTime, maxTime],[minLon, maxLon], [minLat, minLat], [minDep, maxDep], [dVars]]
		""" Get the data from a NetCDF/THREDDS, make a temporal/spatila subset and
        save it to a local file in the "Temp Directory". """

		minTime, maxTime = extent[0] if not extent[0] is None else [None, None]
		dVars = extent[4] if not extent[4] is None else None
		minLon, maxLon = extent[1] if not extent[1] is None else [None, None]
		minLat, maxLat = extent[2] if not extent[2] is None else [None, None]
		minDep, maxDep = extent[3] if not extent[3] is None else [None, None]

		dt = minTime

		print(f"Getting data from dataset '{name}'.")
		print(f'Requested time: {dt:%Y-%m-%d %H:%M:%S}')

		with xr.open_dataset(url).sel(time=[dt], method='nearest') as ds:
		#with xr.open_dataset(url).sel(time= slice(minTime, maxTime)) as ds:

			# get the actual date available (nearest)
			dt_actual = self.to_datetime(ds['time'].values[0])
			tdelta = dt - dt_actual
			print(f'Nearest available time: {dt_actual:%Y-%m-%d %H:%M:%S}')
			print(f'Time difference: {str(abs(tdelta))}')

			msg = (f"Dataset {name}: Nearest available time "
			       f"({dt_actual:%Y-%m-%d %H:%M:%S}) has a significative offset "
			       f"({str(abs(tdelta))}) from the requested time "
			       f"({dt:%Y-%m-%d %H:%M:%S}).")

			if abs(tdelta.total_seconds()) > 86400:
				iface.messageBar().pushMessage('Warning', msg, level = Qgis.Warning, duration = 20)

			ds = ds if extent[3] is None else ds.sel(depth = slice(minDep, maxDep))
			ds = ds if extent[4] is None else ds[dVars]
			ds = ds.sel(longitude=slice(minLon, maxLon), latitude=slice(minLat, maxLat))

			ds.load()

            # fix attributes so that MDAL can recognize u and v components
			for var in ds.data_vars:

				long_name = ds[var].attrs.get('long_name')

				if long_name is None:
					continue

				ds[var].attrs['long_name'] = (long_name
													.replace('zonal component', 'u component')
													.replace('meridional component', 'v component'))

				tmp = (self.view.tempDir / f'file{np.random.randint(0, 1_000_000):06d}.nc')

			sizes = ds.sizes
			la, lo = sizes['latitude'], sizes['longitude']

			if not (la > 0 and lo > 0):
				print("There is no datasets on this range")
				return False
			else:
				ds.to_netcdf(tmp)

		return (tmp, dt_actual)

	def to_datetime(self, dt):

		timestamp = ((dt - np.datetime64('1970-01-01T00:00:00')) / np.timedelta64(1, 's'))
		return datetime.datetime.utcfromtimestamp(timestamp)

	def createMeshLayer(self, name, temp, dt_actual, style, group='datasets'):

		layer_name = f'{name} - {dt_actual:%Y-%m-%d %H:%M:%S}'

		print(f"Creating layer '{layer_name}'.")

		layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]

		if layer_name in layer_names:
			print(f"There is already an active layer '{layer_name}'.")

		layer = QgsMeshLayer(path=str(temp), baseName=layer_name, providerLib='mdal')

		if style:
			layer.loadNamedStyle(str(style))
			iface.layerTreeView().refreshLayerSymbology(layer.id())

		root = QgsProject.instance().layerTreeRoot()

		if group is None:

			group_node = root

		else:

			group_node, group_new = ((root.addGroup(group), True) if root.findGroup(group) is None else (root.findGroup(group), False))

	        # set as first in layer tree view if newly created group
	        # https://www.lutraconsulting.co.uk/blog/2014/07/25/qgis-layer-tree-api-part-2/
			if group_new:
				group_clone = group_node.clone()
				root.insertChildNode(0, group_clone)
				root.removeChildNode(group_node)
				group_node = group_clone

	    # add the layer without showing it
		QgsProject.instance().addMapLayer(layer, addToLegend=False)

	    # https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/loadlayer.html?highlight=insertchildnode#qgsproject-instance
	    # group_node.addLayer(layer)   # add layer as last
		group_node.insertChildNode(0, QgsLayerTreeLayer(layer))   # add layer as first

	    # Expand the layer item in the legend
		layer_node = root.findLayer(layer.id())
		layer_node.setExpanded(False)   # must be False and then True
	    # layer_node.setExpanded(True)

	    # it is possible to load the data from a local file and then delete it ???
	    # os.remove(tmp)

		return

	def toggleUseCheckBox(self):

		if (self.view.getCheckBoxState()):
			self.desableBoxes([False,True,True,True])
		else:
			self.setBoxesLimits()
		