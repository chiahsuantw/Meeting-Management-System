let meeting_id;
$(document).ready(function () {
    meeting_id = window.location.pathname.split('/').pop();

    $.ajax({
        'url': $SCRIPT_ROOT + '/api/meeting/' + meeting_id,
        'data': null,
        'type': 'GET',
        'dataType': 'json',
        'success': function (data) {
            titleInput.val(data['title']);
            let datetime = new Date(data['time']).toISOString();
            timeInput.val(datetime.substring(0, datetime.length - 1));
            locationInput.val(data['location']);
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

                if (data['chair'] === parseInt(value)) {
                    oldChairIndex = index;
                    minuteTakerBar[index].disabled = true;
                    attendeeBar[index - 1].disabled = true;
                    guestBar[index - 1].disabled = true;
                } else if (data['minuteTaker'] === parseInt(value)) {
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

            data['files'].forEach(function (fileObj) {
                let fileTypeIcon = {
                    'jpg': 'photos',
                    'jpeg': 'photos',
                    'png': 'photos',
                    'pdf': 'adobe-acrobat',
                    'txt': 'notepad',
                    'ppt': 'microsoft-powerpoint-2019',
                    'pptx': 'microsoft-powerpoint-2019',
                    'xls': 'microsoft-excel-2019',
                    'xlsx': 'microsoft-excel-2019',
                    'doc': 'microsoft-word-2019',
                    'docx': 'microsoft-word-2019',
                    'others': 'file'
                };

                let fileBtn = `
                    <div class="card bg-light">
                        <div class="card-body d-flex align-items-center" title="${fileObj['file_name'] + '.' + fileObj['file_type']}">
                            <img src="https://img.icons8.com/fluency/240/000000/${fileTypeIcon[fileObj['file_type']]}.png"
                                     width="24" height="24" alt="">
                            <p class="mx-1 mb-0 card-text">${fileObj['file_name']}</p>
                            <div class="deleteFileBtn" id="deleteFileBtn-${fileObj['file_id']}" style="cursor: pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                `;
                $('#savedFiles').append(fileBtn);
            });
        }
    });
});


$('#editMeetingBtn').on('click', function () {
    // The form validation state updates when changes were made in the form
    // And it triggers the validation process before clicking the submit button
    // We add .has-validated class to mark if the button was clicked
    // and remove it if the user decided to cancel the process
    newMeetingForm.addClass('has-validated');

    if (!newMeetingForm.valid()) {
        // Show the error message at the bottom
        $('#meetingFormArea').animate({scrollTop: 10000}, 1);
        // If NewMeetingForm is invalid -> Don't send form post
        return;
    }

    // formData contains: { json_form: body_form_save_as_json, attachments: FileList }
    let formData = new FormData();
    let meetingForm = {};

    meetingForm['title'] = titleInput.val();
    meetingForm['time'] = timeInput.val();
    meetingForm['location'] = locationInput.val();
    meetingForm['type'] = typeInput.val();
    meetingForm['chair'] = chairInput.val();
    meetingForm['minuteTaker'] = minuteTakerInput.val();
    meetingForm['attendee'] = attendeeInput.val();
    meetingForm['guest'] = guestInput.val();
    meetingForm['chairSpeech'] = chairSpeechInput.val();

    let announcementList = [];
    let motionList = [];
    let extemporeList = [];

    $('#pAnnouncement').children('div').each(function () {
        announcementList.push($(this).children().val());
    })

    let present = [];
    $('.attendanceCheck').each(function () {
        if ($(this).siblings('input').prop('checked')) {
            present.push(parseInt(this.id.split('-')[1]));
        }
    });
    meetingForm['present'] = present;

    let motionRaw = $('#pMotion')[0].getElementsByClassName('motion-form');
    for (let i = 0; i < motionRaw.length / 6; i++) {
        let head = i * 6;
        motionList.push({
            'MotionDescription': motionRaw[head].value,
            'MotionStatus': motionRaw[head + 2].value,
            'MotionContent': motionRaw[head + 3].value,
            'MotionResolution': motionRaw[head + 4].value,
            'MotionExecution': motionRaw[head + 5].value
        })
    }

    $('#pExtempore').children('div').each(function () {
        extemporeList.push($(this).children().val());
    })

    meetingForm['announcement'] = announcementList;
    meetingForm['motion'] = motionList;
    meetingForm['extempore'] = extemporeList;

    formData.append('json_form', JSON.stringify(meetingForm));

    let attachments = document.getElementById('mAttachmentInput').files;
    for (let i = 0; i < attachments.length; i++) {
        formData.append('files[]', attachments[i]);
    }

    $.ajax({
        'type': 'POST',
        'dataType': 'json',
        'mimeType': 'multipart/form-data',
        'url': $SCRIPT_ROOT + '/edit/meeting/' + meeting_id,
        'data': formData,
        'success': (data) => {
            if (data['message'] === 'Success') {
                // Redirect to homepage if the submission is successful
                window.location.href = '/meeting/' + meeting_id;
                console.log('success')
            } else {
                // TODO: If validation failed -> show error message
                console.log(data['message']);
            }
        },
        'contentType': false,
        'processData': false,
    });
});

$('#savedFiles').on('click', 'div > div > div', function () {
    let file_id = $(this).attr('id').split('-')[1];
    $.ajax({
        'type': 'POST',
        'url': $SCRIPT_ROOT + '/delete-file/' + file_id,
        'success': (data) => {
            if (data['message'] === 'Success') {
                console.log('File delete successfully!')
                $(this).parent().parent().remove();
            } else {
                // TODO: If deleting failed -> show error message
                console.log(data['message']);
            }
        },
    });
});