var player = document.getElementById('videoElement');
var userid = getCookie("userid")
var username = getCookie("username")
var hrefstr = window.location.href
var roomid = hrefstr.split("=")[2]
var wstest = new WebSocket("ws://127.0.0.1:8888/wstest");
var permittest = new WebSocket("ws://127.0.0.1:8888/permittest");
var chatsocket = new WebSocket("ws://127.0.0.1:8888/chat");
var handsocket = new WebSocket("ws://127.0.0.1:8888/hand");
var initsocket = new WebSocket("ws://127.0.0.1:8888/init/?roomid=" + roomid + "&username=" + username);

// initsocket.onopen = function () {
//     var apply_msg = {
//         room: roomid,
//         from: userid
//     }
//     apply_msg = eval(apply_msg);
//     apply_msg_str = JSON.stringify(apply_msg);
//     initsocket.send(apply_msg_str);
// }

chatsocket.onmessage = function (e) {
    ev = JSON.parse(e.data);
    var target_room = ev.room
    var at = ev.at
    var from = ev.from
    var content = ev.content
    if (self.roomid == target_room) {
        if (at == "") {
            $('#chatarea').append("<p>" + from + "说:" + content + "</p>");
        }
        else {
            $('#chatarea').append("<p>" + from + "@" + at + "说:" + content + "</p>");
        }
    }
}

permittest.onmessage = function (e) {
    ev = JSON.parse(e.data);
    var target_room = ev.room
    var target_user = ev.user
    if (self.userid == target_user && self.roomid == target_room) {
        $("#lock").text("权限已开启");
    }
}

$('#watchScreenButton').click(pullScreen)
function pullScreen() {
    var target_userid = $('#target_userid').val()
    if (flvjs.isSupported()) {
        var flvPlayer = flvjs.createPlayer({
            type: 'flv',
            url: 'http://192.168.223.128:19351/live?port=1935&app=myapp&stream=room' + roomid + "user" + target_userid + "Screen"
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
    }
}

$('#watchVideoButton').click(pullVideo)
function pullVideo() {
    var target_userid = $('#target_userid').val()
    if (flvjs.isSupported()) {
        var flvPlayer = flvjs.createPlayer({
            type: 'flv',
            url: 'http://192.168.223.128:19351/live?port=1935&app=myapp&stream=room' + roomid + "user" + target_userid + "Video"
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
    }
}

function getCookie(name) {
    var cookies = document.cookie;
    var list = cookies.split("; ");     // 解析出名/值对列表

    for (var i = 0; i < list.length; i++) {
        var arr = list[i].split("=");   // 解析出名和值
        if (arr[0] == name)
            return decodeURIComponent(arr[1]);   // 对cookie值解码
    }
    return "";
}

function flv_start() {
    flvPlayer.load()
}
function flv_finish() {
    flvplayer.pause();
    flvPlayer.unload()
}
function flv_pause() {
    player.pause();
}

function flv_destroy() {
    player.pause();
    player.unload();
    player.detachMediaElement();
    player.destroy();
    player = null;
}

function flv_seekto() {
    player.currentTime = parseFloat(document.getElementsByName('seekpoint')[0].value);
}

$(document).ready(function () {

    $("#whiteboardButton").click(function () {
        var lock = document.getElementById("lock").innerText;
        if (lock == "权限已开启") {
            $("#whiteboardElement").show();
            $("#videoElement").hide();
            $("#signElement").hide();
            $("#closewhiteboard").show();
            $("#whiteboard").hide();
        }
    });

    $("#closewhiteboardButton").click(function () {

        $("#whiteboardElement").hide();
        $("#videoElement").show();
        $("#signElement").hide();
        $("#closewhiteboard").hide();
        $("#whiteboard").show();

    });

    $("#shareScreenButton").click(function () {
        var lock = document.getElementById("lock").innerText;
        if (lock == "权限已开启") {
            $("#quitShareScreen").show();
            $("#shareScreen").hide();
            window.PyHandler.init_home('2|' + roomid + "|" + userid)
            flv_start()
        }

    });
    $("#quitShareScreenButton").click(function () {
        $("#quitShareScreen").hide();
        $("#shareScreen").show();
        window.PyHandler.init_home('5|' + roomid + "|" + userid)
        flv_finish()
    });

    $("#openMicoButton").click(function () {
        var lock = document.getElementById("lock").innerText;
        if (lock == "权限已开启") {
            $("#closeMico").show();
            $("#openMico").hide();
            window.PyHandler.init_home('3|' + roomid + "|" + userid)
            flv_start()
        }
    });
    $("#closeMicoButton").click(function () {
        $("#closeMico").hide();
        $("#openMico").show();
        window.PyHandler.init_home('6|' + roomid + "|" + userid)
        flv_finish()
    });

    $("#openVideoButton").click(function () {
        var lock = document.getElementById("lock").innerText;
        if (lock == "权限已开启") {
            $("#quitshareVideo").show();
            $("#shareVideo").hide();
            window.PyHandler.init_home('4|' + roomid + "|" + userid)
            flv_start()
        }
    });
    $("#closeVideoButton").click(function () {
        $("#quitshareVideo").hide();
        $("#shareVideo").show();
        window.PyHandler.init_home('7|' + roomid + "|" + userid)
        flv_finish()
    });

    $("#testbutton").click(function () {
        var apply_msg = {
            room: roomid,
            user: userid
        }
        apply_msg = eval(apply_msg);
        apply_msg_str = JSON.stringify(apply_msg);
        wstest.send(apply_msg_str);
    });

    $("#sendbutton").click(function () {
        var at = $('#at').val()
        var content = $('#content').val()

        var permit_msg = {
            room: roomid,
            from: username,
            at: at,
            content: content
        }

        permit_msg = eval(permit_msg);
        permit_msg_str = JSON.stringify(permit_msg);
        chatsocket.send(permit_msg_str);
        $('#at').val("")
        $('#content').val("")
    });

    $("#handbutton").click(function () {
        var date = new Date();
        //时 getHours()：(0 ~ 23)
        var hour = date.getHours();
        //分 getMinutes()： (0 ~ 59)
        var minute = date.getMinutes();
        //秒 getSeconds()：(0 ~ 59)
        var second = date.getSeconds();
        var time_str = hour + ":" + minute + ":" + second
        var permit_msg = {
            room: roomid,
            from: username,
            time: time_str
        }
        permit_msg = eval(permit_msg);
        permit_msg_str = JSON.stringify(permit_msg);
        handsocket.send(permit_msg_str);
    });

    $("#signButton").click(function () {
        $("#signElement").show();
        $("#videoElement").hide();
        $("#whiteboardElement").hide();
        $("#closesign").show();
        $("#sign").hide();
    });

    $("#closesignButton").click(function () {
        $("#whiteboardElement").hide();
        $("#signElement").hide();
        $("#videoElement").show();
        $("#closesign").hide();
        $("#sign").show();
    });

});

