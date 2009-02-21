import cgi

def xspf_xml(context):
	return """<playlist version="0">
  <title>m1xes/sub-pop-mix-1</title>
  <creator>Shrub</creator>
  <info>http://shrub.appspot.com</info>
  <location>http://s3.amazonaws.com/m1xes?delimiter=%2F&prefix=sub-pop-mix-1%2F</location>
  <trackList>
    <track>
      <location>http://s3.amazonaws.com/m1xes/sub-pop-mix-1%2F01-Dntel-The_Distance_%28ft._Arthur%26Yu%29.mp3</location>
      <meta rel="type">mp3</meta>
      <title>01-Dntel-The_Distance_(ft._Arthur&Yu)</title>
    </track>
    <track>
      <location>http://s3.amazonaws.com/m1xes/sub-pop-mix-1%2F02-No_Age-Eraser.mp3</location>
      <meta rel="type">mp3</meta>
      <title>02-No_Age-Eraser</title>
    </track>
    ...
	"""

def xspf_slim_player(context, url):
	return """<object id="xspf-slim-player" class="xspf-slim-player" 
  width="400" height="15" 
  type="application/x-shockwave-flash" 
  name="xspf-slim-player" 
  data="/shrub/swf/xspf_player_slim.swf?playlist_url=%s">

  <param name="allowscriptaccess" value="always"/>
</object>""" % (url)

def xspf_slim_player_swf_object(context, url):
	return """var loadXspfSlimPlayer = function() {
  var xspfUrl = "http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf";
  var flashvars = { };
  var params = { allowscriptaccess: "always" };
  var attributes = { id: "xspf-slim-player", name: "xspf-slim-player", styleclass:"xspf-slim-player" };

  swfobject.embedSWF('/shrub/swf/xspf_player_slim.swf?playlist_url=' + encodeURI(xspfUrl), "xspf-slim-player", "400", "15", "8.0.0", false, flashvars, params, attributes);
};

$(document).ready(loadXspfSlimPlayer);"""