function modifyTelephone(){
	var telephone = document.getElementById("telephone").value;
	var reg = new RegExp(/^[1][3,4,5,7,8][0-9]{9}$/);
	if (telephone == ""){
		alert("手机号不能为空");
		return false
	}else if (telephone.length < 11){
		alert("手机号不合法");
		return false
	}else if (reg.test(telephone) == false){
		alert("手机号不合法");
		return false
	}else{
		return telephone
	}
}
function modifyPassword(){
	var pwd = document.getElementById("password").value;
	var reg = new RegExp(/^(?![^a-zA-Z]+$)(?!\D+$)(?=.*[~!@#$%^&*()_+`\-=])/);
	if (pwd == ""){
		alert("密码不能为空");
		return false
	}else if (pwd.length < 8){
		alert("密码长度不少于8位");
		return false
	}else if (reg.test(pwd) == false){
		alert("必须包含字母，数字，特殊符号");
		return false
	}else{
		return pwd
	}
}
function modifyNewPassword(){
	var pwd = document.getElementById("password").value;
	var pwd1 = document.getElementById("password1").value;
	var reg = new RegExp(/^(?![^a-zA-Z]+$)(?!\D+$)(?=.*[~!@#$%^&*()_+`\-=])/);
	if (pwd1 == ""){
		alert("确认密码不能为空");
		return false
	}else if (pwd1.length < 8){
		alert("确认密码长度不少于8位");
		return false
	}else if (reg.test(pwd1) == false){
		alert("必须包含字母，数字，特殊符号");
		return false
	}else if (pwd != pwd1){
		alert("两次输入密码不一致");
		return false
	}else{
		return pwd1
	}
}
function modifyCommit(){
	var telephone;
	var pwd;
	var pwd1;
	if (modifyTelephone()!=false){
		if (modifyPassword()!=false){
			if (modifyNewPassword()!=false){
					telephone = modifyTelephone();
					pwd = modifyPassword();
					pwd1 = modifyNewPassword();
					var dataurl = JSON.stringify({"telephone": telephone, "pwd": pwd, "pwd1": pwd1})
					$.ajax({
                            url:"http://127.0.0.1:5000/forget",
                            type:"POST",
                            contentType:"application/json; charset=utf-8",
                            data: dataurl,
//                            async:false,
                            success:function (data) {
                                if (data == "ok"){
                                    alert("修改成功");
                                window.location.href = "/login";
                                }
                                if (data == "error"){
                                    alert("用户不存在");
                                }
                            }
                     });
			} 
		}
	}	
}