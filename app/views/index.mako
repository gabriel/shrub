# -*- coding: utf-8 -*-
<%namespace name="base" module="app.helpers.base"/>\
<%namespace name="examples" module="app.helpers.examples"/>\
<%inherit file="layout.mako" />

<div id="doc" class="index">    

  <div id="bd"class="yui-t1">
    <div id="yui-main">
      <div class="yui-b">
    
          <h1>Shrub <span>/ Amazon S3 Proxy</span></h1>
    
          <form method="get" action="/">
           <input autosave="com.appspot.s3hub" id="search" name="q" results="10" type="search" size="50" value=""/>
           <input type="submit" value="Go"/>
          </form>
          <p class="example">Enter in a bucket name</p>
         
          
          <hr/>
          <hr/>
          
          <h2>What?</h2>
          <p>Shrub lists files in public S3 buckets. For when you want to share a bucket with the world.</p>

          <hr/>

          <h2>How?</h2>
          <ol>
          <li>Create a bucket. Make it publicly readable.</li>      
          <li>Point people at your bucket: <strong>http://shrub.appspot.com/<em>bucket-name</em></strong></li>
          <li>Make sure files in the bucket are publicly readable (if you want people to be able to access them).</li>
          </ol>
          
          <br/>
          
          <p>For example, I keep my <a href="http://s3hub.com">S3Hub</a> builds in a s3hub bucket thats publicly readable, so it can be accessed at: <a href="/s3hub">http://shrub.appspot.com/s3hub</a>.</p>
          
          <hr/>
          
          <h2 id="questions">Questions?</h2>
          <p>Visit the google group: <a href="http://groups.google.com/group/shrub-gae">shrub-gae</a></p>
          
          <hr/>
          
          <h2 id="source">Source</h2>
          <p>Shrub is open source. You can find it at github: <a href="http://github.com/gabriel/shrub/tree/master">gabriel/shrub</a></p>
          
          <hr/>
          
          <h2 id="url_params">URL parameters</h2>
          
          <p>These parameters are available to all requests.</p>
          <table id="url-params" class="tabular">
            <thead>
              <tr><th>Parameter</th> <th>Description</th> <th>Accepted</th> <th>Default</th></tr>
            <tbody>
            <tr>
              <td>format</td> <td>Response format</td> 
              <td><a href="#rss">rss</a><br/><a href="#json">json</a><br/><a href="#id3">id3-json</a><br/><a href="#xspf">xspf</a><br/><a href="#tape">tape</a></td> 
              <td>None (HTML)</td>
            </tr>
            <tr><td>delimiter</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> / </td></tr>
            <tr><td>prefix</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> </td></tr>
            <tr><td>marker</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> </td></tr>
            <tr><td>max-keys</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> </td></tr>
            </tbody>
          </table>
          <p><span class="disclaimer">See below for more info.</span></p>
          
          <hr/>          
          
          <h2 id="rss">RSS</h2>
          <p>Generate an RSS 2.0 feed with <em>format=rss</em> URL parameter. <br/> For example, <a href="/s3hub?format=rss">http://shrub.appspot.com/s3hub?format=rss</a>.<br/>
          <span class="disclaimer">See limitations below.</span></p>
          
          <hr/>
          
          <h2 id="json">JSON</h2>
          <p>Get list bucket response in JSON format with <em>format=json</em> URL parameter.<br/> For example, <a href="/s3hub?format=json">http://shrub.appspot.com/s3hub?format=json</a> <br/><span class="disclaimer">See limitations below.</span><br/><br/></p>
<pre>
{"maxKeys": "1000", 
 "prefix": "", 
 "commonPrefixes": [], 
 "isTrucated": false, 
 "contents": [
     {"etag": "\"ee8a4f9c22e98b6dfb1781650eaffe01\"", 
      "storageClass": "STANDARD", 
      "key": "S3Hub-0.5.1.dmg", 
      "lastModified": 1213991757, 
      "bucket": "s3hub", 
      "size": 2635399}, 
     {"etag": "\"cb8d95164e9696823f7b01b306840896\"", 
      "storageClass": "STANDARD", 
      "key": "S3Hub-0.5.10.dmg", 
      "lastModified": 1213991757, 
      "bucket": "s3hub", 
      "size": 2779097}, ...
</pre>
          
          <br/>
          
          <h3>URL parameters</h3>
          
          <table id="url-params" class="tabular">
            <thead>
              <tr><th>Parameter</th> <th>Description</th> <th>Accepted</th> <th>Default</th></tr>
            <tbody>
            <tr><td>callback</td> <td>Callback function name to use in response</td> <td>Callback function names may only use upper and lowercase alphabetic characters (A-Z, a-z), numbers (0-9), the period (.), the underscore (_)</td> <td> </td></tr>
            </tbody>
          </table>
          <br/>
          <br/>
          <p>Example of <a href="http://shrub.appspot.com/s3hub?format=json">http://shrub.appspot.com/s3hub?format=json&callback=myCallback</a>:</p>
          <br/>
<pre>
myCallback({"maxKeys": "1000", "prefix": "", ...})
</pre>
          <hr/>
          
          <h2 id="id3">ID3</h2>
          <p>Lookup ID3 information (returned as JSON) for an MP3 with <em>format=id3-json</em> URL parameter. <br/>For example, <a href="/m1xes/sub-pop-mix-1/01-Dntel-The_Distance_(ft._Arthur%26Yu).mp3?format=id3-json">
            http://shrub.appspot.com/m1xes/sub-pop-mix-1/01-Dntel-The_Distance_(ft._Arthur%26Yu).mp3?format=id3-json</a>
            <br/><br/>
          </p>
          
          <pre>
{ "album": "Dumb Luck",
  "performer": "Dntel",
  "title": "The Distance (Ft. Arthur & Yu)",
  "track": "5/9",
  "year": null,
  "isTruncated": false }
          </pre>

          <p>
            Currently, Shrub will only get the first 1024 bytes of the mp3 (using the Range: bytes=0-1024 header) and will parse as much ID3 tag information as it can. ID3 tag information should be in the beginning of the file (so ID3v1 is not supported). If there was more information after the first 1024 bytes, then the isTruncated will be true. ID3 info is cached for 5 minutes.
          </p>
          
          <br/>
          
          <p>This request accepts JSON url parameters (like callback). See JSON section for more info.</p>
            
          <hr/>
          <h2 id="xspf">XSPF</h2>
          <p>Generate an XSPF playlist of media files in a bucket or folder with <em>format=xspf</em> URL parameter.<br/>
          For example, <a href="/m1xes/sub-pop-mix-1/?format=xspf">http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf</a>
          </p>
          <br/>
          <h3>URL parameters</h3>
          
          <table class="tabular">
            <thead>
              <tr><th>Parameter</th> <th>Description</th></tr>
            <tbody>
            <tr>
              <td>exts</td>
              <td>List of extensions to filter (comma-delimited). For example, exts=mp3,foo,bar
              </td>
            </tr>
            </tbody>
          </table>
          <br/>
          <br/>
          
<pre style="overflow:auto; width=380px">
${examples.xspf_xml() | h}
</pre>
          <hr/>
          <h3 id="music-player">Embeddable music player</h3>
          <p>Embed an <a href="http://musicplayer.sourceforge.net/">xspf music player</a>, pointing to an XSPF format. For example:<br/>
          <a href="http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf">http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf</a>
          </p>
          <br/>
          <br/>
          
          <h4>XSPF Slim Player</h4>
          <div id="xspf-slim-player" class="flash-player warn"><span>You need Javascript enabled and/or a recent version of Flash for the XSPF Slim Player to work.</span></div>
          <hr/>
          
          <h4>XSPF Player</h4>
          <div id="xspf-player" class="flash-player warn"><span>You need Javascript enabled and/or a recent version of Flash for the XSPF player to work.</span></div>
          <hr/>
          <h4>Object embed example</h4>
<pre style="overflow:auto; width=380px">
${examples.xspf_slim_player("http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf") | h}
</pre>
          <hr/>
          <h4>SWFObject embed example</h4>
<pre style="overflow:auto; width=380px">
${examples.xspf_slim_player_swf_object("http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf") | h}
</pre>
          
          <hr/>
          
          <h2>Crossdomain</h2>
          <p>There is a <a href="/crossdomain.xml">crossdomain.xml</a>, so you can use URLs from flash. For example, an <a href="#music-player">XSPF Music Player</a>.</p>
          
          <hr/>
          
          <h2>*Tape</h2>
          <p>Present bucket or directory as a tape (like MuxTape/OpenTape, etc) with <em>format=tape</em> URL parameter. <br/>For example, <a href="/m1xes/sub-pop-mix-1/?format=tape">http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=tape</a> <br/>Currently only supports mp3's. Track information is displayed using ID3v2 info (see above).</p>
          
          <hr/>
          
          <h2>Sub-directories</h2>
          <p>By default, Shrub uses a delimiter of <tt>/</tt> to simulate sub-directories. <br/>
          For example, <a href="/s3hub/Images/">http://shrub.appspot.com/s3hub/Images/</a> only shows the files in the s3hub bucket with the <em>Images/</em> prefix.</p>
          <br/>
          <p>To override, specify an empty delimiter, for example: <a href="/s3hub/?delimiter=">http://shrub.appspot.com/s3hub/?delimiter=</a>.</p>
          
          <hr/>
                    
          <h2>Limitations</h2>
          <p>Shrub will only access the first 1000 entries of a bucket (and will show a warning if you go over). If there are more than 1000 entries in an RSS feed, it will return a 501 error.</p>
                    
      </div>    
    </div>
    
    <div class="yui-b">
      <div id="logo">&nbsp;</div>
    </div>
    
  </div>  
  
  <div id="ft">
    <%include file="footer.mako"/>
    <p class="disclaimer">Amazon is a registered trademark of Amazon.com, Inc. or its subsidiaries in the U.S. and/or other countries.</p>
  </div>
        
</div>

<script type="text/javascript">
var loadXspfPlayer = function() {
  var xspfUrl = "http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf";
  var flashvars = { };
	var params = { allowscriptaccess: "always" };
	var attributes = { id: "xspf-player", name: "xspf-player", styleclass:"xspf-player" };
	
	swfobject.embedSWF('/shrub/swf/xspf_player.swf?playlist_url=' + encodeURI(xspfUrl), "xspf-player", "400", "170", "8.0.0", false, flashvars, params, attributes);
};

var loadXspfSlimPlayer = function() {
  var xspfUrl = "http://shrub.appspot.com/m1xes/sub-pop-mix-1/?format=xspf";
  var flashvars = { };
	var params = { allowscriptaccess: "always" };
	var attributes = { id: "xspf-slim-player", name: "xspf-slim-player", styleclass:"xspf-slim-player" };
	
	swfobject.embedSWF('/shrub/swf/xspf_player_slim.swf?playlist_url=' + encodeURI(xspfUrl), "xspf-slim-player", "400", "15", "8.0.0", false, flashvars, params, attributes);
};

$(document).ready(loadXspfSlimPlayer);
$(document).ready(loadXspfPlayer);

</script>
