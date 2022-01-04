const motionTiles = $('.motionTile');
const motionViewArea = $('#motionViewArea');
const motionViewModal = $('#motionViewModal');

motionTiles.on('click', function () {
    motionTiles.removeClass('active');
    $(this).addClass('active');

    $.ajax({
        'url': $SCRIPT_ROOT + '/get/motion',
        'data': {
            id: $(this).attr('id').split('-')[1]
        },
        'type': 'GET',
        'dataType': 'html',
        'success': function (data) {
            motionViewArea.html(data);
            motionViewArea.animate({scrollTop: 0}, 1);
            if ($(window).width() < 992) {
                motionViewModal.children().children().children('.modal-body').html(data);
                // noinspection JSUnresolvedFunction
                motionViewModal.modal('show');
            }
        }
    });
});