// Google Maps variables
var map;
var radar;
var opacity;    
var marker;
    
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
var images_qual  = new Array();	/* quality */
images_qual["qblock"] = new Array();
images_qual["qanom"] = new Array();
images_qual["pover"] = new Array();
var texts_time = new Array();	/* time */   
var quality = false;
// ---------------------------------------------------------------------------------------------------------------
function isCanvasSupported(){
  var elem = document.createElement('canvas');
  return !!(elem.getContext && elem.getContext('2d'));
}

function initialize() {
    if (!isCanvasSupported()) {
        alert("This website uses HTML5 canvases. You are running a browser that does not support them. Please use a recent version of Firefox, Chrome, Opera, Safari, or a W3C-compliant version of Explorer.");
	window.location = "http://www.baltrad.eu/"
        return false;
    }
    /// Create map

    // Set map center and zoom
    var point = new google.maps.LatLng(parseFloat(lat), parseFloat(lon));
    if(zoom>maxMapScale) {
      zoom=maxMapScale;
    } 	
    
    viewportwidth = window.innerWidth;
    if (!viewportwidth)
        viewportwidth = document.body.clientWidth;
    viewportheight = window.innerHeight;
    // Set default UI interface
    var mapoptions = {
        center: point,
        zoom: parseInt(zoom),
        disableDoubleClickZoom: false,
        minZoom: minMapScale,
        maxZoom: maxMapScale,
        scrollwheel: true,
        keyboaldShortcuts: true,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        mapTypeControl: true,
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR},
        overviewMapControl: true,
        overviewMapControlOptions: {opened: viewportwidth > 1024},
        scaleControl: true,
        streetViewControl: false
    };
        
    map = new google.maps.Map(document.getElementById("map"), mapoptions);


    /// Create radar overlay
    /// ./img/nic.png Dont initialize overlay with nic.png it doesn't exist
    radar = new ProjectedOverlay(map, "", boundaries, {id: "radar_img", percentOpacity: 60});
    

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

    toggle_quality();
    // Hide "loading" DIV and show loaded content
    setTimeout("document.getElementById('loading').style.display = 'none'; document.getElementById('loaded').style.visibility = 'visible';", 1000);

    // Search bar
    var element = document.getElementById('search_location');

    map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(element);
    geocoder = new google.maps.Geocoder();
    
    
}

function codeAddress() {
    var address = document.getElementById("address").value;
    if(marker) marker.setMap(null);
    geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location
                    });
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });
}


function unload(){
    try{
        radar.setMap(null);
        radar = null;
    }catch(e){
    }
}
    
