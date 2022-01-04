const personTiles = $('.personTile');
const personViewArea = $('#personViewArea');
const personViewModal = $('#personViewModal');

personTiles.on('click', function () {
    personTiles.removeClass('active');
    $(this).addClass('active');

    $.ajax({
        'url': $SCRIPT_ROOT + '/get/person',
        'data': {
            id: $(this).attr('id').split('-')[1]
        },
        'type': 'GET',
        'dataType': 'html',
        'success': function (data) {
            personViewArea.html(data);
            personViewArea.animate({scrollTop: 0}, 1);
            if ($(window).width() < 992) {
                personViewModal.children().children().children('.modal-body').html(data);
                // noinspection JSUnresolvedFunction
                personViewModal.modal('show');
            }
        }
    });
});