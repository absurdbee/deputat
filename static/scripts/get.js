function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

window.addEventListener('popstate', function (e) {
  e.preventDefault();

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  ajax_link.open('GET', $serf_history.slice(-1), true);
  ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  ajax_link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          elem_ = document.createElement('span');
          elem_.innerHTML = ajax_link.responseText;
          ajax = elem_.querySelector("#reload_block");
          rtr = document.getElementById('ajax');

          //prev = rtr.querySelector(".main-container");
          //next = ajax.querySelector(".main-container");
          //init_stat_lists(next.getAttribute("data-type"), next.getAttribute("data-pk"), prev.getAttribute("data-type"), prev.getAttribute("data-pk"));

          rtr.innerHTML = ajax.innerHTML;
          window.scrollTo(0, 0);
          title = elem_.querySelector('title').innerHTML;
          window.history.pushState(null, "vfgffgfgf", $serf_history.slice(-1));
          document.title = title;
          create_pagination(rtr);
          get_document_opacity_1();
          $serf_history.push(document.location.href);
          console.log($serf_history)
      }
  }
  ajax_link.send()
});

function loadScripts( src ) {
    var script = document.createElement("SCRIPT"),
        head = document.getElementsByTagName( "head" )[ 0 ],
        error = false;
    script.type = "text/javascript";
    script.onload = script.onreadystatechange = function( e ){
        if ( ( !this.readyState || this.readyState == "loaded" || this.readyState == "complete" ) ) {
            if ( !error ) {
                removeListeners();
            } else {
                null
            }
        }
    };
    script.onerror = function() {
        error = true;
        removeListeners();
    }
    function errorHandle( msg, url, line ) {
        if ( url == src ) {
            error = true;
            removeListeners();
        }
        return false;
    }

    function removeListeners() {
        script.onreadystatechange = script.onload = script.onerror = null;
        if ( window.removeEventListener ) {
            window.removeEventListener('error', errorHandle, false );
        } else {
            window.detachEvent("onerror", errorHandle );
        }
    }

    if ( window.addEventListener ) {
        window.addEventListener('error', errorHandle, false );
    } else {
        window.attachEvent("onerror", errorHandle );
    }
    script.src = src;
    head.appendChild( script );
}

loadScripts('/static/scripts/lib/progressive-image.js');
loadScripts('/static/scripts/functions/general.js');
loadScripts('/static/scripts/functions/comment_attach.js');
loadScripts('/static/scripts/functions/elect_new_attach.js');
loadScripts('/static/scripts/functions/preview.js');
loadScripts('/static/scripts/main.js');
loadScripts('/static/scripts/progs/blog.js');
loadScripts('/static/scripts/progs/elect.js');
loadScripts('/static/scripts/progs/user.js');
loadScripts('/static/scripts/progs/photo.js');
loadScripts('/static/scripts/progs/doc.js');
loadScripts('/static/scripts/progs/video.js');
loadScripts('/static/scripts/progs/music.js');
loadScripts('/static/scripts/progs/survey.js');
loadScripts('/static/scripts/auth.js');
loadScripts('/static/scripts/progs/community.js');
