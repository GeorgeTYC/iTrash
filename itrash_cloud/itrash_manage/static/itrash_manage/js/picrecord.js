$(function() {
    $(".re_lbl").on("click",function(evt){
        var pid=($(this).data("id"));
        $("#re_"+pid).text("正在处理");
        $("#re_"+pid).attr("disabled",true);
        postReLbl(pid);
    });
    $(".pic-delete").on("click",function (evt) {
        var pid=($(this).data("id"));
        postDelete(pid);
        $("<div style='width: 100%;height: 100%;z-index:1000;background-color:black;filter:alpha(Opacity=20);-moz-opacity:0.2;opacity: 0.2;position:absolute;left:0; top:0'></div>").insertBefore($(this).parents(".card-main"))
    })
});
function postReLbl(pid) {
    url="/picrelbl";
    var csrftoken = $.cookie('csrftoken');
    $.ajax(url, {
        type: "POST",
        data:{pid:pid},
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        if(response.succ)
            $("#re_"+pid).text(response.msg);
        else
            console.log(response.msg)
    }, function (error) {
        console.log(error);
    })
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