# Shrub

Amazon S3 Proxy for Google App Engine.

The idea is to have a proxy to act in between S3 and browsers or other devices. 

Questions? See [shrub-gae google group](http://groups.google.com/group/shrub-gae)

Examples of formats that Shrub exposes are:

* RSS
* HTML
* JSON
* XSPF
* HTML/Tape (like MuxTape/OpenTape)

The web app: `app/`
The main library: `shrub/`
Third party libraries: `lib/`
Static assets: `public/`
Tests: `test/`

## Running

To run locally:

1. Clone the repo: git clone git://github.com/gabriel/shrub.git
2. Start up GoogleAppEngineLauncher (Get GoogleAppEngine SDK + Launcher at http://code.google.com/appengine/)
3. Right click on screen, and choose Add Existing
4. Choose path to cloned repo.
5. Hit run.
6. Go to http://localhost:8080/

## Other Libraries

- lib/mako: [mako](http://www.makotemplates.org)
- lib/iso8601: [pyiso8601](http://code.google.com/p/pyiso8601/)
- lib/id3: [id3reader](http://nedbatchelder.com/code/modules/id3reader.html)
- lib/simplejson: [simplejson](https://svn.red-bean.com/bob/simplejson/tags/simplejson-1.3/docs/index.html)

- test/lib/gaeunit: [GAEUnit](http://code.google.com/p/gaeunit/)

- public/javascripts/swfobject: [SWFObject](http://code.google.com/p/swfobject/)
- public/javascripts/jquery: [jQuery](http://jquery.com/)

- public/css/yui: [YUI](http://developer.yahoo.com/yui/) grid, fonts, reset (CSS)
- public/images/...: [famfamfam](http://www.famfamfam.com/lab/icons/silk/) Silk icons
- public/swf/player.swf: [JW Flash audio player](http://www.jeroenwijering.com/?item=JW_FLV_Media_Player)

Main leaf icon was purchased from iStockPhoto and is licensed by me (Gabriel Handford).

## Changes

The following changes were made to libraries to handle certain features:

* simplejson has some changes to automatically encode non-encodable data types via __json__ method if an object responds to it.
* id3reader has some changes to allow it to parse from a buffer, and also to be able to read truncated ID3 tag data.

## Tests

To run the tests:

* Uncomment the test routes in app.yaml
* Load the dev_server and go to: [http://localhost:8080/test?package=controllers](http://localhost:8080/test?package=controllers)

----
Copyright 2008 Gabriel Handford