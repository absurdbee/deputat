function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

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
loadScripts('/static/scripts/functions/general.js?ver3');
loadScripts('/static/scripts/functions/comment_attach.js?ver4');
loadScripts('/static/scripts/functions/message_attach.js?ver4');
loadScripts('/static/scripts/functions/elect_new_attach.js?ver1');
loadScripts('/static/scripts/functions/preview.js?ver4');
loadScripts('/static/scripts/main.js?ver9');
loadScripts('/static/scripts/progs/blog.js?ver2');
loadScripts('/static/scripts/progs/elect.js?ver2');
loadScripts('/static/scripts/progs/user.js');
loadScripts('/static/scripts/progs/photo.js');
loadScripts('/static/scripts/progs/doc.js');
loadScripts('/static/scripts/progs/video.js');
loadScripts('/static/scripts/progs/music.js');
loadScripts('/static/scripts/progs/survey.js');
loadScripts('/static/scripts/auth.js');
loadScripts('/static/scripts/progs/community.js');
loadScripts('/static/scripts/progs/chat.js');
