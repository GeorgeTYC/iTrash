$(function() {
    $(".changeUpload").on("click",function(evt){
        var st=$(".changeUploadVal").find(":checked").val();
        changeUpload(st);
    });
});
changeUpload=function(st) {
    url="/control";
    var csrftoken = $.cookie('csrftoken');
    $.ajax(url, {
        type: "POST",
        data:{st:st},
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        getSubView(url);
    }, function (error) {
        console.log(error);
    })
};
