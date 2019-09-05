$(function() {
    var initrefresh=$("#enrefresh").val();
    if(Number(initrefresh)){
            $(".togglerefresh").addClass("text-gray-800")
        }else{
        $(".togglerefresh").addClass("text-gray-300")
    }
    $(".togglerefresh").on("click",function (evt) {
        var newval=1-$("#enrefresh").val();
        $("#enrefresh").val(newval);
        if(newval){
            $(".togglerefresh").removeClass("text-gray-300").addClass("text-gray-800")
        }else {
            $(".togglerefresh").addClass("text-gray-300").removeClass("text-gray-800")
        }
    });
    $(".totop").on("click",function (evt) {
        scrollTo(0,0);
    })
    $(".audit_yes").on("click",function(evt){
        var pred=$(this).data("pred");
        var pid=($(this).data("id"));
        $("#bar_"+pid).html("<p>正在处理</p>").css("height","38px");
        postAudit(pid,pred);
    });
    $(".audit_sel").on("change",function (evt) {
        var pid=($(this).data("id"));
        var pred=$(this).find(':selected').val();
        $("#bar_"+pid).html("<p>正在处理</p>").css("height","38px");
        postAudit(pid,pred);
    });
    $(".setLbl").on("click",function(evt){
        var lbl=$("#lblList").val();
        postchangeLbl(lbl);
    });
    $(".pic-delete").on("click",function (evt) {
        var pid=($(this).data("id"));
        postDelete(pid);
        $("<div style='width: 100%;height: 100%;z-index:200;background-color:black;filter:alpha(Opacity=20);-moz-opacity:0.2;opacity: 0.2;position:absolute;left:0; top:0'></div>").insertBefore($(this).parents(".card-main"))
    })
});
function postAudit(pid,real) {
    url="/doaudit";
    var csrftoken = $.cookie('csrftoken');
    $.ajax(url, {
        type: "POST",
        data:{pid:pid,real:real},
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        $("#bar_"+pid).html("<p>"+response.msg+"</p>").css("height","38px")
    }, function (error) {
        console.log(error);
    })
}
function postchangeLbl(lbl) {
    url="/changeLbl";
    var csrftoken = $.cookie('csrftoken');
    $.ajax(url, {
        type: "POST",
        data:{lblStr:lbl},
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        if(response.succ===1)
            $("#alert-placeholder").html("<div class=\"alert alert-success alert-dismissible fade show alert-top\" role=\"alert\">"+response.msg+"<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        else
            $("#alert-placeholder").html("<div class=\"alert alert-warning alert-dismissible fade show alert-top\" role=\"alert\">"+response.msg+"<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
    }, function (error) {
        console.log(error);
    });
}
function postDelete(pid) {
    url="/deletePic";
    var csrftoken = $.cookie('csrftoken');
    $.ajax(url, {
        type: "POST",
        data:{pid:pid},
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        if(response.succ===1)
            $("#alert-placeholder").html("<div class=\"alert alert-success alert-dismissible fade show alert-top\" role=\"alert\">"+response.msg+"<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        else
            $("#alert-placeholder").html("<div class=\"alert alert-warning alert-dismissible fade show alert-top\" role=\"alert\">"+response.msg+"<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
    }, function (error) {
        console.log(error);
    });
}
