const newAnnouncementBtn = $('#newAnnouncementBtn');
const newMotionBtn = $('#newMotionBtn');
const newExtemporeBtn = $('#newExtemporeBtn');

const announcementSection = $('#pAnnouncement');
const motionSection = $('#pMotion');
const extemporeSection = $('#pExtempore');

const titleInput = $('#mTitleInput');
const timeInput = $('#mTimeInput');
const locationInput = $('#mLocationInput');
const typeInput = $('#mTypeInput');
const minuteTakerInput = $('#mMinuteTakerInput');
const attendeeInput = $('#mAttendeeInput');
const guestInput = $('#mGuestInput');
const chairSpeechInput = $('#mChairSpeechInput');


newAnnouncementBtn.on('click', function () {
    // Add an announcement to the meeting
    const announcementElement = '<div class="d-flex mb-2">' +
        '<textarea class="form-control" rows="2" ' +
        'aria-label="AnnouncementContent" placeholder="內容"></textarea>' +
        '<a href="javascript:void(0)" class="my-auto ms-2">' +
        '<img src="/static/images/trash-fill.svg" width="20" alt=""></a></div>';
    announcementSection.append(announcementElement);
});

newMotionBtn.on('click', function () {
    // Add a motion to the meeting
    const motionElement =
        '<div class="d-flex mb-2"><div class="border rounded px-2 flex-fill">' +
        '<div class=my-2>' +
        '<h6>案由</h6><input class="form-control motion-form" aria-label=MotionDescription>' +
        '</div><div class=mb-2><h6>狀態</h6>' +
        '<select class="selectpicker motion-form" data-style=bg-white data-width=100% aria-label=MotionStatus>' +
        '<option value=InDiscussion selected>討論中</option>' +
        '<option value=InExecution>執行中</option>' +
        '<option value=Closed>結案</option>' +
        '</select></div>' +
        '<div class=mb-2>' +
        '<h6>內容</h6>' +
        '<textarea type=text class="form-control motion-form" rows=3 aria-label=MotionContent></textarea></div>' +
        '<div class=mb-2>' +
        '<h6>決策</h6><textarea type=text class="form-control motion-form" rows=3 aria-label=MotionResolution></textarea>' +
        '</div><div class=mb-2>' +
        '<h6>執行</h6><textarea type=text class="form-control motion-form" rows=3 aria-label=MotionExecution></textarea>' +
        '</div></div><a href=javascript:void(0) class="my-auto ms-2">' +
        '<img src=/static/images/trash-fill.svg width=20 alt=""></a></div>';
    motionSection.append(motionElement);
    $('select').selectpicker();
});

newExtemporeBtn.on('click', function () {
    // Add an extempore to the meeting
    const extemporeElement = '<div class="d-flex mb-2">' +
        '<textarea class="form-control" rows="2" ' +
        'aria-label="ExtemporeContent" placeholder="內容"></textarea>' +
        '<a href="javascript:void(0)" class="my-auto ms-2">' +
        '<img src="/static/images/trash-fill.svg" width="20" alt=""></a></div>';
    extemporeSection.append(extemporeElement);
});

announcementSection.on('click', 'div > a', function () {
    // Delete the announcement
    $(this).parent().remove();
})

motionSection.on('click', 'div > a', function () {
    // Delete the motion
    $(this).parent().remove();
})

extemporeSection.on('click', 'div > a', function () {
    // Delete the extempore
    $(this).parent().remove();
})

$('#newMeetingBtn').on('click', function () {
    // formData contains: { json_form: body_form_save_as_json, attachments: FileList }
    let formData = new FormData();
    let meetingForm = {};

    meetingForm['title'] = titleInput.val();
    meetingForm['time'] = timeInput.val();
    meetingForm['location'] = locationInput.val();
    meetingForm['type'] = typeInput.val();
    meetingForm['minuteTaker'] = minuteTakerInput.val();
    meetingForm['attendee'] = attendeeInput.val();
    meetingForm['guest'] = guestInput.val();
    meetingForm['chairSpeech'] = chairSpeechInput.val();

        let announcementList = [];
        let motionList = [];
        let extemporeList = [];

    $('#pAnnouncement').children().each(function () {
        announcementList.push($(this).children().val());
    })

        let motionRaw = $('#pMotion')[0].getElementsByClassName('motion-form');
    for (let i = 0; i < motionRaw.length / 6; i++) {
        motionList.push({
            'MotionDescription': motionRaw[0].value,
            'MotionStatus': motionRaw[2].value,
            'MotionContent': motionRaw[3].value,
            'MotionResolution': motionRaw[4].value,
            'MotionExecution': motionRaw[5].value
        })
    }

    $('#pExtempore').children().each(function () {
        extemporeList.push($(this).children().val());
    })

    meetingForm['announcement'] = announcementList;
    meetingForm['motion'] = motionList;
    meetingForm['extempore'] = extemporeList;

    formData.append('json_form', JSON.stringify(meetingForm));

    // File uploads
    let attachments = document.getElementById('mAttachmentInput').files;
    for (let i = 0; i < attachments.length; i++) {
        formData.append('files[]', attachments[i]);
    }

    $.ajax({
        'type': 'POST',
        'dataType': 'json',
        'mimeType': 'multipart/form-data',
        'url': $SCRIPT_ROOT + '/new/meeting',
        'data': formData,
        'success': (data) => {
            if (data['message'] === 'Success') {
                console.log(data['message'])
            } else {
                // TODO: If validation failed -> show error message
                console.log(data['message']);
            }
        },
        'contentType': false,
        'processData': false,
        });
    }
);
