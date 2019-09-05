$(function () {
    $('#main_menu').metisMenu();

    $('#child_menu a,#brandname').on('click', function (evt) {
        $("#currentpage").val($(this).attr('href'));
        getSubView($(this).attr('href'));
        evt.preventDefault();});
    var clk=self.setInterval("refresh()",6000);
  });
function getSubView(url) {
    $.ajax(url, {
        method: "GET"
    })
    .then(function (response) {
        if (response.redirect) {
            if (response.authenticated) {
                window.open(response.url, "_blank");
            } else {
                location.href = response.url;
            }
        } else {
            $('#content-wrapper').html(response);
        }
    }, function (error) {
        console.log(error);
    })
}
function refresh() {
    url=$("#currentpage").val();
    en=$("#enrefresh").val();
    if(url==="/doaudit" && Number(en)) {
        getSubView("/doaudit");
        scrollTo(0,document.body.scrollHeight);
    }
}