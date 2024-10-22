
// name of this page (needed for correct bookmarking)
var page_name='index.html'

// name of radar images
//var title_string_name='EUMETNET-OPERA Radar Composite: ';
//var title_string_name='BALTRAD Radar Composite: ';
var title_string_name='';

// copyright info
//var title_string_copyright='(c): <a target="_blank" href="http://www.knmi.nl/opera/">EUMETNET-OPERA participants</a>';
//var title_string_copyright='&copy; <a target="_blank" href="http://baltrad.eu/">BALTRAD Partnership</a>';
var title_string_copyright='';

// name of script that makes list of radar images  
var script_for_radar_image_list='list_data.php';

var rep='1';
var add='4';
var lat=radar_products[radar_option_list[0]].lat;
var lon=radar_products[radar_option_list[0]].lon;
var zoom=parseInt(radar_products[radar_option_list[0]].zoom);
var opa='4';
var update='0';
var nselect='24';
var nload='999';
var prd=radar_option_list[0];
var qind='qvoid';
var datadate='".gmdate("YmdHi")."';

var radar = null;
var boundaries = null;
var qualityLayer = null;

let productInfo;
let product_provider_baseurls;
let odimSource;
$(document).ready( function(){
	loadCookieSettings();
	initViewer();
	initialize();
});

function loadCookieSettings() {
	lat = getCookie("radar_gmap[lat]");
	if (lat == "") {
		lat=radar_products[radar_option_list[0]].lat;
	}
	
	lon = getCookie("radar_gmap[lon]");
	if (lon == "") {
		lon=radar_products[radar_option_list[0]].lon;
	}
	
	zoom = parseInt(getCookie("radar_gmap[zoom]"));
	if (isNaN(zoom)) {
		zoom=parseInt(radar_products[radar_option_list[0]].zoom);
	}
	
	rep = getCookie("radar_gmap[rep]");
	if (rep == "") {
		rep='1';
	}
	
	add = getCookie("radar_gmap[add]");
	if (add == "") {
		add='1';
	}
	
	update = getCookie("radar_gmap[update]");
	if (update == "") {
		update='0';
	}
	
	opa = getCookie("radar_gmap[opa]");
	if (opa == "") {
		opa='4';
	}
	
	nselect = getCookie("radar_gmap[nselect]");
	if (nselect == "") {
		nselect='24';
	}
	
	qind = getCookie("radar_gmap[qind]");
	if (qind == "") {
		qind='qvoid';
	}
	$("#qind").val(qind).change();
}

function initViewer() {
    // radar image boundaries - outer edges of corner pixels
    var nelat = radar_products[radar_option_list[0]].nelat;
    var nelon = radar_products[radar_option_list[0]].nelon;
    var swlat = radar_products[radar_option_list[0]].swlat;
    var swlon = radar_products[radar_option_list[0]].swlon;
    var ne = new L.latLng(nelat,nelon);
    var sw = new L.latLng(swlat,swlon);
    boundaries = new L.latLngBounds(sw, ne); 
}

//create ajax http request
//----------------------------------------------
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

//ajax request processing
//----------------------------------------------
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

//handle ajax answer
//----------------------------------------------
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
			var timestring=pad(time.getUTCFullYear())+"-"+pad(time.getUTCMonth()+1)+"-"+pad(time.getUTCDate())+" "+pad(time.getUTCHours())+":"+pad(time.getUTCMinutes())+":"+pad(time.getUTCSeconds())+"Z";
			document.getElementById('div_update_info').innerHTML="Updated:<br />"+timestring;
			load_radar_images();
		} else{
			document.getElementById('radar_img_list').innerHTML='<option value="-">Could not load</option>';
		}
	}
}

//-----------------------------------------------------------------------------------------------------------------------------------------------------------
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
	is_anim = timeout_id;
	stop();
	change_center_boundary();
	request_radar_image_list();
	
	map.removeLayer(radar);
	radar = null;
	var imageOverlayOptions = {className : "radar_img"}
	radar = L.imageOverlay("", boundaries, imageOverlayOptions).addTo(map);
	radar.bringToFront();
	
	map.removeLayer(qualityLayer);
	qualityLayer = null;
	var imageOverlayOptions = {className : "quality_img"}
	qualityLayer = L.imageOverlay("", boundaries, imageOverlayOptions).addTo(map);
	qualityLayer.bringToBack();
	
	change_update_time();
	map.panTo(new L.latLng(lat, lon));
	map.setZoom(zoom + 1);
	toggle_quality();
	if(is_anim)
	{
		anim();
	}
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
	ne = new L.latLng(nelat,nelon);
	sw = new L.latLng(swlat,swlon);
	boundaries = new L.latLngBounds(sw, ne);  
	map.panTo(new L.latLng(lat, lon));
	map.setZoom(zoom + 1);

	return false;
}

//refreshing of image list
function update_radar_image_list() {
	now = new Date();
	window.document.getElementById('datadate_txt').value = '';
	datadate = now.getUTCFullYear()+""
	+ pad(now.getUTCMonth()+1)+''
	+ pad(now.getUTCDate())+''
	+ pad(now.getUTCHours())+''
	+ pad(now.getUTCMinutes());

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

//changing opacity and animation speed
function change_opacity() {
	opacity=parseInt(document.getElementById('opacity').options[document.getElementById('opacity').selectedIndex].value);
	if (document.getElementById('show').checked == true && radar) {
		radar.setOpacity(opacity / 100.0); // Set radar layer transparency
	}
}

function toggle_opacity() {
	opacity = parseInt(document.getElementById('opacity').options[document.getElementById('opacity').selectedIndex].value);
	if (document.getElementById('show').checked == true) {
		radar.setOpacity(opacity / 100.0);
	} else {
		radar.setOpacity(0);
	}
}

function toggle_quality() {
	quality = document.getElementById('qind').options[document.getElementById('qind').selectedIndex].value;
	change_radar();
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

function basename(path) {
	return path.replace(/\\/g,'/').replace( /.*\//, '' );
}

function dirname(path) {
	return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');;
}


//loading images into memory
function load_radar_images() {
	loaded = 0;
	num_loaded=0;      

//	clear current images from memory
	for(var i=nselect-1; i>=0; i--) {
		delete images_rad[i]; 
		delete texts_time[i];
	}

//	Load length of image list
	var total=document.getElementById('radar_img_list').options.length;

	nselect=0;   
	for(var i=0; i <=total-1; i++) {
		if(document.getElementById('radar_img_list').options[i].selected) {
			nselect++;
		}
	}

//	Clear 
	document.getElementById('input_load').value = "Loaded: (" + 0 + " / " + (nselect) + ") images";

//	Load picture into memory
	var pom_i=0;
	for(var i=total-1; i >=0; i--) {
		if (document.getElementById('radar_img_list').options[i].selected) {    
			var parts=document.getElementById('radar_img_list').options[i].value.split(";");
			images_rad[pom_i] = new Image();
			images_rad[pom_i].onload = loaded_info;
			images_rad[pom_i].src = parts[1];
			images_qual["qblock"][pom_i] = new Image();
			images_qual["qblock"][pom_i].src = dirname(parts[1]) + "/se.smhi.detector.beamblockage/" + parts[0] + ".png";
			images_qual["qanom"][pom_i] = new Image();
			images_qual["qanom"][pom_i].src = dirname(parts[1]) + "/fi.fmi.ropo.detector.classification/" + parts[0] + ".png";
			images_qual["pover"][pom_i] = new Image();
			images_qual["pover"][pom_i].src = dirname(parts[1]) + "/se.smhi.detector.poo/" + parts[0] + ".png";
			texts_time[pom_i] = parts[0];			
			pom_i++;
		}
	}
	loaded = 1;
	anim();
}

function anim() {
	if(loaded == 0 || nselect == 0) return;
	stop();
	frame = (frame +1)% nselect;
	change_radar();

	var total_time=0; 
	total_time=rep_time;
//	if (frame == 0) total_time=add_time+rep_time;
//	BUGFIX: Pause on last image not the first
	if (frame == nselect-1) {
		total_time=add_time+rep_time;
	}
	timeout_id = setTimeout("anim()",total_time);
}

function stop() {
	if (timeout_id) {
		clearTimeout(timeout_id); 
		timeout_id=null;
	}	
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
		var imageOverlayOptions = {className : "radar_img"}
		radar = L.imageOverlay(images_rad[frame].src, boundaries, imageOverlayOptions).addTo(map);
		radar.bringToFront();
	}
	
	if(!qualityLayer && quality != "qvoid") {
		var imageOverlayOptions = {className : "quality_img"}
		qualityLayer = L.imageOverlay(images_qual[quality][frame].src, boundaries, imageOverlayOptions).addTo(map);
		qualityLayer.bringToBack();
	} else if (qualityLayer && quality == "qvoid") {
		map.removeLayer(qualityLayer);
		qualityLayer = null;
	}
	
	radar.setUrl(images_rad[frame].src);

	if (quality != "qvoid") {
		qualityLayer.setUrl(images_qual[quality][frame].src);
		qualityLayer.setOpacity(0.65);
	}

	if (document.getElementById('show').checked == true) {
		radar.setOpacity(opacity / 100.0); // Set radar layer transparency
	} else {
		radar.setOpacity(0);
	}
}

//functions to save current settings to cookies or bookmark
//----------------------------------------------
function set_cookie(name, value, expire) {
	document.cookie = name + "=" + escape(value) + ((expire == null) ? "" : ("; expires=" + expire.toGMTString()))
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
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

	set_cookie("radar_gmap[lat]", Math.round(map.getCenter().lat*10000)/10000, expires);
	set_cookie("radar_gmap[lon]", Math.round(parent.map.getCenter().lng*10000)/10000, expires);
	set_cookie("radar_gmap[zoom]", map.getZoom(), expires);
	set_cookie("radar_gmap[rep]", document.getElementById('rep_time').selectedIndex, expires);
	set_cookie("radar_gmap[add]", document.getElementById('add_time').selectedIndex, expires);
	set_cookie("radar_gmap[update]", document.getElementById('update_time').selectedIndex, expires);
	set_cookie("radar_gmap[opa]", document.getElementById('opacity').selectedIndex, expires);
	set_cookie("radar_gmap[nselect]", nselect, expires);
	set_cookie("radar_gmap[qind]", quality, expires);
	alert("Your current settings was saved!!");
}

function clear_cookies(){
	var ted = new Date();
	var expires = new Date();

	expires.setTime(ted.getTime() - 50*365*86400*1000); //50let * pocet dni do roka* pocet sekund za den * prevod na milisekundy

	set_cookie("radar_gmap[lat]", Math.round(map.getCenter().lat*10000)/10000, expires);
	set_cookie("radar_gmap[lon]", Math.round(parent.map.getCenter().lng*10000)/10000, expires);
	set_cookie("radar_gmap[zoom]", map.getZoom(), expires);
	set_cookie("radar_gmap[rep]", document.getElementById('rep_time').selectedIndex, expires);
	set_cookie("radar_gmap[add]", document.getElementById('add_time').selectedIndex, expires);
	set_cookie("radar_gmap[update]", document.getElementById('update_time').selectedIndex, expires);
	set_cookie("radar_gmap[opa]", document.getElementById('opacity').selectedIndex, expires);
	set_cookie("radar_gmap[nselect]", nselect, expires);
	set_cookie("radar_gmap[qind]", quality, expires);

	alert("Your current settings was cleared!!");
}

function save_bookmark(){
	var title="Radar data viewer using GoogleMaps"
		var page=dirname(document.location.href)+"/"+page_name+"?";

	page=page+"lat="+Math.round(map.getCenter().lat*10000)/10000;
	page=page+"&lon="+Math.round(parent.map.getCenter().lng*10000)/10000;
	page=page+"&zoom="+map.getZoom();
	page=page+"&rep="+document.getElementById('rep_time').selectedIndex;
	page=page+"&add="+document.getElementById('add_time').selectedIndex;
	page=page+"&update="+document.getElementById('update_time').selectedIndex;
	page=page+"&opa="+document.getElementById('opacity').selectedIndex;
	page=page+"&nselect="+nselect;
	page=page+"&qind="+quality;

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
