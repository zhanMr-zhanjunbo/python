function consultSubmit(){
//	alert("hello");
	var title = document.getElementById("title").value;
	var content = document.getElementById("contentArea").value;
	var name = document.getElementsByName("public");
	var i;
	var isPublic;
	if (title == ""){
		alert("标题不能为空");
	}else if (content == ""){
		alert("内容不能为空");
	}else{
		for(i=0;i<name.length;i++){
			if (name[i].checked){
				isPublic = name[i].value;
			}
		}
		var dataurl = JSON.stringify({"title": title, "content": content, "is_public": isPublic});
        $.ajax({
                url:"http://127.0.0.1:5000/publish_leave",
                type:"POST",
                contentType:"application/json; charset=utf-8",
                data: dataurl,
//              async:false,
                success:function (data) {
                            if (data == "ok"){
                                alert("发布成功");
                            }
                }
                });
	}
}
function reset(){
	document.getElementById("title").value = "";
	document.getElementById("contentArea").value = "";
}