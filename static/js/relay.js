function relayLeave(){
    document.getElementById("relay_consult").style.display = 'none';
	document.getElementById("relayContent").style.display = 'block';
}
function send(){
    var title = document.getElementById("temp_title").innerHTML;
	var relay_content = document.getElementById("areaContent").value;
	if (relay_content == ""){
		alert("回复内容不能为空");
	}else{
		var dataurl = JSON.stringify({"content": relay_content});
			$.ajax({
                    url:"http://127.0.0.1:5000/relay_leave/"+title,
                    type:"POST",
                    contentType:"application/json; charset=utf-8",
                    data: dataurl,
                    success:function (data) {
                         if (data == "ok"){
                            document.getElementById("relayContent").style.display = 'none';
                            window.location.href = "/relay_leave/"+title;
                         }
                    }
            });

	}
}