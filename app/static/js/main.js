// 在页面上弹出Toast
function Toast(msg, duration) {
    duration = isNaN(duration) ? 3000 : duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText = "max-width:60%;min-width: 150px;padding:0 14px;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 4px;position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);z-index: 999999;background: rgba(0, 0, 0,.7);font-size: 16px;";
    document.body.appendChild(m);
    setTimeout(function () {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function () {
            document.body.removeChild(m)
        }, d * 1000);
    }, duration);
}

$(function () {

    //锚点跳转滑动效果
    $(".nav-link").bind("click touch", function () {
        //根据a标签的href转换为id选择器，获取id元素所处的位置，并高度减50px（这里根据需要自由设置）
        $('html,body').animate({scrollTop: ($($(this).attr('href')).offset().top - 50)}, 500);
    });

    $("#scan-and-try-it").popover({
        trigger: 'manual',
        placement: 'top', //placement of the popover. also can use top, bottom, left or right
        title: '<div style="text-align:center; color:black; font-size:14px;">打开微信扫描</div>', //this is the top title bar of the popover. add some basic css
        html: true, //needed to show html of course
        content: '<div id="popOverBox"><img src="https://ytools.xyz/gh_62c9c4c58680_258.jpg" width="200" height="200" /></div>', //this is the content of the html box. add the image here or anything you want really.
        animation: false
    }).on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(this).siblings(".popover").on("mouseleave", function () {
            $(_this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide")
            }
        }, 100);
    });

    $("#send-feedback").click(function () {
        $.get({
            url: "https://www.ytools.xyz/api/v1/user/ip",
            jsonp: "callback",
            crossDomain: true,
            success: function (res) {
                console.log("来访者IP为：" + res.info[0].ip);
                var ip = res.info[0].ip;
                var content = $("#contactFormEmail").val();
                var contact = $("#feedbackContent").val();

                var data = {
                    "uid": ip,
                    "content": content,
                    "contact": contact,
                    "origin": "1"
                };

                $.post({
                    url: "https://www.ytools.xyz/api/v1/user/feedback/create",
                    jsonp: "callback",
                    crossDomain: true,
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    data: JSON.stringify(data),
                    success: function (res) {
                        console.log(res);
                        Toast(res['msg'], 2000);
                    },
                    error: function (err) {
                        Toast(res.msg, 2000);
                    }
                })
            }
        });
    });
});