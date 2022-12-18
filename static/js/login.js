//function accountsCheck(){
//	var login_account = document.getElementById("publicLoginId").vlaue;
//	alert(login_account.length);
//	if (login_account==""){
//		alert("请输入用户名/手机号");
//	}
//}
function passwordCheck(){
	var pwd = document.getElementById("publicPassword").value;
	var pwdLength = pwd.length;
	if (pwdLength == 0){
		alert("密码不能为空");
		return false;
	}else{
		return pwd;
	}
}
function accountsCheck() { 
    var account = document.getElementById("publicLoginId").value;
	var accountLength = account.length;
	if (accountLength == 0){
		alert("请输入用户名/手机号");
		return false;
	}else{
		return account;
	}
} 
function login(){
	var account;
	var pwd;
	if (accountsCheck() != false){
		if (passwordCheck() != false){
			account = accountsCheck();
			pwd = passwordCheck();
			var dataurl = JSON.stringify({"account": account, "pwd": pwd});
			$.ajax({
                    url:"http://127.0.0.1:5000/login",
                    type:"POST",
                    contentType:"application/json; charset=utf-8",
                    data: dataurl,
//                  async:false,
                    success:function (data) {
                         if (data == "ok"){
                            alert("登录成功");
                            window.location.href = "/publish_leave";
                         }
                         if (data == "error"){
                            alert("用户名或密码错误");
                         }
                    }
            });
		}	
	}
}
function jumpToRegister(){
	window.location.href = "/register/";
}
function jumpToForget(){
	window.location.href = "/forget";
}