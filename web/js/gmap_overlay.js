// Create an overlay on the map from a projected image - Maps v3...
// Author. John D. Coryat 05/2009 USNaviguide LLC - http://www.usnaviguide.com
// Thanks go to Mile Williams EInsert: http://econym.googlepages.com/einsert.js, Google's GOverlay Example and Bratliff's suggestion...
// Opacity code from TPhoto: http://gmaps.tommangan.us/addtphoto.html
// Modified by Bernat Puigdomenech: http://www.radar.mcgill.ca

// This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License 
// as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

function ProjectedOverlay(map, imageUrl, bounds, opts)
{
 google.maps.OverlayView.call(this);

 this.map_ = map;
 this.url_ = imageUrl ;
 this.bounds_ = bounds ;
 this.addZ_ = opts.addZoom || '' ;				// Add the zoom to the image as a parameter
 this.id_ = opts.id || this.url_ ;				// Added to allow for multiple images
 this.percentOpacity_ = opts.percentOpacity || 60 ;
 this.div_ = null;
 this.setMap(map);
}

ProjectedOverlay.prototype = new google.maps.OverlayView();

ProjectedOverlay.prototype.createElement = function()
{
 var panes = this.getPanes() ;
 var div = this.div_ ;

 if (!div)
 {
  div = document.createElement("div");
  div.style.position = "absolute" ;
  var img = document.createElement("img");		
  img.setAttribute('id',this.id_);			
  div.appendChild(img);
  this.div_ = div ;
  this.lastZoom_ = -1 ;
  if( this.percentOpacity_ )
  {
   this.setOpacity(this.percentOpacity_) ;
  }
  panes.overlayLayer.appendChild(div);
 }
}

// Remove the main DIV from the map pane

ProjectedOverlay.prototype.remove = function()
{
 if (this.div_) 
 {
  this.setMap(null);
  this.div_.parentNode.removeChild(this.div_);
  this.div_ = null;
 }
}

// Redraw based on the current projection and zoom level...

ProjectedOverlay.prototype.draw = function(firstTime)
{
 // Creates the element if it doesn't exist already.

 this.createElement();

 if (!this.div_)
 {
  return ;
 }

 var c1 = this.get('projection').fromLatLngToDivPixel(this.bounds_.getSouthWest());
 var c2 = this.get('projection').fromLatLngToDivPixel(this.bounds_.getNorthEast());

 if (!c1 || !c2) return;

 // Now position our DIV based on the DIV coordinates of our bounds

 this.div_.style.width = Math.abs(c2.x - c1.x) + "px";
 this.div_.style.height = Math.abs(c2.y - c1.y) + "px";
 this.div_.style.left = Math.min(c2.x, c1.x) + "px";
 this.div_.style.top = Math.min(c2.y, c1.y) + "px";

 // Do the rest only if the zoom has changed...
 
 if ( this.lastZoom_ == this.map_.getZoom() )
 {
  return ;
 }

 this.lastZoom_ = this.map_.getZoom() ;

 var url = this.url_ ;

 if ( this.addZ_ )
 {
  url += this.addZ_ + this.map_.getZoom() ;
 }
 var img = document.getElementById(this.id_);
 
 if (img.src != url) img.setAttribute('src',url);

 img.setAttribute('width',this.div_.style.width);
 img.setAttribute('height',this.div_.style.height);	
}

ProjectedOverlay.prototype.setOpacity=function(opacity)
{
 if (opacity < 0)
 {
  opacity = 0 ;
 }
 if(opacity > 100)
 {
  opacity = 100 ;
 }
 var c = opacity/100 ;

 if (typeof(this.div_.style.filter) =='string')
 {
  this.div_.style.filter = 'alpha(opacity:' + opacity + ')' ;
 }
 if (typeof(this.div_.style.KHTMLOpacity) == 'string' )
 {
  this.div_.style.KHTMLOpacity = c ;
 }
 if (typeof(this.div_.style.MozOpacity) == 'string')
 {
  this.div_.style.MozOpacity = c ;
 }
 if (typeof(this.div_.style.opacity) == 'string')
 {
  this.div_.style.opacity = c ;
 }
}

