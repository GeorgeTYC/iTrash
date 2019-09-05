$(function(){
    var url="/stat/1";
    var csrftoken = $.cookie('csrftoken');
    $.ajax(url, {
        type: "POST",
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        draw_piechart(response.trashCount)
    });
    var url2="stat/2";
    $.ajax(url2, {
        type: "POST",
        headers:{'X-CSRFtoken':csrftoken}
    })
    .then(function (response) {
        draw_barchart(response.trashCount)
    });
    $(".doqueryTrash").on("click",function (evt) {
        var q_url="/query/"+$("#queryTrash").val();
        $.ajax(q_url,{
            type:"GET",
            headers:{'X-CSRFtoken':csrftoken}
        }).then(
            function (response) {
                $(".modal-body").html(response)
            }
        )
    })
} );

function draw_barchart(trashCount) {
    var ctx = document.getElementById("myBarChart");
    data = {
        labels: ["有害垃圾","可回收垃圾","干垃圾", "湿垃圾"],
        datasets: [{
            data: trashCount,
            backgroundColor: ['#dc3545', '#1cc88a', '#4e73df', '#36b9cc',],
            hoverBackgroundColor: ['#cd3e3f', '#17a673','#2e59d9', '#2c9faf',],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    };
    options = {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgba(255,255,255,0.8)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: true,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    };
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}
function draw_piechart(trashCount) {
    var ctx = document.getElementById("myPieChart");
    data = {
        labels: ["干垃圾", "可回收垃圾", "湿垃圾","有害垃圾"],
        datasets: [{
            data: trashCount,
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc','#dc3545'],
            hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf','#cd3e3f'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    };
    options = {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgba(255,255,255,0.8)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    };
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options
    });
}