// noinspection JSUnresolvedFunction

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

meetingViewArea.on('click', '#send-notice', function () {
    let meeting_id = $('#meeting-minutes')[0].attributes.name.value;
    $.ajax({
        'url': $SCRIPT_ROOT + '/mail/notice/' + meeting_id,
        'data': null,
        'type': 'GET',
        'success': function () {
            $('#toast-notice').toast('show');
        }
    });
});

meetingViewArea.on('click', '#send-minute', function () {
    let meeting_id = $('#meeting-minutes')[0].attributes.name.value;
    $.ajax({
        'url': $SCRIPT_ROOT + '/mail/minute/' + meeting_id,
        'data': null,
        'type': 'GET',
        'success': function () {
            $('#toast-minute').toast('show');
        }
    });
});

meetingViewArea.on('click', '#send-modify', function () {
    if (!$('#modifyRequestText').val()) {
        $('#modifyRequestText').addClass('is-invalid');
        return;
    }

    let meeting_id = $('#meeting-minutes')[0].attributes.name.value;
    $.ajax({
        'url': $SCRIPT_ROOT + '/mail/modify/' + meeting_id,
        'data': {modify: $('#modifyRequestText').val()},
        'type': 'GET',
        'success': function () {
            $('#modifyRequestModal').modal('hide');
            $('#modifyRequestText').removeClass('is-invalid');
            $('#modifyRequestText').val('');
            $('#toast-modify').toast('show');
        }
    });
});

meetingViewArea.on('click', '#print-minute', function () {
    let meeting_id = $('#meeting-minutes')[0].attributes.name.value;
    let printWindow = window.open($SCRIPT_ROOT + '/print/minute/' + meeting_id);
    printWindow.print();
});

meetingViewArea.on('click', '#confirmBtn', function () {
    let checkElem = '<i class="bi bi-check mb-1"></i>';
    if ($(this).hasClass('btn-outline-primary')) {
        $(this).removeClass('btn-outline-primary');
        $(this).addClass('btn-primary');
        $('#person-' + $('#current_user_id').text()).append(checkElem);
        $.ajax({
            'url': $SCRIPT_ROOT + '/confirm',
            'data': {
                person_id: $('#current_user_id').text(),
                meeting_id: $('#meeting-minutes')[0].attributes.name.value,
                confirm: true
            },
            'type': 'GET',
            'success': function (data) {
                if (data === 'Archived') {
                    $('#controlZone').html('<span class="badge bg-secondary fs-5 m-2">已封存</span>');
                }
            }
        });
    } else {
        $(this).removeClass('btn-primary');
        $(this).addClass('btn-outline-primary');
        $('#person-' + $('#current_user_id').text()).children('i').remove();
        $.ajax({
            'url': $SCRIPT_ROOT + '/confirm',
            'data': {
                person_id: parseInt($('#current_user_id').text()),
                meeting_id: $('#meeting-minutes')[0].attributes.name.value,
                confirm: false
            },
            'type': 'GET',
            'success': function () {
                console.log('unconfirm check');
            }
        });
    }
});