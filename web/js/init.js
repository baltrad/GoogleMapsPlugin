// Google Maps variables
var map;
var radar;
var opacity;    
    
// Radar variables
var update_time = 300000;
var update_timeout_id = null;
var num_loaded = 0;
var frame=0;
var rep_time=500;
var add_time=2000;
var loaded = 0;
var timeout_id = null;
var images_rad  = new Array();	/* radar */
var texts_time = new Array();	/* time */   
    
// ---------------------------------------------------------------------------------------------------------------

function initialize() {
  if (GBrowserIsCompatible()) {
    map = new GMap2(document.getElementById("map"));
	
    // Set map center and zoom
    var point = new GLatLng(parseFloat(lat), parseFloat(lon));
    if(zoom>maxMapScale) {
      zoom=maxMapScale;
    } 	
    map.setCenter(point, parseInt(zoom));
		
    // Set default UI interface
    map.addControl(new GLargeMapControl3D());
    map.addControl(new GMapTypeControl());
    map.addControl(new GScaleControl(), new GControlPosition(G_ANCHOR_BOTTOM_LEFT, new GSize(105,40)));     
    map.enableDoubleClickZoom();
    map.enableScrollWheelZoom();    
    new GKeyboardHandler(map); // Keyboard enabled

    // Add terrain map and set default map type
    map.addMapType(G_PHYSICAL_MAP);

    if(maptype.length==1){
      maptype=map.getMapTypes()[maptype];    
    }
    map.setMapType(maptype);

    // Restricting the range of Zoom Levels =====
    var mapTypes = map.getMapTypes();
    for (var i=0; i<mapTypes.length; i++) {
      mapTypes[i].getMinimumResolution = function() {return minMapScale;}
	    mapTypes[i].getMaximumResolution = function() {return maxMapScale;}
    }
 		
    // Add Overview map
    map.addControl(new GOverviewMapControl());
		
    // Add Local search button
    map.addControl(new google.maps.LocalSearch(), new GControlPosition(G_ANCHOR_BOTTOM_LEFT,new GSize(105,5)));
	   
    // Add radar to map   
    radar = EInsert.groundOverlay("./img/nic.png", boundaries);
    map.addOverlay(radar);

    // Add name and copyright info into title box   
    document.getElementById('span_title_name').innerHTML=title_string_name;
    document.getElementById('div_title_copy').innerHTML=title_string_copyright;
    
    // Set opacity 
    document.getElementById('opacity').options[parseInt(opa)].selected=true;
    change_opacity();

    // Set animation speed
    document.getElementById('rep_time').options[parseInt(rep)].selected=true;
    change_rep_time();
    
    // Set additional time on the end of animation
    document.getElementById('add_time').options[parseInt(add)].selected=true;
    change_add_time();

    // Set update time of radar image list
    document.getElementById('update_time').options[parseInt(update)].selected=true;
    change_update_time();
  
    // Load radar image list
    update_radar_image_list();
	
    change_center_boundary();
    change_colorbar();
    // Hide "loading" DIV and show loaded content
    setTimeout("document.getElementById('loading').style.display = 'none'; document.getElementById('loaded').style.visibility = 'visible';", 1000);
	
  }else{
    alert("Sorry, the Google Maps API is not compatible with this browser !");
  }	    
}
