const meetingTiles = $('.meetingTile');
const meetingViewArea = $('#meetingViewArea');

meetingTiles.on('click', function () {
    meetingTiles.removeClass('active');
    $(this).addClass('active');

    $.ajax({
        'url': $SCRIPT_ROOT + '/get/meeting',
        'data': {
            id: $(this).attr('id').split('-')[1]
        },
        'type': 'GET',
        'dataType': 'html',
        'success': function (data) {
            meetingViewArea.html(data);
            meetingViewArea.animate({scrollTop: 0}, 1);
        }
    });
});