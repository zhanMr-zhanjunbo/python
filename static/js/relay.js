function relayLeave(){
	document.getElementById("relayContent").style.display = 'block';	
}
function send(){
	var relay_content = document.getElementById("areaContent").value;
	if (relay_content == ""){
		alert("回复内容不能为空");
	}else{
		$.post("/relay", { "relay_content": relay_content}, function (data) {
			if (data == "ok") {
				document.getElementById("relayContent").style.display = 'none';
			}
		})
	}
}