import ee
import pandas as pd

def get_ndvi_timeseries(project_id: str, bbox: list, start: str, end: str):
     """Fetches Sentinel-2 NDVI time series for construction progress."""
     ee.Initialize(project = project_id)
     roi = ee.Geometry.Rectangle(bbox)

     collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                   .filterBounds(roi)
                   .filterDate(start, end)
                   .filter(ee.Filter.ly('CLOUDY_PIXEL_PERCENTAGE', 20)))
     
     def compute_ndvi(image):
          ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
          mean_ndvi = ndvi.reduceRegion(ee.Reducer.mean(), roi, 10).get('NDVI')
          return ee.Feature(None, {'date': image.date().format('YYYY-MM-dd'), 'NDVI': mean_ndvi})
     
     features = ee.FeatureCollection(collection.map(compute_ndvi)).getInfo()['features']
     data = [{'date': f['properties']['date'], 'NDVI': f['properties']['NDVI']} for f in features]
     df = pd.DataFrame(data)
     df['date'] = pd.to_datetime(df['date'])
     return df
