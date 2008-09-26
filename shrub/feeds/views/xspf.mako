# -*- coding: utf-8 -*-
<%namespace name="he" module="shrub.feeds.helper"/>\
<?xml version="1.0" encoding="UTF-8"?>
<playlist version="0" xmlns="http://xspf.org/ns/0/">
  <title>${title | h}</title>
  <creator>${creator | h}</creator>
  <info>${info | h}</info>
  <location>${location | h}</location>
  <trackList>
    %for track in tracks:
    <track>
      <location>${track.location | h}</location>
      <meta rel="type">${track.meta | h}</meta>
      <title>${track.title | h}</title>
      ${he.if_tag(track, 'info', html_escape=True)}\
    </track>
    %endfor
  </trackList>
</playlist>