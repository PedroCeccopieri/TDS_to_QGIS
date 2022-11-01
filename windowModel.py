import pandas as pd
import xarray as xr

class windowModel():

    def __init__(self):

        self.datasets = None

    def openJson(self, url):
        """ Try to access the URL given in "Dataset Configuration File"
            and gets the (name, url, style) for each dataset from the json file. """
        try:

            self.datasets = pd.read_json(url) # return a pandas.Dataframe
            return True

        except:

            print("Error while loading the json file")
            self.datasets = None
            return False

    def getDatasetsNames(self):
        """ Return a list with all datasets names from self.datasets if it exist. """
        if (self.datasets is not None):
            return [row['name'] for index, row in self.datasets.iterrows()]
        else:
            return None

    def getDatasetUrl(self, name):
        """ Get the url from a specified dataset if self.datasets exist. """
        if (self.datasets is not None):
            return self.datasets[self.datasets["name"] == name].iloc[0].to_dict()["url"]
        else:
            return None

    def getDatasetStyle(self, name):
        """ Get the style from a specified dataset if self.datasets exist. """
        if not (self.datasets is None):
            return self.datasets[self.datasets["name"] == name].iloc[0].to_dict()["style"]
        else:
            return None

    def getData(self, url):
        """ Access the dataset in the URL and extract all data contained in it. """
        try:

            with xr.open_dataset(url) as ds:

                time = ds['time'].values
                latitude = ds['latitude'].values
                longitude = ds['longitude'].values
                dVars = list(ds.data_vars)

                if ('depth' in list(ds.variables)):
                    depth = ds['depth'].values
                else:
                    depth = None

        except:

            print("Error while loading dataset url")
            time, latitude, longitude, depth, dVars = (None,)*5

        return (time, latitude, longitude, depth, dVars)
