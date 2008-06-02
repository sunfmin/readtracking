(function(){


var loadReadTracking = function(){
w=window,d=document,e=encodeURIComponent,url=location.href;
b=d.getElementsByTagName('body')[0];

var selectedWord = function(){
    var txt='';
    if (w.getSelection)
    	txt = w.getSelection();
    else if (d.getSelection)
    	txt = d.getSelection();
    else if (d.selection)
    	txt = d.selection.createRange().text;
    return txt;
}

var ask_url = 'http://readtracking.appspot.com/ask?q='+e(selectedWord())+'&url='+e(url)+'&title='+e(d.title);
if(window.readtracking_ask_iframe_container){
    b.removeChild(window.readtracking_ask_iframe_container);
}

height = 580;
if(w.innerHeight) {
    height = w.innerHeight - 10;
}
width = 800;
if(w.innerWidth) {
    width = w.innerWidth / 2
}

//making wraper
wrpr=d.createElement('div');
wrpr.style.zIndex='10000000';
wrpr.style.position='fixed';
wrpr.style.top='0';
wrpr.style.right='0';
wrpr.style.lineHeight='20px';
wrpr.style.width=(width + 'px');
wrpr.style.height=(height + 'px');
wrpr.style.margin="0px";
wrpr.style.textAlign='left';
wrpr.style.background='#f6f5ee';
wrpr.style.border='1px solid #CCCCCC';
wrpr.style.borderTopWidth='1px';
wrpr.style.borderRightWidth='1px';
wrpr.style.fontFamily = 'Courier New';
window.readtracking_ask_iframe_container = wrpr;


//making close button
butt=d.createElement('input');
with (butt) {
    type='button';
    value='Close';
    style.clear='both';
    style.width='100px';
    style.marginRight='20px';
    style.padding='2px';
    style.color='#5f758b';
    style.fontSize='12px';
    style.background=' #e1e1e1';
    style.border="0"
    style.borderRight='1px solid #CCCCCC';
    style.borderBottom='1px solid #CCCCCC';
}


// making logo
logo=d.createElement('a');
with (logo) {
 href="http://readtracking.appspot.com";
 alt="ReadTracking";
 title="ReadTracking";
 paddingLeft="30px";
 innerHTML="ReadTracking"
 target="_top";
 style.fontSize="12px"
}


//adding events for close button
butt.onmouseover = function() {
	this.style.color='#435362';
	this.style.background='#d9d9d9';
};

butt.onmouseout = function() {
	this.style.color='#5f758b';
	this.style.background='#e1e1e1';
};

butt.onclick=function() {
	wrpr.style.display = 'none';
};

random_key =  (Math.random() + "").replace('.', '');

//making iframe
ifrm=d.createElement('iframe');
ifrm.id="readtracking_iframe_" + random_key
ifrm.scrolling='no';
ifrm.style.display='block';
ifrm.style.width=(width - 20) + 'px';
ifrm.style.height=(height - 40) + 'px';
ifrm.style.borderWidth='0';
ifrm.style.margin="0";
ifrm.src=ask_url;

b.appendChild(wrpr);
wrpr.appendChild(butt);
wrpr.appendChild(logo);
wrpr.appendChild(ifrm);
}

// var keydown_handler = function(e){
//     if(e.keyCode == 27){
//         wrpr = window.readtracking_ask_iframe_container;
//         if(!wrpr) {
//             return;
//         }
//         if(wrpr.style.display == 'none') {
//             loadReadTracking();
//         } else {
//             b=document.getElementsByTagName('body')[0];
//             b.removeChild(wrpr)
//             window.readtracking_ask_iframe_container = null;
//         }
//     }
//     window.focus();
// }


loadReadTracking()
// window.onkeydown = keydown_handler



})();

