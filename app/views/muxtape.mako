# -*- coding: utf-8 -*-
<%namespace name="base" module="app.helpers.base"/>\
<%inherit file="layout.mako" />

<div id="doc3" class="shrub-tape">    

  <div id="hd">
  </div>  
  
  <div id="bd">
    
    <div id="tape-info">
      <div id="shrub-player" class="flash-player warn"><span>You need Javascript enabled and/or a recent version of Flash.</span></div>
      
      <p>
      <a id="tape-play" href="" onClick="shrubTape.playTrack(shrubPlayer.getCurrentTrack(), true); return false;">Play</a>
      <a id="tape-stop" href="" onClick="shrubTape.stop(); return false;">Stop</a>
      <a id="tape-skip1" href="" onClick="shrubPlayer.jump(30); return false;">Jump</a>
      </p>
    </div>

    %if len(tracks) == 0:
      <hr/>
      <p class="warn"><span>No tracks available.</span></p>
    %else:
    
    <ul id="songs">      
      %for i in range(len(tracks)):
      <li id="song-${i}" class="song">
        <div id="song-bar-${i}" class="song-bar">&nbsp;</div>
        <div class="song-g">
          <span class="song-name unknown">${tracks[i].title}</span>
          <span class="song-duration unknown">0:00</span>
          <span class="song-loaded unknown">0%</span>
          <span class="song-album"></span>
          <!--<span class="song-download"><a href="${tracks[i].location}">Download</a></span>-->
          <span class="song-status">&nbsp;</span>
          <span class="song-position" style="display:none">0:00</span>
        </div>
      </li>
      %endfor
    </ul>
    
    %endif
    
  </div>
  
  <div id="ft">
    <p><a href="${list_url}">Files</a> &mdash; <a href="${xspf_url}">XSPF</a> &mdash; <a href="#" onClick="loadID3(); return false;">Reload ID3</a> &mdash; <a href="${s3response.url}">Proxied</a></p>    
    <p>Based on <a href="http://muxtape.com">MuxTape</a> and <a href="http://opentape.fm/">OpenTape</a>.</p>
    <%include file="footer.mako"/>
  </div>
</div>


<script type="text/javascript">
// Callback from player.swf load
function playerReady(obj) {
  shrubPlayer.setPlayer(obj);
}

</script>

<script type="text/javascript">
var loadID3 = function() {
  var flashvars = { type: "xml", shuffle: "false", repeat: "list", file: "${xspf_url}"	}			
	var params = { allowscriptaccess: "always" };			
	var attributes = { id: "shrub-player", name: "shrub-player", styleclass: "flash-player" };
	
	swfobject.embedSWF('/shrub/swf/player.swf', "shrub-player", "0", "0", "8.0.0", false, flashvars, params, attributes);
    
  for(var i = 0, length = ${len(tracks)}; i < length; i++) {
    (function(index) {
      $("#song-" + index).click(function() {
        shrubTape.playTrack(index, true);
      });     
    })(i);
  }
  
  var id3Urls = ${base.to_json(id3_urls)};
  shrubTape.loadID3Urls(id3Urls);     
};

$(document).ready(loadID3);
</script>
