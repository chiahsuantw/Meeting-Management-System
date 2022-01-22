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
        'success': function (data) {
            console.log('mail sending')
        }
    });
    $('#toast-notice').toast('show');
});

meetingViewArea.on('click', '#send-minute', function () {
    let meeting_id = $('#meeting-minutes')[0].attributes.name.value;
    $.ajax({
        'url': $SCRIPT_ROOT + '/mail/minute/' + meeting_id,
        'data': null,
        'type': 'GET',
        'success': function (data) {
            console.log('mail sending')
        }
    });
    $('#toast-minute').toast('show');
});

meetingViewArea.on('click', '#send-modify', function () {
    let meeting_id = $('#meeting-minutes')[0].attributes.name.value;
    $.ajax({
        'url': $SCRIPT_ROOT + '/mail/modify/' + meeting_id,
        'data': {modify: $('#modifyRequestText').val()},
        'type': 'GET',
        'success': function (data) {
            console.log('mail sending')
        }
    });
    $('#toast-minute').toast('show');
});

meetingViewArea.on('click', '#confirmBtn', function () {
    let checkElem = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
             class="bi bi-check mb-1" viewBox="0 0 16 16">
            <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"></path>
        </svg>
    `;
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
                console.log('confirm check');
            }
        });
    } else {
        $(this).removeClass('btn-primary');
        $(this).addClass('btn-outline-primary');
        $('#person-' + $('#current_user_id').text()).children('svg').remove();
        $.ajax({
            'url': $SCRIPT_ROOT + '/confirm',
            'data': {
                person_id: parseInt($('#current_user_id').text()),
                meeting_id: $('#meeting-minutes')[0].attributes.name.value,
                confirm: false
            },
            'type': 'GET',
            'success': function (data) {
                console.log('unconfirm check');
            }
        });
    }
});