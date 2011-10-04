<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="cs">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="content-language" content="en_US" />

    <meta http-equiv="last-modified" content="<?php $last_modified_time=filemtime("./index.php") ; echo gmdate("D, d M Y H:i:s", $last_modified_time)." GMT";?>" />
    <meta http-equiv="pragma" content="no-cache, must-revalidate" />
    <meta http-equiv="cache-control" content="no-cache, must-revalidate" />
    <meta http-equiv="X-UA-Compatible" content="IE=9; IE=8" />
    <meta name="author" content="" />
    <meta name="robots" content="index,follow" />
    <meta name="description" content="BALTRAD Radar data viewer using Google Maps" />
    <meta name="keywords" content="radar,weather,precipitation" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <title>BALTRAD Google Maps Viewer</title>

    <!-- Scripts -->
    <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script>    <script src="js/gmap_overlay.js" type="text/javascript"></script>
    <script src="js/datetimepicker_css.js"></script>
    <!-- This script needs to be generated prior usage -->
    <script src="./products.js" type="text/javascript"></script>

    <script type="text/javascript">
      // definition of the startup values (highest priority has webpage parametrs (GET method), 
      // then value stored in Cookies and then default value defined here      
            	    
      // repetition time = animation speed (index in the option list)
	  <?php 
	    if(isset($_GET["rep"])){
	      echo "var rep='".$_GET["rep"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["rep"])) {
	        echo "var rep='".$_COOKIE["radar_gmap"]["rep"]."';\n";
	      } else {
	        echo "var rep='1';\n";
	      }
	    }
	  ?>
	    
      // additional waiting time for last image in the animation (index in the option list)
	  <?php 
	    if(isset($_GET["add"])){
	      echo "var add='".$_GET["add"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["add"])){
	        echo "var add='".$_COOKIE["radar_gmap"]["add"]."';\n";
	      } else {
	        echo "var add='4';\n";
	      }
	    }
	  ?>
	    
      // latitude of the center of the map
	  <?php 
	    if(isset($_GET["lat"])){
	      echo "var lat='".$_GET["lat"]."';\n";
	    } else {
	      if($_COOKIE["radar_gmap"]["lat"]){
	        echo "var lat='".$_COOKIE["radar_gmap"]["lat"]."';\n";
	      } else {
	        //echo "var lat='56.0';\n";
	        echo "var lat=radar_products[radar_option_list[0]].lat;\n";
	      }
	    }
	  ?>
	    
      // longitude of the center of the map
	  <?php
	    if(isset($_GET["lon"])){
	      echo "var lon='".$_GET["lon"]."';\n";
	    } else {
	      if($_COOKIE["radar_gmap"]["lon"]){
	        echo "var lon='".$_COOKIE["radar_gmap"]["lon"]."';\n";
	      } else {
	        //echo "var lon='12.0';\n";
	        echo "var lon=radar_products[radar_option_list[0]].lon;\n";
	      }
	    }
	  ?>
	    
      // zoom level
	  <?php 
	    if(isset($_GET["zoom"])){
	      echo "var zoom='".$_GET["zoom"]."';\n";
	    } else {
	      if($_COOKIE["radar_gmap"]["zoom"]){
	        echo "var zoom='".$_COOKIE["radar_gmap"]["zoom"]."';\n";
	      } else {
	        //echo "var zoom='6';\n";
	        echo "var zoom=radar_products[radar_option_list[0]].zoom;\n";
	      }
	    }
	  ?>
	    
      // radar image opacity (index in the option list)
	  <?php
	    if(isset($_GET["opa"])){
	      echo "var opa='".$_GET["opa"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["opa"])){
	        echo "var opa='".$_COOKIE["radar_gmap"]["opa"]."';\n";
	      } else {
	        echo "var opa='4';\n";
	      }
	    }
	  ?>

      // map type to be displayed
	  <?php
	    if(isset($_GET["maptype"])){
	      echo "var maptype='".$_GET["maptype"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["maptype"])){
	        echo "var maptype='".$_COOKIE["radar_gmap"]["maptype"]."';\n";
	      } else {
	        echo "var maptype=google.maps.MapTypeId.TERRAIN;\n";
	      }
	    }
	  ?>

      // update time of radar image list (index in the option list)
	  <?php
	    if(isset($_GET["update"])){
	      echo "var update='".$_GET["update"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["update"])) {
	        echo "var update='".$_COOKIE["radar_gmap"]["update"]."';\n";
	      } else {
	        echo "var update='0';\n";
	      }
	    }
	  ?>

      // number of image to be selected in radar image list
	  <?php
	    if(isset($_GET["nselect"])){
	      echo "var nselect='".$_GET["nselect"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["nselect"])){
	        echo "var nselect='".$_COOKIE["radar_gmap"]["nselect"]."';\n";
	      } else {
	        echo "var nselect='24';\n";
	      }
	    }
	  ?>

      // number of image to be loaded into the radar image list
	  <?php
	    if(isset($_GET["nload"])){
	      echo "var nload='".$_GET["nload"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["nload"])){
	        echo "var nload='".$_COOKIE["radar_gmap"]["nload"]."';\n";
	      } else {
	        echo "var nload='999';\n";
	      }
	    }
	  ?>

      // Product
	  <?php
	    if(isset($_GET["prd"])){
	      echo "var prd='".$_GET["prd"]."';\n";
	    } else {
	      if(isset($_COOKIE["radar_gmap"]["prd"])){
	        echo "var prd='".$_COOKIE["radar_gmap"]["prd"]."';\n";
	      } else {
	        echo "var prd=radar_option_list[0];\n";
	      }
	    }
	  ?>

      // date of data
	  <?php if(isset($_GET["datadate"])){echo "var datadate='".$_GET["datadate"]."';\n";}else{echo "var datadate='".gmdate("YmdHi")."';\n";}?>

      //user-defined variables:
      
      // name of this page (needed for correct bookmarking)
      var page_name='index.php'
  
      // name of radar images
      //var title_string_name='EUMETNET-OPERA Radar Composite: ';
      //var title_string_name='BALTRAD Radar Composite: ';
      var title_string_name='';

      // copyright info
      //var title_string_copyright='(c): <a target="_blank" href="http://www.knmi.nl/opera/">EUMETNET-OPERA participants</a>';
      //var title_string_copyright='&copy; <a target="_blank" href="http://baltrad.eu/">BALTRAD participants</a>';
      var title_string_copyright='';

      // name of script that makes list of radar images  
      var script_for_radar_image_list='list_data.php';

      // radar image boundaries - outer edges of corner pixels
      //var ne = new google.maps.LatLng(69.800,32.694);
      //var sw = new google.maps.LatLng(35.417,-12.028);
      var nelat = radar_products[radar_option_list[0]].nelat;
      var nelon = radar_products[radar_option_list[0]].nelon;
      var swlat = radar_products[radar_option_list[0]].swlat;
      var swlon = radar_products[radar_option_list[0]].swlon;
      var ne = new google.maps.LatLng(nelat,nelon);
      var sw = new google.maps.LatLng(swlat,swlon);
      var boundaries = new google.maps.LatLngBounds(sw, ne);  

      //  minimum scale of map
      var minMapScale = 4;
      //  maximum scale of map
      var maxMapScale = 11;
      // maxMapScale should be smaller for MSIE, since it is not able display so big image      
      if(navigator.userAgent.toLowerCase().indexOf("msie") != -1) {
        maxMapScale = 9;
      }	
      // maxMapScale should be smaller for OPERA, since it is not able display so big image
      //if(navigator.userAgent.toLowerCase().indexOf("opers") != -1) {      
      if(navigator.userAgent.toLowerCase().indexOf("opera") != -1) {
        maxMapScale = 10;
      }
      
      // Called when window loads. A bit more controlled and we don't
      // need to rely if body.onload is called before head initialization
      //
      function doloadwindow() {
        initialize();
      }
      window.onload=doloadwindow;
    </script>

    <script src="./js/init.js" type="text/javascript"></script>
    <script src="./js/radar.js" type="text/javascript"></script>
 		
    <!-- Styles -->
	<link rel="stylesheet" href="./css/gsearch.css" type="text/css" />
	<link rel="stylesheet" href="./css/gmlocalsearch.css" type="text/css" />
	<link rel="stylesheet" href="./css/radar.css" type="text/css" />

    <!-- Favicon -->
	<link rel="shortcut icon" href="./img/favicon.ico" />
	
  </head>
  
  <!--onload="initialize();" -->
    <body onunload="unload();">
    <!-- content visible during loading of application -->
    <div id="loading">
	<div class="centered">
	    <img src='./img/loading.gif' alt="" /><br />
	    Loading application, please wait ...
	</div>
    </div>    

    <!-- content visible when application is loaded-->
    <div id="loaded">
    <div id="map">
        If this text does not disappear quickly, then your browser does not
        support Google Maps API.</div>


    <!-- box with title image dates and copuright-->
    <div id="div_title">
      &nbsp; &nbsp;<a href="http://baltrad.eu/" title="BALTRAD - baltrad.eu" onclick="window.open(this.href); return false;"><img src="./img/BALTRAD-logo-small128.png" alt="BALTRAD - baltrad.eu" /></a><br/>
      <span id="span_title_name"></span>
      <span id="span_title_time_utc">&nbsp;</span><br/>
      <span id="span_title_time_local">&nbsp;</span><br/>
      <div id="div_title_copy">&nbsp;</div>
    </div>

  <div id="search_location">
    <input id="address" type="textbox" value="">
    <input type="button" value="Search" onclick="codeAddress()">
  </div>

  <div id="div_scl">
    <img src="./img/scl.png">
    </div>

  <div id="div_controls">
    <div id="div_update_info">Updated: </div>

    <div id="div_setdatadate">
               <form name="datadate" onsubmit="return false"><input type="text" size="19" name='datadate_field' id="datadate_txt" onchange="return change_datadate()" onclick="javascript:NewCssCal ('datadate_txt','yyyyMMdd','arrow',true,'24'); return false;">
    </div>

	<div id="div_setprd">
	  <form name="prd">
	    <select name="prd" id="prd" onsubmit="return false" onchange="return change_prd()">
<!--
          This list is generated dynamically from the radar option list	    
	      <option value="swegmaps_2000">SMHI Composite</option>
	      <option value='ekxv.baltrad'>BALTRAD HMC Virring</option>
	      <option value='mosaic.smhi'>SMHI Composite</option>
	      <option value='mosaic.dmi' selected>DMI Composite</option>
	      <option value='ekrn.dmi'>DMI Bornholm</option>
	      <option value='eksn.dmi'>DMI Sindal</option>
	      <option value='ekxr.dmi'>DMI Romo</option>
	      <option value='ekxs.dmi'>DMI Stevns</option>
	      <option value='ekxv.dmi'>DMI Virring</option>
-->	      
	    </select>
	    
	  </div>
	  
      <script type="text/javascript">
        // add options to product list dynamically
        for (var i = 0; i < radar_option_list.length; i++) {
          var key = radar_option_list[i];
          var prod = radar_products[key];
          var optn = document.createElement("OPTION");
          optn.text = prod.description;
          optn.value = key;
          var s = document.getElementById('prd');
          s.options[s.options.length] = optn;
        }
      </script>
      
      <div id="div_update">
      Update image list
      <input type="button" value="now" onclick="update_radar_image_list()" />
      <br/>       
        Update every 
        <select id="update_time" onchange="change_update_time()">
  				<option value="-999">no</option>
  				<option value="60000">1 min</option>
  				<option value="120000">2 min</option>
  				<option value="300000">5 min</option>
			        <option value="600000">10 min</option>
        </select>
	    </div>
  
	    <div id="div_radar_img_list">
		<select id="radar_img_list" multiple="multiple" size="10">
		    <option value="-">LOADING...</option>
		</select>
	    </div>

	    <div id="div_control_panel">
	      <input type="button" id="input_load" onclick="if (loaded == 1) load_radar_images();" /><br/>
	      &nbsp;<br/>
		  <table style="position:relative; margin: 0 auto;"><tr><td>
       <input type="button" id="input_first" value="|<" onclick="first();" /></td><td>
       <input type="button" id="input_previous" value=" < " onclick="previous();" /></td><td>
       <input type="button" id="input_play" value=">>" onclick="if (timeout_id == null) anim();" /></td><td>
       <input type="button" id="input_pause" value=" | | " onclick="if (timeout_id) { clearTimeout(timeout_id); timeout_id=null; }" /></td><td>
       <input type="button" id="input_next" value=" > " onclick="next();" /></td><td>
       <input type="button" id="input_last" value=">|" onclick="last();" /></td>
      </tr></table><br/>

		<table style="position:relative; margin: 0 auto;">
		<tr>
			<td align='right'>anim. speed:&nbsp;</td>
			<td align='left'>			
        <select id="rep_time" onchange="change_rep_time();">
				  <option value="250">250 ms</option>
				  <option value="500">500 ms</option>
				  <option value="750">750 ms</option>
				  <option value="1000">1 s</option>
				  <option value="2000">2 s</option>
				  <option value="5000">5 s</option>
        </select>
			</td>
		</tr>
		<tr>
			<td align='right'>last image:&nbsp;</td>
			<td align='left'>
        <select id="add_time" onchange="change_add_time();">
				  <option value="250">+250 ms</option>
				  <option value="500">+500 ms</option>
				  <option value="750">+750 ms</option>
				  <option value="1000">+1 s</option>
				  <option value="2000">+2 s</option>
				  <option value="5000">+5 s</option>
				  <option value="10000">+10 s</option>
    		</select>
      </td>
		</tr>
		<tr>
			<td align='right'>opacity:&nbsp;</td>
      <td align='left'>
        <select id="opacity" onchange="change_opacity();">
				  <option value="100">100%</option>
				  <option value="90">90%</option>
				  <option value="80">80%</option>
				  <option value="70">70%</option>
				  <option value="60">60%</option>
				  <option value="50">50%</option>
				  <option value="40">40%</option>
				  <option value="30">30%</option>
				  <option value="20">20%</option>
				  <option value="10">10%</option>
				  <option value="1">0%</option>
				  <!-- value is 1 because 0 does not work -->
        </select></td>
		</tr>
		<tr>
			<td align='right'>show:&nbsp;</td>
      <td align='left'>
	<form>
	  <input checked="yes" type="checkbox" name="show" id="show" onchange="toggle_opacity();"><br/>
	</form>
	</td>
		</tr>
		</table><br/>
		
	  Current settings:
    <input type="button" id="save_bookmark" onclick="save_bookmark();" value="save as bookmark"/><br/>    
    <input type="button" id="save_cookies" onclick="save_cookies();" value="save into cookies"/>
	  <input type="button" id="clear_cookies" onclick="clear_cookies();" value="clear"/><br/>

	  </div>

    </div>

<!--
  <div id="div_about">
  <table style="position:relative; margin: 0 auto;"><tr><td align='right'>
  <a href="http://baltrad.eu/" title="BALTRAD - baltrad.eu" onclick="window.open(this.href); return false;">
  <img src="./img/BALTRAD-logo-small128.png" alt="BALTRAD - baltrad.eu" /></a>
  </td>
  <td align='center' style="padding-bottom:6px;">BALTRAD&mdash;an advanced<br/>weather radar network<br/>for the Baltic Sea region</td>
  <td align='center'></td></tr></table>
  </div>
  -->

    </div>
   
  </body>
</html>
