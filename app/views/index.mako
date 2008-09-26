# -*- coding: utf-8 -*-
<%namespace name="base" module="app.helpers.base"/>\
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
          
          <h2>URL parameters</h2>
          
          <table id="url-params" class="tabular">
            <thead>
              <tr><th>Parameter</th> <th>Description</th> <th>Accepted</th> <th>Default</th></tr>
            <tbody>
            <tr><td>format</td> <td>Response format</td> <td>rss,json,id3-json,tape</td> <td>None (HTML)</td></tr>
            <tr><td>delimiter</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> / </td></tr>
            <tr><td>prefix</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> </td></tr>
            <tr><td>marker</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> </td></tr>
            <tr><td>max-keys</td> <td>See S3 docs</td> <td>Passed to S3</td> <td> </td></tr>
            </tbody>
          </table>
          <p><span class="disclaimer">See below for more info.</span></p>
          
          <hr/>          
          
          <h2>RSS</h2>
          <p>Get RSS feed with <em>format=rss</em> URL parameter. <br/> For example, <a href="/s3hub?format=rss">http://shrub.appspot.com/s3hub?format=rss</a> <br/><span class="disclaimer">See limitations below.</span></p>
          
          <hr/>
          
          <h2>JSON</h2>
          <p>Get list bucket response in JSON format with <em>format=json</em> URL parameter.<br/> For example, <a href="/s3hub?format=rss">http://shrub.appspot.com/s3hub?format=json</a> <br/><span class="disclaimer">See limitations below.</span></p>
          
          <hr/>
          
          <h2>ID3</h2>
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