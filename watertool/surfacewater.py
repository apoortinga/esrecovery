import ee
import config
import oauth2client

ee.Initialize(config.EE_CREDENTIALS)

IMAGE_COLLECTION = ee.ImageCollection('JRC/GSW1_0/MonthlyHistory')

watershed = ee.FeatureCollection("ft:1vTonxuDFs7rBkt02H3ZzFy1SSFsNPhlPlRE15pVr","geometry")


def WaterMap(startDate,endDate):


  myjrc = IMAGE_COLLECTION.filterDate(startDate, endDate).filterBounds(watershed)
  
  # calculate total number of observations
  def calcObs(img):
	# observation is img > 0
	obs = img.gt(0);
	return ee.Image(obs).set('system:time_start', img.get('system:time_start'));  
  
  # calculate the number of times water
  def calcWater(img):
	  water = img.select('water').eq(2);
	  return ee.Image(water).set('system:time_start', img.get('system:time_start'));
      
  observations = myjrc.map(calcObs)
  
  water = myjrc.map(calcWater)
  
  # sum the totals
  totalObs = ee.Image(ee.ImageCollection(observations).sum().toFloat());
  totalWater = ee.Image(ee.ImageCollection(water).sum().toFloat());
  
  # calculate the percentage of total water
  returnTime = totalWater.divide(totalObs).multiply(100)

  # make a mask
  Mask = returnTime.gt(1)
  returnTime = returnTime.updateMask(Mask)
  
  # clip the result
  returnTime = returnTime #.clip(watershed)

  return returnTime.getMapId({
      'min': '0',
      'max': '100',
      'bands': 'water',
      'palette' : 'c10000,d742f4,001556,b7d2f7'
  })

 
def getSentinel():

  img0 = ee.Image("COPERNICUS/S2/20160823T184922_20160823T235521_T10TGK");
  img1 = ee.Image("COPERNICUS/S2/20160803T190133_20160803T235100_T10TFK");
  img2 = ee.Image("COPERNICUS/S2/20160714T190130_20160714T235020_T10TFL");

  mosaic = ee.ImageCollection([img0,img1,img2]).mosaic().clip(watershed);
  
  mapId = mosaic.getMapId({'min': 0, 'max': 2048,'bands':'B4,B3,B2'})
  
  return mapId

def mapForest():

  img0 = ee.Image("COPERNICUS/S2/20160823T184922_20160823T235521_T10TGK");
  img1 = ee.Image("COPERNICUS/S2/20160803T190133_20160803T235100_T10TFK");
  img2 = ee.Image("COPERNICUS/S2/20160714T190130_20160714T235020_T10TFL");

  mosaic = ee.ImageCollection([img0,img1,img2]).mosaic().clip(watershed);
  
  ndvi = mosaic.normalizedDifference(['B8', 'B4']);
  
  mask = ndvi.gt(0.5);
  forest = ndvi.mask(mask); 
  
  mapId = forest.getMapId({'min': 0, 'max': 1,'palette':'darkgreen'})
  
  return mapId

def mapSoil():

  img0 = ee.Image("COPERNICUS/S2/20160823T184922_20160823T235521_T10TGK");
  img1 = ee.Image("COPERNICUS/S2/20160803T190133_20160803T235100_T10TFK");
  img2 = ee.Image("COPERNICUS/S2/20160714T190130_20160714T235020_T10TFL");
  
  mosaic = ee.ImageCollection([img0,img1,img2]).mosaic().clip(watershed);
  
  ndbi = mosaic.normalizedDifference(['B8', 'B11']);
  mask = ndbi.lt(-0.1)
  soil = ndbi.mask(mask)
 
  mapId = soil.getMapId({'min': 0, 'max': 1,'palette':'red'})
  
  print mapId
  
  return mapId 

def mapGrass():


  img0 = ee.Image("COPERNICUS/S2/20160823T184922_20160823T235521_T10TGK");
  img1 = ee.Image("COPERNICUS/S2/20160803T190133_20160803T235100_T10TFK");
  img2 = ee.Image("COPERNICUS/S2/20160714T190130_20160714T235020_T10TFL");
  
  mosaic = ee.ImageCollection([img0,img1,img2]).mosaic().clip(watershed);
  
  ndvi = mosaic.normalizedDifference(['B8', 'B4']);
  mask1 = ndvi.lt(0.25);
  mask2 = ndvi.gt(0.0);
  grass = ndvi.mask(mask1).updateMask(mask2);
 
  mapId = grass.getMapId({'min': 0, 'max': 1,'palette':'yellow'})
  
  return mapId  
  
def mapShrub():

  img0 = ee.Image("COPERNICUS/S2/20160823T184922_20160823T235521_T10TGK");
  img1 = ee.Image("COPERNICUS/S2/20160803T190133_20160803T235100_T10TFK");
  img2 = ee.Image("COPERNICUS/S2/20160714T190130_20160714T235020_T10TFL");
  
  mosaic = ee.ImageCollection([img0,img1,img2]).mosaic().clip(watershed);
  
  ndvi = mosaic.normalizedDifference(['B8', 'B4']);
  
  mask1 = ndvi.lt(0.5)
  mask2 = ndvi.gt(0.25)

  ndbi = mosaic.normalizedDifference(['B8', 'B11']);
  mask = ndbi.gt(-0.1)

  shrub = ndvi.mask(mask1).updateMask(mask2).updateMask(mask)
 
  mapId = shrub.getMapId({'min': 0, 'max': 1,'palette':'65f442'})
  
  return mapId  
