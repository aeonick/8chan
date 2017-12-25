function setTempCookie(){var d = new Date();d.setTime(d.getTime()+15000);document.cookie = "cold=1; expires=" + d.toGMTString();return 1;}
function getCookie(){var name = "cold=";var ca = document.cookie.split(';');for(var i=0; i<ca.length; i++){var c = ca[i].trim();if (c.indexOf(name)==0) return c.substring(name.length,c.length);}return "";}
function checkShow(){
    var winH = $(window).scrollTop()+$(window).height()+400;
    $("img.lazyimg").each(function(){
        if($(this).attr('state')==0){return;}
        var imgurl = $(this).attr("hide");
        if(!imgurl){$(this).attr('state',0)}
        if($(this).offset().top<winH && imgurl){
            $(this).attr("src",imgurl);
            $(this).fadeIn(600);
            $(this).attr("state",0);
        }
    });
}
$(window).on('scroll', function(){checkShow();});
function confirm0() {
    $("#tnow").val(tnow);
    if(getCookie()){alert("本版块发文最短间隔为15秒，请稍后再发");return false;}
    if($("#content").val().length<4){alert("内容不能少于四个字");return false;} 
    if($("#section").val()==0){alert("请先选择版块");return false;}
    setTempCookie();
};
function confirm1() {
    $("#tnow").val(tnow);
    if(getCookie()){alert("本版块发文最短间隔为15秒，请稍后再发");return false}
    if($("#content").val().length<2){alert("内容不能少于两个字");return false;} 
    $("#section").removeAttr("disabled");
    $("#section").val('0');
    setTempCookie();
};
$(function(){
    tnow=0;
    $("repinfo").each(function(){
        var num=Math.max($(this).attr("num")-5,0);
        if(num!=0){$(this).html("回应有"+num+"条被省略，点击查看所有回应");}
    });
    $("#content").click(function(){if(!tnow){tnow=parseInt((new Date().getTime())/1000);}});
    checkShow();
    $("img.lazyimg").click(function(){
        $("mask").fadeIn(200);
        var imgsrc = $(this).attr("src");
        document.getElementById("mask").innerHTML='<span></span><a target="_blank" href="'+imgsrc+'"><img title="点击查看原图" src="'+imgsrc+'"></a>';
    });
    $("mask").click(function(){
        $("mask").fadeOut(200);
    });
});