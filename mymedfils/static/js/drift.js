!function e(t,n,i){function s(l,a){if(!n[l]){if(!t[l]){var r="function"==typeof require&&require;if(!a&&r)return r(l,!0);if(o)return o(l,!0);var h=new Error("Cannot find module '"+l+"'");throw h.code="MODULE_NOT_FOUND",h}var u=n[l]={exports:{}};t[l][0].call(u.exports,function(e){var n=t[l][1][e];return s(n?n:e)},u,u.exports,e,t,n,i)}return n[l].exports}for(var o="function"==typeof require&&require,l=0;l<i.length;l++)s(i[l]);return s}({1:[function(e,t,n){(function(t){"use strict";function i(e){return e&&e.__esModule?e:{"default":e}}function s(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}var o=function(){function e(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}return function(t,n,i){return n&&e(t.prototype,n),i&&e(t,i),t}}();Object.defineProperty(n,"__esModule",{value:!0}),n.VERSION=void 0;var l=e("./util/dom"),a=e("./injectBaseStylesheet"),r=i(a),h=e("./Trigger"),u=i(h),d=e("./ZoomPane"),c=i(d),f=(n.VERSION="0.1.5",function(){function e(t){var n=this,i=arguments.length<=1||void 0===arguments[1]?{}:arguments[1];if(s(this,e),this.destroy=function(){n._unbindEvents()},this.triggerEl=t,!(0,l.isDOMElement)(this.triggerEl))throw new TypeError("`new Drift` requires a DOM element as its first argument.");var o=i.namespace,a=void 0===o?null:o,h=i.showWhitespaceAtEdges,u=void 0===h?!1:h,d=i.containInline,c=void 0===d?!1:d,f=i.inlineOffsetX,m=void 0===f?0:f,g=i.inlineOffsetY,v=void 0===g?0:g,p=i.sourceAttribute,w=void 0===p?"data-zoom":p,y=i.zoomFactor,_=void 0===y?3:y,E=i.paneContainer,C=void 0===E?document.body:E,b=i.inlinePane,z=void 0===b?375:b,O=i.handleTouch,S=void 0===O?!0:O,L=i.onShow,P=void 0===L?null:L,M=i.onHide,k=void 0===M?null:M,I=i.injectBaseStyles,T=void 0===I?!0:I;if(z!==!0&&!(0,l.isDOMElement)(C))throw new TypeError("`paneContainer` must be a DOM element when `inlinePane !== true`");this.settings={namespace:a,showWhitespaceAtEdges:u,containInline:c,inlineOffsetX:m,inlineOffsetY:v,sourceAttribute:w,zoomFactor:_,paneContainer:C,inlinePane:z,handleTouch:S,onShow:P,onHide:k,injectBaseStyles:T},this.settings.injectBaseStyles&&(0,r["default"])(),this._buildZoomPane(),this._buildTrigger()}return o(e,[{key:"_buildZoomPane",value:function(){this.zoomPane=new c["default"]({container:this.settings.paneContainer,zoomFactor:this.settings.zoomFactor,showWhitespaceAtEdges:this.settings.showWhitespaceAtEdges,containInline:this.settings.containInline,inline:this.settings.inlinePane,namespace:this.settings.namespace,inlineOffsetX:this.settings.inlineOffsetX,inlineOffsetY:this.settings.inlineOffsetY})}},{key:"_buildTrigger",value:function(){this.trigger=new u["default"]({el:this.triggerEl,zoomPane:this.zoomPane,handleTouch:this.settings.handleTouch,onShow:this.settings.onShow,onHide:this.settings.onHide,sourceAttribute:this.settings.sourceAttribute})}},{key:"isShowing",get:function(){return this.zoomPane.isShowing}},{key:"zoomFactor",get:function(){return this.settings.zoomFactor},set:function(e){this.settings.zoomFactor=e,this.zoomPane.settings.zoomFactor=e}}]),e}());n["default"]=f,t.Drift=f}).call(this,"undefined"!=typeof global?global:"undefined"!=typeof self?self:"undefined"!=typeof window?window:{})},{"./Trigger":2,"./ZoomPane":3,"./injectBaseStylesheet":4,"./util/dom":5}],2:[function(e,t,n){"use strict";function i(e){return e&&e.__esModule?e:{"default":e}}function s(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}var o=function(){function e(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}return function(t,n,i){return n&&e(t.prototype,n),i&&e(t,i),t}}();Object.defineProperty(n,"__esModule",{value:!0});var l=e("./util/throwIfMissing"),a=i(l),r=function(){function e(){var t=arguments.length<=0||void 0===arguments[0]?{}:arguments[0];s(this,e),h.call(this);var n=t.el,i=void 0===n?(0,a["default"])():n,o=t.zoomPane,l=void 0===o?(0,a["default"])():o,r=t.sourceAttribute,u=void 0===r?(0,a["default"])():r,d=t.handleTouch,c=void 0===d?(0,a["default"])():d,f=t.onShow,m=void 0===f?null:f,g=t.onHide,v=void 0===g?null:g;this.settings={el:i,zoomPane:l,sourceAttribute:u,handleTouch:c,onShow:m,onHide:v},this._bindEvents()}return o(e,[{key:"_bindEvents",value:function(){this.settings.el.addEventListener("mouseenter",this._show,!1),this.settings.el.addEventListener("mouseleave",this._hide,!1),this.settings.el.addEventListener("mousemove",this._handleMovement,!1),this.settings.handleTouch&&(this.settings.el.addEventListener("touchstart",this._show,!1),this.settings.el.addEventListener("touchend",this._hide,!1),this.settings.el.addEventListener("touchmove",this._handleMovement,!1))}},{key:"_unbindEvents",value:function(){this.settings.el.removeEventListener("mouseenter",this._show,!1),this.settings.el.removeEventListener("mouseleave",this._hide,!1),this.settings.el.removeEventListener("mousemove",this._handleMovement,!1),this.settings.handleTouch&&(this.settings.el.removeEventListener("touchstart",this._show,!1),this.settings.el.removeEventListener("touchend",this._hide,!1),this.settings.el.removeEventListener("touchmove",this._handleMovement,!1))}},{key:"isShowing",get:function(){return this.settings.zoomPane.isShowing}}]),e}(),h=function(){var e=this;this._show=function(t){t.preventDefault();var n=e.settings.onShow;n&&"function"==typeof n&&n(),e.settings.zoomPane.show(e.settings.el.getAttribute(e.settings.sourceAttribute),e.settings.el.clientWidth),e._handleMovement(t)},this._hide=function(t){t.preventDefault();var n=e.settings.onHide;n&&"function"==typeof n&&n(),e.settings.zoomPane.hide()},this._handleMovement=function(t){if(t.preventDefault(),e.isShowing){var n=void 0,i=void 0;if(t.touches){var s=t.touches[0];n=s.clientX,i=s.clientY}else n=t.clientX,i=t.clientY;var o=e.settings.el,l=o.getBoundingClientRect(),a=n-l.left,r=i-l.top,h=a/e.settings.el.clientWidth,u=r/e.settings.el.clientHeight;e.settings.zoomPane.setPosition(h,u,l)}}};n["default"]=r},{"./util/throwIfMissing":6}],3:[function(e,t,n){"use strict";function i(e){return e&&e.__esModule?e:{"default":e}}function s(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}var o=function(){function e(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}return function(t,n,i){return n&&e(t.prototype,n),i&&e(t,i),t}}();Object.defineProperty(n,"__esModule",{value:!0});var l=e("./util/throwIfMissing"),a=i(l),r=e("./util/dom"),h="animation"in document.createElement("div").style,u=function(){function e(){var t=this,n=arguments.length<=0||void 0===arguments[0]?{}:arguments[0];s(this,e),this._completeShow=function(){t.el.removeEventListener("animationend",t._completeShow,!1),(0,r.removeClasses)(t.el,t.openingClasses)},this._completeHide=function(){t.el.removeEventListener("animationend",t._completeHide,!1),(0,r.removeClasses)(t.el,t.openClasses),(0,r.removeClasses)(t.el,t.closingClasses),(0,r.removeClasses)(t.el,t.inlineClasses),t.el.setAttribute("style",""),t.el.parentElement===t.settings.container?t.settings.container.removeChild(t.el):t.el.parentElement===t.settings.inlineContainer&&t.settings.inlineContainer.removeChild(t.el)},this.isShowing=!1;var i=n.container,o=void 0===i?null:i,l=n.zoomFactor,h=void 0===l?(0,a["default"])():l,u=n.inline,d=void 0===u?(0,a["default"])():u,c=n.namespace,f=void 0===c?null:c,m=n.showWhitespaceAtEdges,g=void 0===m?(0,a["default"])():m,v=n.containInline,p=void 0===v?(0,a["default"])():v,w=n.inlineOffsetX,y=void 0===w?0:w,_=n.inlineOffsetY,E=void 0===_?0:_;this.settings={container:o,zoomFactor:h,inline:d,namespace:f,showWhitespaceAtEdges:g,containInline:p,inlineOffsetX:y,inlineOffsetY:E},this.settings.inlineContainer=document.body,this.openClasses=this._buildClasses("open"),this.openingClasses=this._buildClasses("opening"),this.closingClasses=this._buildClasses("closing"),this.inlineClasses=this._buildClasses("inline"),this._buildElement()}return o(e,[{key:"_buildClasses",value:function(e){var t=["drift-"+e],n=this.settings.namespace;return n&&t.push(n+"-"+e),t}},{key:"_buildElement",value:function(){this.el=document.createElement("div"),(0,r.addClasses)(this.el,this._buildClasses("zoom-pane"));var e=document.createElement("div");(0,r.addClasses)(e,this._buildClasses("zoom-pane-loader")),this.el.appendChild(e),this.imgEl=document.createElement("img"),this.el.appendChild(this.imgEl)}},{key:"_setImageURL",value:function(e){this.imgEl.setAttribute("src",e)}},{key:"_setImageSize",value:function(e){this.imgEl.style.width=e*this.settings.zoomFactor+"px"}},{key:"setPosition",value:function(e,t,n){var i=-(this.imgEl.clientWidth*e-this.el.clientWidth/2),s=-(this.imgEl.clientHeight*t-this.el.clientHeight/2),o=-(this.imgEl.clientWidth-this.el.clientWidth),l=-(this.imgEl.clientHeight-this.el.clientHeight);if(this.el.parentElement===this.settings.inlineContainer){var a=window.scrollX,r=window.scrollY,h=n.left+e*n.width-this.el.clientWidth/2+this.settings.inlineOffsetX+a,u=n.top+t*n.height-this.el.clientHeight/2+this.settings.inlineOffsetY+r;if(this.settings.containInline){this.el.getBoundingClientRect();h<n.left+a?h=n.left+a:h+this.el.clientWidth>n.left+n.width+a&&(h=n.left+n.width-this.el.clientWidth+a),u<n.top+r?u=n.top+r:u+this.el.clientHeight>n.top+n.height+r&&(u=n.top+n.height-this.el.clientHeight+r)}this.el.style.left=h+"px",this.el.style.top=u+"px"}this.settings.showWhitespaceAtEdges||(i>0?i=0:o>i&&(i=o),s>0?s=0:l>s&&(s=l)),this.imgEl.style.transform="translate("+i+"px, "+s+"px)"}},{key:"_removeListenersAndResetClasses",value:function(){this.el.removeEventListener("animationend",this._completeShow,!1),this.el.removeEventListener("animationend",this._completeHide,!1),(0,r.removeClasses)(this.el,this.openClasses),(0,r.removeClasses)(this.el,this.closingClasses)}},{key:"show",value:function(e,t){this._removeListenersAndResetClasses(),this.isShowing=!0,(0,r.addClasses)(this.el,this.openClasses),this._setImageURL(e),this._setImageSize(t),this._isInline?this._showInline():this._showInContainer(),h&&(this.el.addEventListener("animationend",this._completeShow,!1),(0,r.addClasses)(this.el,this.openingClasses))}},{key:"_showInline",value:function(){this.settings.inlineContainer.appendChild(this.el),(0,r.addClasses)(this.el,this.inlineClasses)}},{key:"_showInContainer",value:function(){this.settings.container.appendChild(this.el)}},{key:"hide",value:function(){this._removeListenersAndResetClasses(),this.isShowing=!1,h?(this.el.addEventListener("animationend",this._completeHide,!1),(0,r.addClasses)(this.el,this.closingClasses)):((0,r.removeClasses)(this.el,this.openClasses),(0,r.removeClasses)(this.el,this.inlineClasses))}},{key:"_isInline",get:function(){var e=this.settings.inline;return e===!0||"number"==typeof e&&window.innerWidth<=e}}]),e}();n["default"]=u},{"./util/dom":5,"./util/throwIfMissing":6}],4:[function(e,t,n){"use strict";function i(){if(!document.querySelector(".drift-base-styles")){var e=document.createElement("style");e.type="text/css",e.classList.add("drift-base-styles"),e.appendChild(document.createTextNode(s));var t=document.head;t.insertBefore(e,t.firstChild)}}Object.defineProperty(n,"__esModule",{value:!0}),n["default"]=i;var s="\n@keyframes noop {  }\n\n.drift-zoom-pane.drift-open {\n  display: block;\n}\n\n.drift-zoom-pane.drift-opening, .drift-zoom-pane.drift-closing {\n  animation: noop;\n}\n\n.drift-zoom-pane {\n  position: absolute;\n  overflow: hidden;\n  width: 100%;\n  height: 100%;\n  top: 0;\n  left: 0;\n  pointer-events: none;\n}\n\n.drift-zoom-pane-loader {\n  display: none;\n}\n\n.drift-zoom-pane img {\n  position: absolute;\n  display: block;\n}\n"},{}],5:[function(e,t,n){"use strict";function i(e){return e&&"undefined"!=typeof Symbol&&e.constructor===Symbol?"symbol":typeof e}function s(e){return a?e instanceof HTMLElement:e&&"object"===("undefined"==typeof e?"undefined":i(e))&&null!==e&&1===e.nodeType&&"string"==typeof e.nodeName}function o(e,t){t.forEach(function(t){e.classList.add(t)})}function l(e,t){t.forEach(function(t){e.classList.remove(t)})}Object.defineProperty(n,"__esModule",{value:!0}),n.isDOMElement=s,n.addClasses=o,n.removeClasses=l;var a="object"===("undefined"==typeof HTMLElement?"undefined":i(HTMLElement))},{}],6:[function(e,t,n){"use strict";function i(){throw new Error("Missing parameter")}Object.defineProperty(n,"__esModule",{value:!0}),n["default"]=i},{}]},{},[1]);