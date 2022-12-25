$(document).ready(function () {

    // 使用刚指定的配置项和数据显示图表。
    myChart2.setOption(BarOption2);
    myChart3.setOption(lineOption2);
    myChart1.setOption(lineOption);
    myChart4.setOption(BarOption);
    myChart5.setOption(BarOption3);
    myChart6.setOption(BarOption4);

})

var URL = ""

// 基于准备好的dom，初始化echarts实例
var myChart1 = echarts.init(document.getElementById('chart1'), null, {});
var myChart4 = echarts.init(document.getElementById('chart2'), null, {});
var myChart5 = echarts.init(document.getElementById('chart5'), null, {});
var myChart6 = echarts.init(document.getElementById('chart6'), null, {});
var myChart3 = echarts.init(document.getElementById('chart3'), null, {});
var myChart2 = echarts.init(document.getElementById('chart4'), null, {});

$('#nothing1').hide()
$('#nothing2').hide()
$('#nothing3').hide()
$('#nothing4').hide()
$('#nothing5').hide()
$('#nothing6').hide()

var selectValue = $("#lastTimeSelect").val();

let server_List = ""

getList()

function getList() {
    //获取所有服务器名称和id
    $.ajax({
        type: "get",
        async: false,
        url: URL + "/server",
        dataType: "json",
        success: function (res) {
            var select = $("#lastServerSelect")
            $.each(res, function (index, item) {
                select.append(new Option(item.server_name, item.id));  //在下拉菜单里添加元素
            });
            server_List = res
        }
    });
}

var lastServerSelect = server_List.findIndex(item => item.id == $('#lastServerSelect').val())

$('#lastServerSelect').change(() => {
    lastServerSelect = server_List.findIndex(item => item.id == $('#lastServerSelect').val())
    console.log(lastServerSelect)
    randomData()
});

$("#lastTimeSelect").change(() => {
    randomData($("#lastTimeSelect").val())
})

server_info = ""

let datas = []
let datas2 = []

// 拿取服务器信息
function randomData() {
    var time = ""
    $.ajax({
        type: "get",
        async: false,
        url: URL + "/server/data/" + server_List[lastServerSelect].id,
        dataType: "json",
        success: function (res) {
            var r = res.data
            server_info = r
            // console.log(res)
            if (r[0].x.length == 0) {
                $('#nothing1').show()
                $('#chart1').hide()
                $('#chart1Button1').hide()
            } else {
                $('#nothing1').hide()
                $('#chart1').show()
                $('#chart1Button1').show()
            }
            if (r[1].x.length == 0) {
                $('#nothing3').show()
                $('#chart3').hide()
                $('#chart1Button3').hide()
            } else {
                $('#nothing3').hide()
                $('#chart3').show()
                $('#chart1Button3').show()
            }
            if (r[2].x.length == 0) {
                $('#nothing2').show()
                $('#chart2').hide()
                $('#chart1Button2').hide()
            } else {
                $('#nothing2').hide()
                $('#chart2').show()
                $('#chart1Button2').show()
            }
            if (r[3].x.length == 0) {
                $('#nothing4').show()
                $('#chart4').hide()
                $('#chart1Button4').hide()
            } else {
                $('#nothing4').hide()
                $('#chart4').show()
                $('#chart1Button4').show()
            }
            if (r[4].x.length == 0) {
                $('#nothing5').show()
                $('#chart5').hide()
                $('#chart1Button5').hide()
            } else {
                $('#nothing5').hide()
                $('#chart5').show()
                $('#chart1Button5').show()
            }
            if (r[5].x.length == 0) {
                $('#nothing6').show()
                $('#chart6').hide()
                $('#chart1Button6').hide()
            } else {
                $('#nothing6').hide()
                $('#chart6').show()
                $('#chart1Button6').show()
            }
            // console.log(server_info)
            // for (var i = 0; i < server_info[2].y.length; i++) {
            //     server_info[2].y[i] = server_info[2].y[i]
            // }
            for (var i = 0; i < server_info[3].y.length; i++) {
                server_info[3].y[i] = server_info[3].y[i] / 1024
            }
            for (var i = 0; i < server_info[4].y.length; i++) {
                server_info[4].y[i] = server_info[4].y[i] / 1024
            }
            for (var i = 0; i < server_info[5].y.length; i++) {
                server_info[5].y[i] = server_info[5].y[i] / 1024
            }
            // console.log(server_info.data[2].y)
        }
    });

    // let numLength = 30;//固定的数据长度
    // let interval = (selectValue * 60) / numLength;//时间间隔
    // return Array.from({ length: numLength }, (v, i) => {
    //     let time = new Date().getTime() // 当前时间戳
    //     let afterTime = time - i * 1000 * interval // 计算后的时间戳
    //     console.log(time)
    //     let parseTime = new Date(afterTime).toLocaleString(); //转化后的时间
    //     console.log([parseTime, Math.floor(Math.random() * 100)])
    //     return {
    //         value: [parseTime, Math.floor(Math.random() * 100)]
    //     }
    // }).reverse()
    datas = Array.from(server_info[0].x, (v, i) => {
        let parseTime = new Date(v * 1000).toLocaleString(); //转化后的时间
        return {
            value: [parseTime, server_info[0].y[i]]
        }
    }).reverse()
    datas2 = Array.from(server_info[1].x, (v, i) => {
        let parseTime = new Date(v * 1000).toLocaleString(); //转化后的时间
        return {
            value: [parseTime, server_info[1].y[i]]
        }
    }).reverse()
    // return Array.from(time.x, (v, i) => {
    //     let parseTime = new Date(v * 1000).toLocaleString(); //转化后的时间
    //     return {
    //         value: [parseTime, time.y[i]]
    //     }
    // }).reverse()
}

//每60s刷新一次数据
let timer = setInterval(() => {
    randomData()
    lineOption.series[0].data = datas;
    lineOption2.series[0].data = datas2;
    BarOption2.series[0].data = server_info[3].y;
    BarOption2.yAxis.data = server_info[3].x;
    BarOption.series[0].data = server_info[2].y;
    BarOption.yAxis.data = server_info[2].x;
    BarOption3.series[0].data = server_info[4].y;
    BarOption3.yAxis.data = server_info[4].x;
    BarOption4.series[0].data = server_info[5].y;
    BarOption4.yAxis.data = server_info[5].x;
    myChart1.setOption(lineOption)
    myChart3.setOption(lineOption2)
    myChart2.setOption(BarOption2);
    myChart4.setOption(BarOption);
    myChart5.setOption(BarOption3);
    myChart6.setOption(BarOption4);
}, 1000)



randomData()

// CPU使用率的配置项和数据
var lineOption = {
    title: {
        text: 'CPU使用率',
        textStyle: {
            fontSize: 12,
            color: '#121316'
        }
    },
    tooltip: {},
    animation: false,
    grid: {
        top: 50,
        left: 50,
        right: 20,
        bottom: 30,
    },
    xAxis: {
        type: 'time',
        splitNumber: 3.5,
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            interval: 'auto',
            formatter: '{value} %',
            fontSize: 10
        },
        show: true,
        min: 0,
        max: 100
    },
    series: [
        {
            data: datas,
            type: 'line',
            lineStyle: {
                normal: {
                    color: '#b0cfee',
                    width: 4,
                    type: 'solid'
                }
            }
        }
    ]
};

// 内存使用率的配置项和数据
var lineOption2 = {
    title: {
        text: '内存使用率',
        textStyle: {
            fontSize: 12,
            color: '#121316'
        }
    },
    tooltip: {},
    animation: false,
    grid: {
        top: 50,
        left: 50,
        right: 20,
        bottom: 30,
    },
    xAxis: {
        type: 'time',
        splitNumber: 3.5,
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            interval: 'auto',
            formatter: '{value} %',
            fontSize: 10
        },
        show: true,
        min: 0,
        max: 100
    },
    series: [
        {
            data: datas2,
            type: 'line',
            lineStyle: {
                normal: {
                    color: '#b0cfee',
                    width: 4,
                    type: 'solid'
                }
            }
        }
    ]
};



// 硬盘使用率的配置项和数据

var BarOption = {
    title: {
        text: '硬盘使用率',
        textStyle: {
            fontSize: 12,
            color: '#121316'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    animation: false,
    legend: {
        itemWidth: 10,
        itemHeight: 10,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01],
        min: 0,
        max: 40,
        axisLabel: {
            formatter: `{value}%` // 在每个x轴坐标都添加了单位
        }
    },
    yAxis: {
        type: 'category',
        data: server_info[2].x,
        axisTick: {
            interval: 0
        },
        axisLabel: {
            interval: 0
        }
    },
    series: [
        {
            // name: '2022',
            type: 'bar',
            color: '#b0cfee',
            data: server_info[2].y
        },
    ]
};

//Mysql的配置项和数据

var BarOption2 = {
    title: {
        text: 'Mysql',
        textStyle: {
            fontSize: 12,
            color: '#121316'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    animation: false,
    legend: {
        itemWidth: 10,
        itemHeight: 10,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01],
        min: 0,
        max: 40,
        axisLabel: {
            formatter: `{value}G` // 在每个x轴坐标都添加了单位
        }
    },
    yAxis: {
        type: 'category',
        data: server_info[3].x,
        axisTick: {
            interval: 0
        },
        axisLabel: {
            interval: 0
        }
    },
    series: [
        {
            // name: '2022',
            type: 'bar',
            color: '#b0cfee',
            data: server_info[3].y
        },
    ]
};

//SQL Server的配置项和数据

var BarOption3 = {
    title: {
        text: 'SQL Server',
        textStyle: {
            fontSize: 12,
            color: '#121316'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    animation: false,
    legend: {
        itemWidth: 10,
        itemHeight: 10,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01],
        min: 0,
        max: 40,
        axisLabel: {
            formatter: `{value}G` // 在每个x轴坐标都添加了单位
        }
    },
    yAxis: {
        type: 'category',
        data: server_info[4].x,
        axisTick: {
            interval: 0
        },
        axisLabel: {
            interval: 0
        }
    },
    series: [
        {
            // name: '2022',
            type: 'bar',
            color: '#b0cfee',
            data: server_info[4].y
        },
    ]
};

//Oracle的配置项和数据

var BarOption4 = {
    title: {
        text: 'Oracle',
        textStyle: {
            fontSize: 12,
            color: '#121316'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        itemWidth: 10,
        itemHeight: 10,
    },
    animation: false,
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01],
        min: 0,
        max: 40,
        axisLabel: {
            formatter: `{value}G` // 在每个x轴坐标都添加了单位
        }
    },
    yAxis: {
        type: 'category',
        data: server_info[5].x
    },
    series: [
        {
            // name: '2022',
            type: 'bar',
            color: '#b0cfee',
            data: server_info[5].y
        },
    ]
};

// var autoHeight = BarOption.yAxis.data.length * 30 + 150
// var autoHeight = BarOption2.yAxis.data.length * 30 + 150
// var autoHeight = BarOption3.yAxis.data.length * 30 + 150
// var autoHeight = BarOption4.yAxis.data.length * 30 + 150
//获取option2配置项中y轴的数据源的长度*每个柱状你想设定的高度+150的预留高度
// myChart4.getDom().style.height = autoHeight + "px"
// console.log(autoHeight)
// console.log(myChart4.getDom())

//根据窗口的大小变动图表
// myChart4.resize()

//声明一个 全屏显示的echarts图表
// var chartScreen = null;

//全屏显示 toolbox回调
//@param option   echarts的配置项
// function setFullScreenToolBox(option) {
//     if ($("#fullScreenMask").css("display") === "block") {
//         $("#fullScreenMask").hide();
//         ChartScreen = null;
//         return false;
//     }
//     $("#fullScreenMask").show();
//     chartScreen = echarts.init(document.getElementById("fullScreen"));
//     chartScreen.setOption(option);
//     chartScreen.setOption({
//         toolbox: {
//             feature: {
//                 myTool: {
//                     show: true,
//                     title: "退出全屏",
//                     icon: "image://" + "./css/images/fullscreen-shrink.png",
//                     onclick: function () {
//                         $("#fullScreenMask").hide();
//                     }
//                 }
//             }
//         }
//     });
//     return true;
// }

// 点击放大
// function zoomFunction() {
//     console.log("点击放大");
//     //生成全屏显示的图表
//     setFullScreenToolBox(lineOption)
// }

// window.onresize = function () {
//     chartScreen.resize();
// };



