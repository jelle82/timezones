function clockS(){

	function addZero(i) {
		if (i < 10) {
			i = "0" + i;
		}
		return i;
	}

var d = new Date();
var x = document.getElementById("clock");
var h = addZero(d.getHours());
var m = addZero(d.getMinutes());
var s = addZero(d.getSeconds());
x.innerHTML = h + ":" + m + ":" + s;

setTimeout("clockS()",1000);
}

window.onload=clockS;
