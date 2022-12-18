/*jslint sloppy: false*/
function checkAccount(){
	var account = document.getElementById("register_name").value;
	var reg = new RegExp(/^(?![^a-zA-Z]+$)(?!\D+$)(?=.*[_])/);
	if (account == ""){
		alert("登录账号不能为空");
		return false
	}else if (reg.test(account) == false){
		alert("登录账户包含数字、英文、下划线");
		return false
	}else{
		return account
	}	
}
function checkPassword(){
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
function checkNewPassword(){
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
function checkTelephone(){
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
function registerCommit(){
	var account;
	var pwd;
	var pwd1;
	var telephone;
	if (checkAccount()!=false){
		if (checkPassword()!=false){
			if (checkNewPassword()!=false){
				if (checkTelephone()!=false){
					account = checkAccount();
					pwd = checkPassword();
					pwd1 = checkNewPassword();
					telephone = checkTelephone();
					var dataurl = JSON.stringify({"account": account, "pwd": pwd, "pwd1": pwd1, "telephone": telephone});
                    $.ajax({
                            url:"http://127.0.0.1:5000/register/",
                            type:"POST",
                            contentType:"application/json; charset=utf-8",
                            data: dataurl,
//                            async:false,
                            success:function (data) {
                                if (data == "ok"){
                                    alert("注册成功");
                                    window.location.href = "/login";
                                }
                                if (data == "error"){
                                    alert("用户已存在");
                                }
                            }
                     });
				}
			} 
		}
	}

}