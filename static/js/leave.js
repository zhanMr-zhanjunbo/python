function getConsultList(){
	title = document.getElementById("title_msg").value;
	start_time = document.getElementById("start_time").value;
	end_time = document.getElementById("end_time").value;
	var customDate = new Date(start_time);
	var start_year = customDate.getFullYear();
	var start_month = customDate.getMonth() + 1;
	var start_day = customDate.getDate();
	var start_hours = customDate.getHours();
	var start_date = start_year+"-"+start_month+"-"+start_day+" "+start_hours;
	var customTime = new Date(end_time);
	var end_year = customTime.getFullYear();
	var end_month = customTime.getMonth() + 1;
	var end_day = customTime.getDate();
	var end_hours = customTime.getHours();
	var end_date = end_year+"-"+end_month+"-"+end_day+" "+end_hours;
	$.ajax({
        url:"http://127.0.0.1:5000/my_leave",
        type:"GET",
        contentType:"application/json; charset=utf-8",
        data: "title="+title+"&start_date="+start_date+"&end_date="+end_date,
        success:function (data) {
            if (data == "error"){
                alert("未查询到数据");
            }else if (data == "ok"){
                window.location.href = "/my_leave";
            }else{
                var html='';
                for(var i = 0; i < data.length; i++){
                    if(i<8){
                        html += '<a href="" style="display:inline-block;width: 700px;clear:left" class="titles">'+
                        data[i][0]+'</a>'
                    }else{
                        html += '<a href="" style="display:inline-block;width: 700px;clear:left;display: none" class="titles">'+
                        data[i][0]+'</a>'
                    }
                }
            document.getElementById("newsMsgList_con").innerHTML=html;
           }
        }
    });
}
 