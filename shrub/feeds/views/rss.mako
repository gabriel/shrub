# -*- coding: utf-8 -*-
<%namespace name="he" module="shrub.feeds.helper"/>\
<?xml version="1.0" encoding="UTF-8"?> 
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">
  <channel>
    <title>${title | h}</title>
    <description>${description | h}</description>
    <link>${link | h}</link>
    <pubDate>${pub_date}</pubDate>
    
    %for item in items:
    <item>
      ${he.if_tag(item, 'title', html_escape=True)}\
      ${he.if_tag(item, 'description', html_escape=True)}\
      ${he.if_tag(item, 'link', html_escape=True)}\
      <pubDate>${item.rfc822_pub_date}</pubDate>
      ${he.if_tag(item, 'guid', html_escape=True)}\
    </item>
    %endfor
  </channel>
</rss>