# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>${title}</title>  
    <link href="/shrub/css/yui/reset/reset-min.css" rel="stylesheet" type="text/css"/>
    <link href="/shrub/css/yui/fonts/fonts-min.css" rel="stylesheet" type="text/css"/>
    <link href="/shrub/css/yui/grids/grids-min.css" rel="stylesheet" type="text/css"/>
    <link href="/shrub/css/screen.css" rel="stylesheet" type="text/css"/>
    
    <script type="text/javascript" src="/shrub/javascripts/jquery-1.2.6.pack.js"></script>
    <script type="text/javascript" src='/shrub/javascripts/swfobject.js'></script>
    <script type="text/javascript" src='/shrub/javascripts/shrub.js'></script>
    
    <!--
      <script type='text/javascript' src='http://getfirebug.com/releases/lite/1.2/firebug-lite-compressed.js'></script>
    -->
  
    %if path:
    <link href="http://shrub.appspot.com/${path}?format=rss" rel="alternate" title="RSS Feed" type="application/rss+xml" />
    %endif
  </head>
  
  <body>
    ${self.body()}
    
    <script type="text/javascript">
    var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
    document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
    var pageTracker = _gat._getTracker("UA-1286493-9");
    pageTracker._trackPageview();
    </script>
  </body>
</html>