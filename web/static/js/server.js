let server_List1 = ""

var URL = ""

setTimeout(function showTime() {
    $("#board_fog").hide()
}, 2000);

function getList() {
    //获取所有服务器名称和id
    $.ajax({
        type: "get",
        async: false,
        url: URL + "/server",
        dataType: "json",
        success: function (res) {
            server_List1 = res
            $.ajax({
                url: URL + "/server/show/" + res[0].id,
                dataType: 'json',
                method: 'GET',
                success: function (res) {
                    $("#mysql_ip").val(res.mysql_ip)
                    $("#mysql_password").val(res.mysql_password)
                    $("#mysql_port").val(res.mysql_port)
                    $("#mysql_username").val(res.mysql_username)
                    $("#oracle_db").val(res.oracle_db)
                    $("#oracle_ip").val(res.oracle_ip)
                    $("#oracle_password").val(res.oracle_password)
                    $("#oracle_port").val(res.oracle_port)
                    // $("#oracle_type").val(res.oracle_type)
                    $(".form-group input[type='radio']:checked").removeAttr("checked");
                    $(".form-group input[value='" + res.oracle_type + "']").attr("checked", "true")
                    $("#oracle_username").val(res.oracle_username)
                    $("#server_ip").val(res.server_ip)
                    $("#server_name").val(res.server_name)
                    $("#server_port").val(res.server_port)
                    $("#server_pwd").val(res.server_pwd)
                    $("#server_username").val(res.server_username)
                    $("#sql_server_ip").val(res.sql_server_ip)
                    $("#sql_server_password").val(res.sql_server_password)
                    $("#sql_server_port").val(res.sql_server_port)
                    $("#sql_server_username").val(res.sql_server_username)
                }
            })
            $("#server_List").empty();
            $.each(res, function (index, item) {
                $("#server_List").append("<div class='server_box'  onclick='getID(" + item.id + ")' index='" + index + "' id='server_" + item.id + "'>" + item.server_name
                    + "<a class='destroy' onclick='destroy(" + item.id + ")'>删除</a>" + "</div>");
            });
            $(".idChecked").removeClass("idChecked")
            $("[id=server_" + res[0].id + "]").addClass("idChecked")
        }
    });
}

getList()

$("#add_submit").hide()
$("#fog").hide()

$("#add_server").click(function () {
    $(".idChecked").removeClass("idChecked")
    $("#mysql_ip").val("")
    $("#mysql_password").val("")
    $("#mysql_port").val("3306")
    $("#mysql_username").val("")
    $("#oracle_db").val("")
    $("#oracle_ip").val("")
    $("#oracle_password").val("")
    $("#oracle_port").val("1521")
    // $("#oracle_type").val("")
    $(".form-group input[type='radio']:checked").removeAttr("checked");
    $("#oracle_username").val("")
    $("#server_ip").val("")
    $("#server_name").val("")
    $("#server_port").val("22")
    $("#server_pwd").val("")
    $("#server_username").val("")
    $("#sql_server_ip").val("")
    $("#sql_server_password").val("")
    $("#sql_server_port").val("1433")
    $("#sql_server_username").val("")
    $("#update_submit").hide()
    $("#add_submit").show()
})

//新增
$("#add_submit").click(function () {
    if ($("#server_name").val() == "") {
        $("#fog").show()
        $("#add_name").show()
        return
    }

    let m = $("#mysql_ip").val().split(".")
    let o = $("#oracle_ip").val().split(".")
    let s = $("#server_ip").val().split(".")
    let q = $("#sql_server_ip").val().split(".")

    if ($("#mysql_ip").val() != "") {
        if (m.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < m.length; j++) {
            if (m[j] < 0 || m[j] > 255 || m[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }

    if ($("#oracle_ip").val() != "") {
        if (o.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < o.length; j++) {
            if (o[j] < 0 || o[j] > 255 || o[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }
    if ($("#server_ip").val() != "") {
        if (s.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < s.length; j++) {
            if (s[j] < 0 || s[j] > 255 || s[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }
    if ($("#sql_server_ip").val() != "") {
        if (q.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < q.length; j++) {
            if (q[j] < 0 || q[j] > 255 || q[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }

    $.ajax({
        url: URL + "/server/create",
        dataType: 'json',
        contentType: 'application/json',
        method: 'POST',
        data: JSON.stringify({
            "mysql_ip": $("#mysql_ip").val(),
            "mysql_password": $("#mysql_password").val(),
            "mysql_port": $("#mysql_port").val(),
            "mysql_username": $("#mysql_username").val(),
            "oracle_db": $("#oracle_db").val(),
            "oracle_ip": $("#oracle_ip").val(),
            "oracle_password": $("#oracle_password").val(),
            "oracle_port": $("#oracle_port").val(),
            // "oracle_type": $("#oracle_type").val(),
            "oracle_type": $(".form-group input[type='radio']:checked").val(),
            "oracle_username": $("#oracle_username").val(),
            "server_ip": $("#server_ip").val(),
            "server_name": $("#server_name").val(),
            "server_port": $("#server_port").val(),
            "server_pwd": $("#server_pwd").val(),
            "server_username": $("#server_username").val(),
            "sql_server_ip": $("#sql_server_ip").val(),
            "sql_server_password": $("#sql_server_password").val(),
            "sql_server_port": $("#sql_server_port").val(),
            "sql_server_username": $("#sql_server_username").val()
        }),
        success: function (res) {
            if (res.code == 1) {
                $("#add_success").show()
                $("#fog").show()
                $('#lastServerSelect').val(server_List[0].id)
                parent.location.reload();
                getList()
            } else {
                $("#add_fail").show()
                $("#fog").show()
            }
        },
        error: function () {
            $("#add_fail").show()
            $("#fog").show()
        }
    })
})

//未填写服务器名字
function addName() {
    $("#add_name").hide()
    $("#fog").hide()
}

function addIp() {
    $("#add_ip").hide()
    $("#fog").hide()
}

function addSuccess() {
    $("#add_success").hide()
    $("#fog").hide()
}

function addFail() {
    $("#add_fail").hide()
    $("#fog").hide()
}

var currentId = ""



//查看
function getID(id) {
    $("#update_submit").show()
    $("#add_submit").hide()
    currentId = id
    $(".idChecked").removeClass("idChecked")
    $("[id=server_" + id + "]").addClass("idChecked")
    // console.log($("[id=server_" + id + "]").attr("class"))
    $.ajax({
        url: URL + "/server/show/" + id,
        dataType: 'json',
        method: 'GET',
        success: function (res) {
            $("#mysql_ip").val(res.mysql_ip)
            $("#mysql_password").val(res.mysql_password)
            $("#mysql_port").val(res.mysql_port)
            $("#mysql_username").val(res.mysql_username)
            $("#oracle_db").val(res.oracle_db)
            $("#oracle_ip").val(res.oracle_ip)
            $("#oracle_password").val(res.oracle_password)
            $("#oracle_port").val(res.oracle_port)
            // $("#oracle_type").val(res.oracle_type)
            $(".form-group input[type='radio']:checked").removeAttr("checked");
            $(".form-group input[value='" + res.oracle_type + "']").attr("checked", "true")
            $("#oracle_username").val(res.oracle_username)
            $("#server_ip").val(res.server_ip)
            $("#server_name").val(res.server_name)
            $("#server_port").val(res.server_port)
            $("#server_pwd").val(res.server_pwd)
            $("#server_username").val(res.server_username)
            $("#sql_server_ip").val(res.sql_server_ip)
            $("#sql_server_password").val(res.sql_server_password)
            $("#sql_server_port").val(res.sql_server_port)
            $("#sql_server_username").val(res.sql_server_username)
        }
    })
}

$(".form-group input[type='radio']").click(function () {
    $(".form-group input[type='radio']:checked").removeAttr("checked");
    $(this).attr("checked", "true")
})

//更新
function update() {

    if ($("#server_name").val() == "") {
        $("#add_name").show()
        $("#fog").show()
        return
    }

    let m = $("#mysql_ip").val().split(".")
    let o = $("#oracle_ip").val().split(".")
    let s = $("#server_ip").val().split(".")
    let q = $("#sql_server_ip").val().split(".")

    if ($("#mysql_ip").val() != "") {
        if (m.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < m.length; j++) {
            if (m[j] < 0 || m[j] > 255 || m[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }

    if ($("#oracle_ip").val() != "") {
        if (o.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < o.length; j++) {
            if (o[j] < 0 || o[j] > 255 || o[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }
    if ($("#server_ip").val() != "") {
        if (s.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < s.length; j++) {
            if (s[j] < 0 || s[j] > 255 || s[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }
    if ($("#sql_server_ip").val() != "") {
        if (q.length != 4) {
            $("#add_ip").show()
            $("#fog").show()
            return
        }
        for (var j = 0; j < q.length; j++) {
            if (q[j] < 0 || q[j] > 255 || q[j] == "") {
                $("#add_ip").show()
                $("#fog").show()
                return
            }
        }
    }
    $("#edit_confirm").show()
    $("#fog").show()
}

function editYes() {
    $("#edit_confirm").hide()
    $("#fog").hide()
    $.ajax({
        url: URL + "/server/update",
        // dataType: 'json',
        contentType: 'application/json',
        method: 'POST',
        data: JSON.stringify({
            "id": currentId,
            "mysql_ip": $("#mysql_ip").val(),
            "mysql_password": $("#mysql_password").val(),
            "mysql_port": $("#mysql_port").val(),
            "mysql_username": $("#mysql_username").val(),
            "oracle_db": $("#oracle_db").val(),
            "oracle_ip": $("#oracle_ip").val(),
            "oracle_password": $("#oracle_password").val(),
            "oracle_port": $("#oracle_port").val(),
            // "oracle_type": $("#oracle_type").val(),
            "oracle_type": $(".form-group input[type='radio']:checked").val(),
            "oracle_username": $("#oracle_username").val(),
            "server_ip": $("#server_ip").val(),
            "server_name": $("#server_name").val(),
            "server_port": $("#server_port").val(),
            "server_pwd": $("#server_pwd").val(),
            "server_username": $("#server_username").val(),
            "sql_server_ip": $("#sql_server_ip").val(),
            "sql_server_password": $("#sql_server_password").val(),
            "sql_server_port": $("#sql_server_port").val(),
            "sql_server_username": $("#sql_server_username").val()
        }),
        success: function (res) {
            if (res.code == 1) {
                $("#edit_success").show()
                $("#fog").show()
                getID(currentId)
                $('#lastServerSelect').val(server_List[0].id)
                parent.location.reload();
                getList()
            } else {
                $("#edit_fail").show()
                $("#fog").show()
            }
        },
        error: function () {
            $("#edit_fail").show()
            $("#fog").show()
        }
    })
}

function editSuccess() {
    $("#edit_success").hide()
    $("#fog").hide()
}

function editFail() {
    $("#edit_fail").hide()
    $("#fog").hide()
}


function editCancle() {
    $("#edit_confirm").hide()
    $("#fog").hide()
}

var delete_id = ""

//删除
function destroy(id) {
    $("#delete_confirm").show()
    $("#fog").show()
    delete_id = id
}

function deleteYes() {
    $("#delete_confirm").hide()
    $("#fog").hide()
    $.ajax({
        url: URL + "/server/destroy/" + delete_id,
        dataType: 'json',
        method: 'GET',
        success: function (res) {
            if (res.code == 1) {
                $("#delete_success").show()
                $("#fog").show()
                $('#lastServerSelect').val(server_List[0].id)
                parent.location.reload();
                getList()
            } else {
                $("#delete_fail").show()
                $("#fog").show()
            }
        },
        error: function () {
            $("#delete_fail").show()
            $("#fog").show()
        }
    })
}

function deleteCancle() {
    $("#delete_confirm").hide()
    $("#fog").hide()
}


function deleteSuccess() {
    $("#delete_success").hide()
    $("#fog").hide()
}

function deleteFail() {
    $("#delete_fail").hide()
    $("#fog").hide()
}