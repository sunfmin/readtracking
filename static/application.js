var readtracking = new Object()

readtracking.loadDictionaryIframes = function(dics_json) {
    d = document;
    buttons = [];
    iframes = [];
    jQuery.each(dics_json, function() {
        a = d.createElement('input');
        a.type='button';
        a.value=this.title;
        $("body").append(a);
        buttons.push(a);
    });
    $("body").append("<a href='http://peek.la/dicts' target='_blank' class='manage_buttons'>Add or delete buttons</a>");
    
    height = 500;
    if(window.innerHeight) {
        height = window.innerHeight - 60;
    }
    
    for (var i=0; i < dics_json.length; i++) {
        ifrm=d.createElement('iframe');
        ifrm.scrolling='auto';
        ifrm.style.width='100%';
        ifrm.style.height= (height + 'px');
        ifrm.src=dics_json[i].url
        ifrm.style.display="none";
        $("body").append(ifrm);
        iframes.push(ifrm);
        buttons[i].myiframe = ifrm;
    }
    
    d.current_iframe = iframes[0];
    if(d.current_iframe){
        d.current_iframe.style.display="block";
    }
    for (var i=0; i < dics_json.length; i++) {
        $(buttons[i]).click(function(e){
            d.current_iframe.style.display="none";
            d.current_iframe = this.myiframe;
            d.current_iframe.style.display="block";
        })
    }




}

