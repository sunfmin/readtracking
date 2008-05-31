w=window,d=document,e=encodeURIComponent,url=location.href;

var txt='';
if (w.getSelection)
	txt = w.getSelection();
else if (d.getSelection)
	txt = d.getSelection();
else if (d.selection)
	txt = d.selection.createRange().text;

//making wraper
wrpr=d.createElement('div');
with (wrpr) {
	id='wrapper_readtracking';
	style.zIndex='10000000';
	style.position='fixed';
	style.top='0';
	style.right='0';
	style.lineHeight='20px';
	style.width='800px';
	style.height='580px';
	style.margin="0px";
	style.textAlign='left';
	style.background='#f6f5ee';
	wrpr.style.border='2px solid #ababab';
	wrpr.style.borderTopWidth='1px';
	wrpr.style.borderRightWidth='1px';
}

//making close button
butt=d.createElement('input');
with (butt) {
	id='butt_close_readtracking';
	type='button';
	value='Close';
	style.clear='both';
	style.float ="left";
	style.cssFloat ="left";
	style.styleFloat ="left";
    style.width='100px';
    style.margin='0px';
    style.padding='2px';
    style.color='#5f758b';
    style.fontSize='12px';
    style.background=' #e1e1e1';
    style.border='1px solid #7f9db9';
}


// making logo
logo=d.createElement('a');
with (logo) {
 href="http://readtracking.appspot.com";
 alt="Go to my page";
 title="Go to my page";
 innerHTML="ReadTracking"
 target="_top";
 style.display="block";
 style.margin="0px";
 style.marginRIght="3px";
 style.float ="right";
 style.cssFloat ="right";
 style.styleFloat ="right";
 style.width="100px";
 style.height="20px";
 style.marginRight="8px";
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

//making iframe
ifrm=d.createElement('iframe');
with (ifrm) {
	name='iframe_readtracking';
	id='iframe_readtracking';
	scrolling='no';
	style.width='800px';
	style.height='560px';
	style.borderWidth='0';
	style.margin="0px";
	src='http://localhost:8080/ask?url='+e(url)+'&title='+e(d.title)+'&q='+e(txt);
}



//adding elements in document
d.getElementsByTagName('body')[0].appendChild(wrpr);
wrpr.appendChild(butt);
wrpr.appendChild(logo);
wrpr.appendChild(ifrm);

