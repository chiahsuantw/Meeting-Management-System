const meetingTiles = $('.meetingTile');
const meetingViewArea = $('#meetingViewArea');
const meetingViewModal = $('#meetingViewModal');

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
            if ($(window).width() < 992) {
                meetingViewModal.children().children().children('.modal-body').html(data);
                // noinspection JSUnresolvedFunction
                meetingViewModal.modal('show');
            }
        }
    });
});