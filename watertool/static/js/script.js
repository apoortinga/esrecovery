/**
 * @fileoverview Runs the Ecodash Tool application. The code is executed in the
 * user's browser. It communicates with the App Engine backend, renders output
 * to the screen, and handles user interactions.
 */

// define a number of global variabiles
var DataArr = [];
var all_overlays = [];
var map;
var currentShape; 


 /**
 * Starts the Surface Water Tool application. The main entry point for the app.
 * @param {string} eeMapId The Earth Engine map ID.
 * @param {string} eeToken The Earth Engine map token.
 */
var boot = function(eeMapId, eeToken) {
	
	google.load('visualization', '1.0');

	var app = new App(eeMapId, 
					  eeToken
					  );
		
	document.getElementById('updateWaterMap').addEventListener("click", makeWaterMap);
	document.getElementById('updateSatellite').addEventListener("click", showSatellite);
	document.getElementById('forest').addEventListener("change", makeForest);
	document.getElementById('soil').addEventListener("change", makeSoil);
	document.getElementById('grass').addEventListener("change", makeGrass);
	document.getElementById('shrub').addEventListener("change", makeShrub);
	document.getElementById('clear').addEventListener("click", clearMap);

	
};


var makeWaterMap = function() {
	
	// get data from slider button
	var startDate = $("#aoiControl").val()[0]
	var endDate = $("#aoiControl").val()[1]
	
	var params = {};
	
	// set the parameters
	params['startDate'] = startDate;
	params['endDate'] = endDate;


	$.ajax({
      url: "/MakeWaterMap",
      data: params,
      dataType: "json",
      success: function (data) {
		 var mapType = getEeMapType(data.eeMapId, data.eeToken);
		 map.overlayMapTypes.push(mapType);
		
      },
      error: function (data) {
        alert("An error occured! Please refresh the page.");
      }
    });	
}    


var showSatellite = function() {
	
	console.log("show Satellite");
	
	$.ajax({
      url: "/showSentinel",
      dataType: "json",
      success: function (data) {
		 console.log(data);
		 var mapType = getEeMapType(data.eeMapId, data.eeToken);
		 map.overlayMapTypes.push(mapType);
      },
      error: function (data) {
        alert("An error occured! Please refresh the page.");
      }
    });	
}

var makeForest = function(){
	console.log("enabled");

$.ajax({
      url: "/mapForest",
      dataType: "json",
      success: function (data) {
		 console.log(data);
		 var mapType = getEeMapType(data.eeMapId, data.eeToken);
		 map.overlayMapTypes.push(mapType);
      },
      error: function (data) {
        alert("An error occured! Please refresh the page.");
      }
    });	
}	

var makeSoil = function(){

	console.log("entering")
	$.ajax({
      url: "/mapSoil",
      dataType: "json",
      success: function (data) {
		 console.log(data);
		 var mapType = getEeMapType(data.eeMapId, data.eeToken);
		 map.overlayMapTypes.push(mapType);
      },
      error: function (data) {
        alert("An error occured! Please refresh the page.");
      }
    });	
}	
	
var makeGrass = function(){

	console.log("entering")
	$.ajax({
      url: "/mapGrass",
      dataType: "json",
      success: function (data) {
		 console.log(data);
		 var mapType = getEeMapType(data.eeMapId, data.eeToken);
		 map.overlayMapTypes.push(mapType);
      },
      error: function (data) {
        alert("An error occured! Please refresh the page.");
      }
    });	
}	

var makeShrub = function(){

	console.log("entering")
	$.ajax({
      url: "/mapShrub",
      dataType: "json",
      success: function (data) {
		 console.log(data);
		 var mapType = getEeMapType(data.eeMapId, data.eeToken);
		 map.overlayMapTypes.push(mapType);
      },
      error: function (data) {
        alert("An error occured! Please refresh the page.");
      }
    });	
}	
		
	

// ---------------------------------------------------------------------------------- //
// The application
// ---------------------------------------------------------------------------------- //
/**
 * The main Surface Water Tool application.
 * @param {google.maps.ImageMapType} mapType The map type to render on the map.
 */
var App = function(eeMapId, eeToken) {
  
  console.log("map")
  // Create and display the map.
  map = createMap();
 
 	
   
  // Load the default image.
  //refreshImage(eeMapId, eeToken);
  
 
  //channel = new goog.appengine.Channel(eeToken);
    
  // create listeners for buttons and sliders
  //setupListeners();
  
  // run the slider function to initialize the dates  
  //slider();ss
  
 };

/**
 * Creates a Google Map for the given map type rendered.
 * The map is anchored to the DOM element with the CSS class 'map'.
 * @param {google.maps.ImageMapType} mapType The map type to include on the map.
 * @return {google.maps.Map} A map instance with the map type rendered.
 */
var createMap = function() {
  
  // set the map options
  var mapOptions = {
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
	maxZoom: MAX_ZOOM,
	streetViewControl: false,
	mapTypeId: 'roadmap'
  };

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);
  console.log("returning map")

  return map;
};



	

// ---------------------------------------------------------------------------------- //
// Layer management
// ---------------------------------------------------------------------------------- //

/** Updates the image based on the current control panel config. */
var refreshImage = function(eeMapId, eeToken) {
	console.log(eeMapId)
	console.log(eeToken)
  var mapType = getEeMapType(eeMapId, eeToken);
  map.overlayMapTypes.push(mapType);
};

var opacitySliders = function() {

  setLayerOpacity($("#opacitySlider").val());
  
}

var setLayerOpacity = function(value) {
  map.overlayMapTypes.forEach((function(mapType, index) {
    if (mapType) {
	  var overlay = map.overlayMapTypes.getAt(index);
      overlay.setOpacity(parseFloat(value));
    }
  }).bind(this));
};

/**
* Clear polygons from the map when changing from country to province
**/
var clearMap = function () {

	console.log("clear map");
	map.overlayMapTypes.clear();
};


// ---------------------------------------------------------------------------------- //
// Static helpers and constants
// ---------------------------------------------------------------------------------- //

/**
 * Generates a Google Maps map type (or layer) for the passed-in EE map id. See:
 * https://developers.google.com/maps/documentation/javascript/maptypes#ImageMapTypes
 * @param {string} eeMapId The Earth Engine map ID.
 * @param {string} eeToken The Earth Engine map token.
 * @return {google.maps.ImageMapType} A Google Maps ImageMapType object for the
 *     EE map with the given ID and token.
 */
var getEeMapType = function(eeMapId, eeToken) {
  var eeMapOptions = {
    getTileUrl: function(tile, zoom) {
      var url = EE_URL + '/map/';
      url += [eeMapId, zoom, tile.x, tile.y].join('/');
      url += '?token=' + eeToken;
      return url;
    },
    tileSize: new google.maps.Size(256, 256),
    name: 'FloodViewer',
	opacity: 1.0,
	//mapTypeId: 'satellite'
	mapTypeId: 'roadmap'
  };
  return new google.maps.ImageMapType(eeMapOptions);
};

/** @type {string} The Earth Engine API URL. */
var EE_URL = 'https://earthengine.googleapis.com';

/** @type {number} The default zoom level for the map. */
var DEFAULT_ZOOM = 11;

/** @type {number} The max allowed zoom level for the map. */
var MAX_ZOOM = 25;

/** @type {Object} The default center of the map. */
var DEFAULT_CENTER = {lng: -121.003, lat: 40.30};

/** @type {string} The default date format. */
var DATE_FORMAT = 'yyyy-mm-dd';

/** The drawing manager	*/
var drawingManager;
