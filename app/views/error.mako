# -*- coding: utf-8 -*-
<%inherit file="layout.mako" />

<div id="doc3">    

  <div id="yui-main">
    <div class="yui-b">
    
        <h1>${title}</h1>
    
        %if message:          
          <p>${message}</p>
          <hr/>
        %endif
    
        %if s3_url:
        <p><span class="debug">The resource at <tt>${s3url}</tt> was not available. (${status_code})</span></p>
        %else:
        <p><span class="debug">Status: ${status_code}</span></p>
        %endif
        
        <hr/>
        
        <p><a href="/">Home</a> &mdash; <a href="${request.url}">Refresh</a></p>
      
      </div>
    
    </div>
  </div>
  
</div>