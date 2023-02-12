var player = document.getElementById('videoElement');
userid = getCookie("userid")
var username = getCookie("username")
var hrefstr = window.location.href
var roomid = hrefstr.split("=")[2]
var wstest = new WebSocket("ws://127.0.0.1:8888/wstest");
var permittest = new WebSocket("ws://127.0.0.1:8888/permittest");
var chatsocket = new WebSocket("ws://127.0.0.1:8888/chat");
var handsocket = new WebSocket("ws://127.0.0.1:8888/hand");
var initsocket = new WebSocket("ws://127.0.0.1:8888/init/?roomid=" + roomid + "&username=" + username);

initsocket.onmessage = function (e) {
    ev = JSON.parse(e.data);
    var message = ev.message
    var room = ev.room
    if (self.roomid == room) {
        $('#chatarea').append("<p>" + message + "</p>");
    }
}

handsocket.onmessage = function (e) {
    ev = JSON.parse(e.data);
    var time_str = ev.time
    var from = ev.from
    var room = ev.room
    if (self.roomid == room) {
        $('#chatarea').append("<p>" + from + "在" + time_str + "发起了举手</p>");
    }
}

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

wstest.onmessage = function (e) {
    ev = JSON.parse(e.data);
    var target_room = ev.room
    var target_user = ev.user
    if (self.roomid == target_room) {
        var applyinfo = "学生" + target_user + "号请求授予权限"
        $("#applyreceive").text(applyinfo);
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

function flv_start(flvplayer) {
    flvplayer.load()
}
function flv_finish(flvplayer) {
    flvplayer.pause();
    flvplayer.unload()
    flvplayer.detachMediaElement()
    flvplayer.destroy()
    flvplayer = null

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
        $("#whiteboardElement").show();
        $("#videoElement").hide();
        $("#signElement").hide();
        $("#closewhiteboard").show();
        $("#whiteboard").hide();
    });

    $("#closewhiteboardButton").click(function () {
        $("#whiteboardElement").hide();
        $("#videoElement").show();
        $("#signElement").hide();
        $("#closewhiteboard").hide();
        $("#whiteboard").show();
    });

    $("#shareScreenButton").click(function () {
        $("#quitShareScreen").show();
        $("#shareScreen").hide();
        window.PyHandler.init_home('2|' + roomid + "|" + userid)
        flv_start(flvPlayer1)
    });
    $("#quitShareScreenButton").click(function () {
        $("#quitShareScreen").hide();
        $("#shareScreen").show();
        window.PyHandler.init_home('5|' + roomid + "|" + userid)
        flv_finish(flvPlayer1)
    });

    $("#openMicoButton").click(function () {
        $("#closeMico").show();
        $("#openMico").hide();
        window.PyHandler.init_home('3|' + roomid + "|" + userid)
        flv_start()
    });
    $("#closeMicoButton").click(function () {
        $("#closeMico").hide();
        $("#openMico").show();
        window.PyHandler.init_home('6|' + roomid + "|" + userid)
        flv_finish()
    });

    $("#openVideoButton").click(function () {
        $("#quitshareVideo").show();
        $("#shareVideo").hide();
        $("#TeacherVideoElement").show();
        $("#TeacherAvatar").hide();
        window.PyHandler.init_home('4|' + roomid + "|" + userid)
        flv_start(flvPlayer2)
    });
    $("#closeVideoButton").click(function () {
        $("#quitshareVideo").hide();
        $("#shareVideo").show();
        $("#TeacherVideoElement").hide();
        $("#TeacherAvatar").show();
        window.PyHandler.init_home('7|' + roomid + "|" + userid)
        flv_finish(flvPlayer2)
    });

    $("#permitButton").click(function () {
        var target_userid = $('#target_userid').val()
        var permit_msg = {
            room: roomid,
            user: target_userid
        }
        permit_msg = eval(permit_msg);
        permit_msg_str = JSON.stringify(permit_msg);
        permittest.send(permit_msg_str);
    });

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

