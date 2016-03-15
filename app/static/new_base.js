window.addEventListener('load', function(){
	if (document.body.clientHeight < document.body.scrollHeight) {
		document.body.setAttribute('style', 'height:' + document.body.scrollHeight + 'px');
	}
}, false);
