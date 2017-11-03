import ee
import config
import oauth2client

ee.Initialize(config.EE_CREDENTIALS)

IMAGE_COLLECTION = ee.ImageCollection('JRC/GSW1_0/MonthlyHistory')

watershed = ee.FeatureCollection("ft:1vTonxuDFs7rBkt02H3ZzFy1SSFsNPhlPlRE15pVr","geometry")
lulc = ee.Image("users/servirmekong/california/RegionalLC")

pal = '6f6f6f,aec3d4,b1f9ff,111149,287463,152106,c3aa69,9ad2a5,7db087,486f50,387242,115420,cc0013,8dc33b,ffff00,a1843b,cec2a5,674c06,3bc3b2,f4a460,800080'

def showLandCover(mylegend):
  
  print "legend", mylegend
  mymask = ee.Image(0)

  # enable all checked boxes
  for value in mylegend:
    print value
    tempmask = lulc.eq(ee.Number(int(value)))
    mymask = mymask.add(tempmask)

  
  print "returning" 	
  return lulc.updateMask(mymask).getMapId({
      'min': '0',
      'max': '20',
      'palette' : pal

  })	

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


def getSummer():

  summer = ee.Image("users/servirmekong/california/summer").clip(watershed)
     
  mapId = summer.getMapId({'min': 0, 'max': 2048,'bands':'red,green,blue'})
  
  return mapId

  
def getWinter():

  summer = ee.Image("users/servirmekong/california/winter").clip(watershed)
       
  mapId = summer.getMapId({'min': 0, 'max': 2048,'bands':'red,green,blue'})
  
  return mapId  


def getFire():
	
	fire = ee.Image("users/servirmekong/californiaFire").clip(watershed)
	
	print fire
	mapId = fire.getMapId({'min': 70, 'max': 100,'palette':'yellow,orange,red'})
	
	print mapId
	return mapId  
