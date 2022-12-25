var obtainTimeStamp = function (dateTimeStr) {
    if (dateTimeStr == null || dateTimeStr == '') {
        return 0;
    }
    return Math.floor((new Date(dateTimeStr)).getTime() / 1000);
}


$(document).ready(function () {

    /*
     * 设置 jquery ui datepicker 外观
     */
    timeFormatObj = {

        showSecond: true,
        changeMonth: true,
        timeFormat: 'HH:mm:ss',
        dateFormat: 'yy-mm-dd',

        stepHour: 1,
        stepMinute: 5,
        stepSecond: 5
    };


    $('#beginDateTimepicker').datetimepicker(timeFormatObj);
    $('#endDateTimepicker').datetimepicker(timeFormatObj);

    $('input[type="submit"]').button().click(function (event) {

        var beginTimeStamp = 0, endTimeStamp = 0;
        var now = new Date();
        var endTimeStamp = Math.floor(now.getTime() / 1000);
        var lastTimeValue = $('#lastTimeSelect').val();
        var beginTimeStamp = endTimeStamp - parseInt(lastTimeValue) * 60 * 60;

        var beginTimeStampForUserDefined = obtainTimeStamp($('#beginDateTimepicker').val());
        var endTimeStampForUserDefined = obtainTimeStamp($('#endDateTimepicker').val());

        if (beginTimeStampForUserDefined != 0 && endTimeStampForUserDefined != 0) {
            beginTimeStamp = beginTimeStampForUserDefined;
            endTimeStamp = endTimeStampForUserDefined;
        }

        timeRange = [beginTimeStamp, endTimeStamp];

        // alert(beginTimeStamp + ' ' + endTimeStamp);

    });

    $('#drawChartButton').trigger('click');

});