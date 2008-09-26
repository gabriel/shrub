# -*- coding: utf-8 -*-
<%namespace name="base" module="app.helpers.base"/>\
<%namespace name="helper" module="app.helpers.list"/>\
<%inherit file="layout.mako" />

<div id="doc3">    

  <div id="hd">

    <h1>      
      %for i in range(len(path_components)):
        <a href="/${'/'.join(path_components[0:i+1])}/">${path_components[i]}</a> <span>/</span>
      %endfor
    </h1>
    
    <p class="rss rss-top"><a href="/${path}/?format=rss"><img src="/shrub/images/rss.png" alt="RSS"/></a></p>
  </div>  
  
  <div id="bd">

    <div id="yui-main">
    
      <div class="yui-b">
      
        %if s3response.is_truncated:
          <hr/>
          <p class="warn"><span>There were too many items ( &gt; ${handler.max_keys} ) in the current bucket to display. The results were truncated and may be inaccurate.</span></p>
          <hr/>
        %endif
        
        %if len(s3response.files) == 0:
          <hr/>
          <p class="warn"><span>No files available.</span></p>            
        %else:
        
        <table class="s3">            
        <colgroup>
          <col width="70%"/>
          <col width="20%"/>
          <col width="10%"/>
        </colgroup>
        <thead>
          <tr>
          ${helper.header_link('Name', 'name', sort, sort_asc, path)}
          ${helper.header_link('Date', 'date', sort, sort_asc, path)}
          ${helper.header_link('Size', 'size', sort, sort_asc, path)}
          </tr>
        </thead>
        <tbody>
        %for i in range(len(s3response.files)):
        <% file = s3response.files[i] %>
        <tr class="${helper.if_even(i, 'even', 'odd')}">
          <td>
            %if file.is_folder:
              <img src="/shrub/images/folder.png"/>
              <a class="name folder" href="/${file.name_with_prefix(path)}">${file.name}</a>              
            %else:
              <img src="/shrub/images/page_white.png"/>
              <a class="name file" href="${file.to_url(False)}">${file.name}</a>
            %endif
          </td>
          <td class="date">${file.pretty_last_modified('-')}</td>
          <td class="size">${file.pretty_size('-')}</td>
        </tr>
        %endfor
        </tbody>
        </table>
        
        %endif
      
      </div>
    
    </div>
  </div>
  
  <div id="ft">    
      Formats: 
        <a href="/${path}/?format=rss">RSS</a> /
        <a href="/${path}/?format=json">JSON</a> /
        <a href="/${path}/?format=tape">*Tape</a>
      </p>
    <%include file="footer.mako"/>
    <p><span class="debug">Proxied: ${s3response.url}</span></p>
  </div>
        
</div>
