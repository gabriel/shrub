/*
 Player.
 Controls and handles current state for the player.
*/
var ShrubPlayer = (function() {
  
  var _player;
  var _isReady = false;
  
  var _currentTrack = 0;
  var _currentPosition = 0;
  var _currentDuration = 0;
  var _currentStatus = "";
  var _currentLoaded = 0;
  var _currentTotal = 0;
  var _currentLoadedPercentage = 0;
  
  var _onPositionChange;
  var _onLoadedChange;
  var _onMetaChange;
  var _onTrackChange;
  
  return {
    getCurrentTrack: function() {
      return _currentTrack;
    },
    
    updateState: function(obj) {
  		_currentStatus = obj.newstate;
  		//console.log("Status: " + _currentStatus + ", Current track: " + _currentTrack);
  	},
	
  	updateItem: function(obj) {
  	  if (_currentTrack == obj.index) return false;
  	  
  	  var oldTrack = _currentTrack;
  	  if (_onPositionChange) _onPositionChange(oldTrack, 0, 0);
  		_currentTrack = obj.index;
  		_currentPosition = 0;  		
  		if (_onTrackChange) _onTrackChange(_currentTrack, oldTrack);
  	},
	
	  notifyTime: function(seconds, func) {
	    var minutes = Math.floor(seconds / 60);
	    var secs = Math.round(seconds) % 60;
	    if (secs < 10) secs = "0" + secs;
	    func(_currentTrack, minutes + ":" + secs);
	  },
	
  	updateTime: function (obj) {
      var duration = obj.duration;
  	  var position = Math.round(obj.position);
  	  if (position == _currentPosition || position == 0) return false;
  	  
  	  _currentPosition = position;  		
  		if (!!_onPositionChange) this.notifyTime(_currentPosition, function(track, time) {
  		  var percentage = 0;
  		  if (_currentDuration > 0) percentage = Math.round((_currentPosition / _currentDuration) * 100);
  		  _onPositionChange(track, time, percentage);
  		});
  	},
  	
  	updateLoaded: function(obj) {  	  
  	  _currentLoaded = obj.loaded;
  	  _currentTotal = obj.total;
  	  
  	  var percentage = 0;
  	  if (_currentTotal > 0) percentage = Math.round((_currentLoaded / _currentTotal) * 100);
  	  if (percentage == _currentLoadedPercentage) return;
  	  _currentLoadedPercentage = percentage;
  	  if (_onLoadedChange) _onLoadedChange(_currentTrack, percentage);
  	},
  	
  	updateMeta: function(obj) {
  	  _currentDuration = obj.duration;
  	  if (!!_onMetaChange) this.notifyTime(_currentDuration, _onMetaChange);
  	},
  	
  	onError: function(obj) {
  	  //obj.message;
  	},
  	
  	setPlayer: function(player) {    	
    	var id = player.id;
    	var version = player.version;
    	var client = player.client;
    	//console.log("Player: " + id + ", version: " + version + ", client: " + client);
      _player = document.getElementById(id);      
      _player.addModelListener('STATE', 'ShrubPlayer.updateState');
    	_player.addModelListener('TIME', 'ShrubPlayer.updateTime');
      _player.addControllerListener('ITEM', 'ShrubPlayer.updateItem');  	  
      _player.addModelListener('LOADED', 'ShrubPlayer.updateLoaded');
      _player.addModelListener('ERROR', 'ShrubPlayer.onError');
      _player.addModelListener('META', 'ShrubPlayer.updateMeta');
      _isReady = true;
  	},
  	
  	reset: function() {
  	  _onPositionChange = null;  	  
  	  _onLoadedChange = null;
  	  _onMetaChange = null;
  	  _onTrackChange = null;
  	  _currentLoaded = 0;
  	  _currentTotal = 0;
  	  _currentLoadedPercentage = -1;
  	},
  	
  	play: function(index, options) {
  	  ShrubPlayer.reset();
  	  var changed = false;
  	  if (index >= 0 && _currentTrack != index) {
  	    changed = true;
  	    _currentTrack = index;
  	  }
  	  
  	  if (options) {
  	    if (options.onPositionChange) _onPositionChange = options.onPositionChange;
  	    if (options.onLoadedChange) _onLoadedChange = options.onLoadedChange;
  	    if (options.onMetaChange) _onMetaChange = options.onMetaChange;
  	    if (options.onTrackChange) _onTrackChange = options.onTrackChange;
  	  }
  		if (changed) {
  		  this.sendEvent('ITEM', _currentTrack);
  		  _currentPosition = 0;
  		}
  		//console.log("Play track: " + _currentTrack + ", current position: " + _currentPosition);
  		
  		this.sendEvent('PLAY', true);
  		if (_currentPosition > 0)
  		  this.sendEvent('SEEK', _currentPosition);  		  
  	},
  	
  	seek: function(position) {
  	  this.sendEvent('SEEK', _currentPosition);
  	},
  	
  	jump: function(amount) {
  	  this.sendEvent('SEEK', _currentPosition + amount);
  	},
  	
  	pause: function() {
  	  this.sendEvent('STOP');
  	},

  	stop: function() {
  		this.sendEvent('STOP');
  		_currentPosition = 0;
  	},
  	
  	sendEvent: function(typ, prm) { 
  		if (_isReady) {
        this.thisMovie('shrub-player').sendEvent(typ, prm); 
  		}
  	},

  	thisMovie: function(movieName) {
  		if (navigator.appName.indexOf("Microsoft") != -1) { return window[movieName]; }
  		else { return document[movieName]; }
  	}
  };
	
})();

/*
 Loads ID3 information, asynchronously and in order.
*/
var ShrubTape = (function() {
  
  var _currentId3Index = -1;
  var _urls;
  
  function nextURL() {
    _currentId3Index++;
    if (_currentId3Index < _urls.length)
      return _urls[_currentId3Index];
      
    return null;
  }
  
  function loadNext() {
    var url = nextURL();
    if (!url) return;
    //console.log("Loading url: " + url);
    $.ajax({
      url: url, 
      dataType: 'json',
      success: function(id3) {
        var name_id = "#song-" + _currentId3Index + " .song-name";
        if (!id3.error) {
          if (!!id3.performer && !!id3.title)
            $(name_id).html(id3.performer + " - " + id3.title);
          if (!!id3.album) {
            //var albumSearch = "http://www.amazon.com/s/ref=nb_ss_m?url=search-alias%3Dmusic-album&tag=ducktyper-20&field-keywords=" + id3.album;
            //"<a href='" + albumSearch + "' onClick='ShrubPlayer.stop();'>" + id3.album + "</a>"
            $("#song-" + _currentId3Index + " .song-album").html(id3.album);
          }
        } else {
          $("#song-" + _currentId3Index + " .song-status").html = "Error: " + id3.error;
        }
        $(name_id).removeClass('unknown');          
        loadNext();
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        loadNext();
      }
    });
  }
  
  
  return {
    loadID3Urls: function(urls) {
      _urls = urls;
      _currentId3Index = -1;
      loadNext();
    },
    
    reset: function() {
      $("#songs .song").removeClass("playing");
      $("#songs .song-position").hide();
      $("#songs .song-position").html("0:00");         
      $("#songs .song-bar").width(0);
    },
    
    stop: function() {
      ShrubPlayer.stop();
      // Reset all song positions
      $("#tape-play").html("Play");   
    },
    
    playTrack: function(track, toggle) {
      var node = $("#song-" + track);
            
      // If this song playing stop it
      if (!toggle || node.hasClass("playing")) {   
        $("#songs .song").removeClass("playing");          
        ShrubPlayer.pause();
        $("#tape-play").html("Play");
        if (toggle) return;
      }
      
      this.reset();
      
      // Play node      
      ShrubPlayer.play(track, this);                    
  	  $("#tape-play").html("Pause");
      node.addClass("playing");
      $("#song-" + track + " .song-position").show();
    },

    // Listeners, in ShrubPlayer.play(track, this);
    
    onPositionChange: function(track, time, percentage) {
      //console.log("Position change: " + track + "; " + time + " (" + percentage + ")");
      var positionNode = $("#song-" + track + " .song-position");
      if (time == "0:00") {
        positionNode.hide();
        $("#song-bar-" + track).width(0);
      } else {
        positionNode.html(time);
        $("#song-bar-" + track).width(percentage + "%");
      }
    },
    
    onTrackChange: function(track, old) {
      this.reset();
      $("#song-" + track).addClass("playing");
      $("#song-" + track + " .song-position").show();
    },  	    
    
    onMetaChange: function(track, time) {
      if (isNaN(time)) return;
      var node = $("#song-" + track + " .song-duration");
      node.html(time);
      if (time == "0:00") node.addClass("unknown");
      else node.removeClass("unknown");
    },
    
    onLoadedChange: function(track, percentage) {
      if (isNaN(percentage)) return;
      var node = $("#song-" + track + " .song-loaded");
      node.html(percentage + "%")
      if (percentage > 0) node.removeClass("unknown");
      else node.addClass("unknown");
    }
  };
  
})();

