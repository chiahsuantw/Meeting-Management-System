$(document).ready(function () {
    let meeting_id = window.location.pathname.split('/').pop()

    $.ajax({
        'url': $SCRIPT_ROOT + '/api/meeting/' + meeting_id,
        'data': null,
        'type': 'GET',
        'dataType': 'json',
        'success': function (data) {
            // console.log(data);
            titleInput.val(data['title'])
            locationInput.val(data['location'])
            typeInput.val(data['type']);
            chairInput.val(data['chair']);
            minuteTakerInput.val(data['minuteTaker']);
            attendeeInput.val(data['attendee']);
            guestInput.val(data['guest']);

            // disable click process
            let chairBar = chairInput.children();
            let minuteTakerBar = minuteTakerInput.children();
            let attendeeBar = attendeeInput.children();
            let guestBar = guestInput.children();
            chairInput.children().each(function () {
                let value = $(this).val();
                let index = $(this).index();

                if (data['chair'].toString() === value) {
                    oldChairIndex = index;
                    minuteTakerBar[index].disabled = true;
                    attendeeBar[index - 1].disabled = true;
                    guestBar[index - 1].disabled = true;
                } else if (data['minuteTaker'].toString() === value) {
                    oldMinuteTakerIndex = index;
                    chairBar[index].disabled = true;
                    attendeeBar[index - 1].disabled = true;
                    guestBar[index - 1].disabled = true;
                } else if (data['attendee'][0] === parseInt(value)) {
                    data['attendee'].shift();
                    chairBar[index].disabled = true;
                    minuteTakerBar[index].disabled = true;
                    guestBar[index - 1].disabled = true;
                } else if (data['guest'][0] === parseInt(value)) {
                    data['guest'].shift();
                    chairBar[index].disabled = true;
                    minuteTakerBar[index].disabled = true;
                    attendeeBar[index - 1].disabled = true;
                }
            })
            $('.selectpicker').selectpicker('refresh');
            appendPresentTag();
            $('.attendanceCheck').each(function () {
                if (parseInt(this.id.split('-')[1]) === data['is_present'][0]) {
                    data['is_present'].shift();
                } else {
                    $(this).click()
                }
            });
            chairSpeechInput.text(data['chair_speech']);


            for (let i = 0; i < data['announcements'].length; i++) {
                newAnnouncementBtn.click();
                $('textarea[name="AnnouncementContent-' + i + '"]').text(data['announcements'][i]);
            }
            for (let i = 0; i < data['motions'].length; i++) {
                newMotionBtn.click();
                let motion = data['motions'][i];
                $('input[name="MotionDescription-' + i + '"]').val(motion['description']);
                $('select[name="MotionStatus-' + i + '"]').val(motion['status']).selectpicker('refresh');
                $('textarea[name="MotionContent-' + i + '"]').val(motion['content']);
                $('textarea[name="MotionResolution-' + i + '"]').val(motion['resolution']);
                $('textarea[name="MotionExecution-' + i + '"]').val(motion['execution']);
            }
            for (let i = 0; i < data['extempore'].length; i++) {
                newExtemporeBtn.click();
                $('textarea[name="ExtemporeContent-' + i + '"]').text(data['extempore'][i]);
            }
        }
    });
});
