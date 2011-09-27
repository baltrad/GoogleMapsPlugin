// create ajax http request
// ----------------------------------------------
function createXmlHttpRequestObject(){
  var xmlHttp;
  try{
    xmlHttp = new XMLHttpRequest();
  } catch(e) {
    var XmlHttpVersions = new Array("MSXML2.XMLHTTP.6.0","MSXML2.XMLHTTP.5.0","MSXML2.XMLHTTP.4.0","MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP");

    for (var i=0; i<XmlHttpVersions.length && !xmlHttp; i++) {
      try{
        xmlHttp = new ActiveXObject(XmlHttpVersions[i]);
      } catch (e) { }
	}
  }

  if (!xmlHttp) {
    alert("Error creating the XMLHttpRequest object.");
  } else {
    return xmlHttp;
  }
}

// ajax request processing
// ----------------------------------------------
var xmlHttp_list = createXmlHttpRequestObject();

function request_radar_image_list()
{
  if (xmlHttp_list){
    try {
      var url=script_for_radar_image_list;
      url=url+"?nselect="+nselect+"&nload"+nload+"&datadate="+datadate+"&prd="+prd;
      xmlHttp_list.open("GET", url, true);
      xmlHttp_list.onreadystatechange = handle_radar_image_list;
      xmlHttp_list.send(null);
    } catch(e) {
      alert("Connection error - can't get list of images.");
    }
  }
}

// handle ajax answer
// ----------------------------------------------
function handle_radar_image_list() 
{
  if (xmlHttp_list.readyState == 4) {
    if (xmlHttp_list.status == 200) {
      response = xmlHttp_list.responseText;
      first_line = response.split("\n", 1)[0];
      response = response.substring(first_line.length);
      document.getElementById('div_radar_img_list').innerHTML=response;
      if(document.getElementById('radar_img_list').length == 0)
          {
              document.getElementById('radar_img_list').innerHTML = '<option value="-">Nothing loaded</option>';
          }
      else
          {
              document.getElementById('div_scl').innerHTML=first_line;
          }
      var time=new Date();
      var timestring=pad(time.getUTCFullYear())+"-"+pad(time.getUTCMonth()+1)+"-"+pad(time.getUTCDate())+" "+pad(time.getUTCHours())+":"+pad(time.getUTCMinutes())+":"+pad(time.getUTCSeconds())+" UTC";
      document.getElementById('div_update_info').innerHTML="Updated: "+timestring;

      load_radar_images();
      if ((timeout_id == null) && (loaded == 1)) {
        anim();
      }
    } else{
        document.getElementById('radar_img_list').innerHTML='<option value="-">Could not load</option>';
    }
  }
}

// -----------------------------------------------------------------------------------------------------------------------------------------------------------
function change_datadate() {
  var str = window.document.getElementById('datadate_txt').value;
  var re=/^\d{4}[-]?\d{1,2}[-]?\d{1,2} \d{1,2}:\d{1,2}$/;
  str = str.toString();
  if (!str.match(re)) {
    alert("Enter valid date (yyyy-mm-dd hh:mm or yyyymmdd hh:mm).");
    return false;
  } else {
    datadate = "";
    for (i=0; i<=str.length; i++) {
        if (str.charAt(i) != "-" && 
            str.charAt(i) != " " && 
            str.charAt(i) != ":") {
            datadate+=str.charAt(i);
        }
    }
    request_radar_image_list();
    change_update_time();
    return false;
  }
}

function change_colorbar() {
    //    request_radar_legend();
}

function change_prd() {
  var tmp = window.document.getElementById('prd').value;
  prd = tmp;
  change_center_boundary();
  request_radar_image_list();
  change_update_time();
  change_colorbar();
  map.panTo(new google.maps.LatLng(lat, lon));
  map.setZoom(zoom);
  map.zoomIn(new google.maps.LatLng(lat, lon), true, true);
  return false;
}

function change_center_boundary() {
  var p = radar_products[prd];
  lat = p.lat;
  lon = p.lon;
  zoom = p.zoom;
  nelat = p.nelat;
  nelon = p.nelon;
  swlat = p.swlat;
  swlon = p.swlon;
  ne = new google.maps.LatLng(nelat,nelon);
  sw = new google.maps.LatLng(swlat,swlon);
  boundaries = new google.maps.LatLngBounds(sw, ne);  
  map.panTo(new google.maps.LatLng(lat, lon));
  map.setZoom(zoom + 1);

  return false;
}

// refreshing of image list
function update_radar_image_list() {
  request_radar_image_list();
  change_colorbar();
  change_update_time();
}

function change_update_time() {
  update_time =  window.document.getElementById('update_time').options[window.document.getElementById('update_time').selectedIndex].value;
  if (update_time > 0){
    update_timeout_id = setTimeout("update_radar_image_list()",update_time);
  } else {
    if (update_timeout_id) {
      clearTimeout(update_timeout_id); 
      update_timeout_id=null;
    }	
  }
}

// changing opacity and animation speed
function change_opacity() {
  opacity=parseInt(document.getElementById('opacity').options[document.getElementById('opacity').selectedIndex].value);
  if (document.getElementById('show').checked == true && radar.div_) {
      radar.setOpacity(opacity); // Set radar layer transparency
  }
}

function toggle_opacity() {
  opacity = parseInt(document.getElementById('opacity').options[document.getElementById('opacity').selectedIndex].value);
  if (document.getElementById('show').checked == true) {
    radar.setOpacity(opacity);
  } else {
    radar.setOpacity(1);
  }
}


function change_rep_time() {
  rep_time =  parseInt(document.getElementById('rep_time').options[document.getElementById('rep_time').selectedIndex].value);
}

function change_add_time() {
  add_time =  parseInt(document.getElementById('add_time').options[document.getElementById('add_time').selectedIndex].value);
}

function loaded_info() {
  ++num_loaded;    
  document.getElementById('input_load').value = "Loaded: (" + num_loaded + " / " + (nselect) + ") images";
}

// loading images into memory
function load_radar_images() {
  loaded = 0;
  num_loaded=0;      
  // clear current images from memory
  for(var i=nselect-1; i>=0; i--) {
    delete images_rad[i]; 
    delete texts_time[i];
  }
	    
  // Load length of image list
  var total=document.getElementById('radar_img_list').options.length;

  nselect=0;   
  for(var i=0; i <=total-1; i++) {
    if(document.getElementById('radar_img_list').options[i].selected) {
      nselect++;
    }
  }
  
  // Clear 
  document.getElementById('input_load').value = "Loaded: (" + 0 + " / " + (nselect) + ") images";

  // Load picture into memory
  var pom_i=0;
  for(var i=total-1; i >=0; i--) {
    if (document.getElementById('radar_img_list').options[i].selected) {    
      var parts=document.getElementById('radar_img_list').options[i].value.split(";");
      images_rad[pom_i] = new Image();
      images_rad[pom_i].onload = loaded_info;
      images_rad[pom_i].src=parts[1];
      texts_time[pom_i]=parts[0];			
      pom_i++;
    }
  }
	    
  loaded = 1;
  last();
}
	
function anim() {
  frame = (frame +1)% nselect;
  change_radar();

  var total_time=0; 
  total_time=rep_time;
  //if (frame == 0) total_time=add_time+rep_time;
  //BUGFIX: Pause on last image not the first
  if (frame == nselect-1) {
    total_time=add_time+rep_time;
  }
  timeout_id = setTimeout("anim()",total_time);
}

function next() {
  if ((timeout_id) && (loaded == 1)) {
    clearTimeout(timeout_id); 
    timeout_id=null;
  }	
  frame = (frame +1)% nselect;
  change_radar();
}

function previous() {
  if ((timeout_id) && (loaded == 1)) {
    clearTimeout(timeout_id); 
    timeout_id=null;
  }
  frame = (frame -1)% nselect;
  if (frame < 0 ) {
    frame = nselect-1;
  }
  change_radar();
}

function first() {
  if ((timeout_id) && (loaded == 1)) {
    clearTimeout(timeout_id); 
    timeout_id=null;
  }
  frame = 0;	
  change_radar();
}

function last() {
  if ((timeout_id) && (loaded == 1)) {
    clearTimeout(timeout_id); 
    timeout_id=null;
  }	
  frame = nselect-1;	
  change_radar();
}	

function pad (val, len) {
  val = String(val);
  len = len || 2;
  while (val.length < len) {
    val = "0" + val;
  }
  return val;
}

/*
  Return the ISO 8601 datestring for the UTC time.
 */
function ISODateString_UTC(d){
    return d.getUTCFullYear()+'-'
        + pad(d.getUTCMonth()+1)+'-'
        + pad(d.getUTCDate())+' '
        + pad(d.getUTCHours())+':'
        + pad(d.getUTCMinutes())+'Z'}

/*
  Return the ISO string for the timezone time difference.
  Eg: +03:30, -02:00
*/
function ISOTimeDifference(offset){
    var hours = 0;
    var minutes = 0;
    var sign = "";
    if(offset > 0) {
        sign = "+";
    } else {
        sign = "-";
        offset = -offset;
    }
    hours = Math.floor(offset / 60);
    minutes = offset % 60;
    return sign + pad(hours) + ":" +  pad(minutes);}

/*
  Return the ISO 8601 datestring for the local time.
 */
function ISODateString_Locale(d){
    var offset = -d.getTimezoneOffset();
    return d.getFullYear()+'-'
        + pad(d.getMonth()+1)+'-'
        + pad(d.getDate())+' '
        + pad(d.getHours())+':'
        + pad(d.getMinutes())+
        ISOTimeDifference(offset)}

function change_radar(){
  if(!texts_time || !texts_time[frame]) return;
  var year=texts_time[frame].substr(0,4)*1;	
  var month=texts_time[frame].substr(4,2)*1;
  var day=texts_time[frame].substr(6,2)*1;
  var hour=texts_time[frame].substr(8,2)*1;	
  var minute=texts_time[frame].substr(10,2)*1;
    
  var time=new Date(Date.UTC(year,month-1,day,hour,minute));
  var timestring=ISODateString_UTC(time);
  document.getElementById('span_title_time_utc').innerHTML=timestring;		// UTC time

  timestring=ISODateString_Locale(time);
  document.getElementById('span_title_time_local').innerHTML=timestring;	// LOCAL time

  if(!radar) {
     radar = new ProjectedOverlay(map, images_rad[frame].src, boundaries, {id: "radar_img"});
  }

  var img = document.getElementById('radar_img');
  if (img) {
      img.src = radar.url_ = images_rad[frame].src;
  }
  if (document.getElementById('show').checked == true) {
      radar.setOpacity(opacity); // Set radar layer transparency
  } else {
      radar.setOpacity(1);
  }
}

// functions to save current settings to cookies or bookmark
// ----------------------------------------------
function set_cookie(name, value, expire) {
  document.cookie = name + "=" + escape(value) + ((expire == null) ? "" : ("; expires=" + expire.toGMTString()))
}

function currentMapTypeNumber(map){ 
  var type=-1; 
  mapTypes = google.maps.MapTypeId;
  for(var ix=0;ix<mapTypes.length;ix++){
    if(mapTypes[ix]==map.getMapTypeId()) type=ix; 
  } 
  return type; 
} 

function dirname(path) {
  return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');
}

function basename(path) {
  return path.replace(/\\/g,'/').replace( /.*\//, '' );
}
  
function save_cookies(){
  var ted = new Date();
  var expires = new Date();
		
  expires.setTime(ted.getTime() + 50*365*86400*1000); //50let * pocet dni do roka* pocet sekund za den * prevod na milisekundy
  set_cookie("radar_gmap[lat]", Math.round(map.getCenter().lat()*10000)/10000, expires);
  set_cookie("radar_gmap[lon]", Math.round(parent.map.getCenter().lng()*10000)/10000, expires);
  set_cookie("radar_gmap[zoom]", map.getZoom(), expires);
  set_cookie("radar_gmap[rep]", document.getElementById('rep_time').selectedIndex, expires);
  set_cookie("radar_gmap[add]", document.getElementById('add_time').selectedIndex, expires);
  set_cookie("radar_gmap[update]", document.getElementById('update_time').selectedIndex, expires);
  set_cookie("radar_gmap[opa]", document.getElementById('opacity').selectedIndex, expires);
  set_cookie("radar_gmap[maptype]", currentMapTypeNumber(map), expires);
  set_cookie("radar_gmap[nselect]", nselect, expires);
    
  alert("Your current settings was saved!!");
}

function clear_cookies(){
  var ted = new Date();
  var expires = new Date();
	
  expires.setTime(ted.getTime() - 50*365*86400*1000); //50let * pocet dni do roka* pocet sekund za den * prevod na milisekundy
  set_cookie("radar_gmap[lat]", Math.round(map.getCenter().lat()*10000)/10000, expires);
  set_cookie("radar_gmap[lon]", Math.round(parent.map.getCenter().lng()*10000)/10000, expires);
  set_cookie("radar_gmap[zoom]", map.getZoom(), expires);
  set_cookie("radar_gmap[rep]", document.getElementById('rep_time').selectedIndex, expires);
  set_cookie("radar_gmap[add]", document.getElementById('add_time').selectedIndex, expires);
  set_cookie("radar_gmap[update]", document.getElementById('update_time').selectedIndex, expires);
  set_cookie("radar_gmap[opa]", document.getElementById('opacity').selectedIndex, expires);
  set_cookie("radar_gmap[maptype]", currentMapTypeNumber(map), expires);
  set_cookie("radar_gmap[nselect]", nselect, expires);

  alert("Your current settings was cleared!!");
}

function save_bookmark(){
  var title="Radar data viewer using GoogleMaps"
  var page=dirname(document.location.href)+"/"+page_name+"?";
    
  page=page+"lat="+Math.round(map.getCenter().lat()*10000)/10000;
  page=page+"&lon="+Math.round(parent.map.getCenter().lng()*10000)/10000;
  page=page+"&zoom="+map.getZoom();
  page=page+"&rep="+document.getElementById('rep_time').selectedIndex;
  page=page+"&add="+document.getElementById('add_time').selectedIndex;
  page=page+"&update="+document.getElementById('update_time').selectedIndex;
  page=page+"&opa="+document.getElementById('opacity').selectedIndex;
  page=page+"&maptype="+currentMapTypeNumber(map);
  page=page+"&nselect="+nselect;
    
  if (window.sidebar) { // Mozilla Firefox
    window.sidebar.addPanel(title, page,"");
  } else {
    if (window.external) { // IE 
      window.external.AddFavorite( page, title); 
    } else {
      alert("It is not supported in your browser \n you can manually bookmark page: " +   page);
    }
  } 
}
