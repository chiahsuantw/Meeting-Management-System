const newAnnouncementBtn = $('#newAnnouncementBtn');
const newMotionBtn = $('#newMotionBtn');
const newExtemporeBtn = $('#newExtemporeBtn');

const announcementSection = $('#pAnnouncement');
const motionSection = $('#pMotion');
const extemporeSection = $('#pExtempore');

const newMeetingForm = $('#newMeetingForm');
const titleInput = $('#mTitleInput');
const timeInput = $('#mTimeInput');
const locationInput = $('#mLocationInput');
const typeInput = $('#mTypeInput');
const chairInput = $('#mChairInput');
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
    // noinspection HtmlUnknownTarget
    const motionElement = `
        <div class="d-flex mb-2">
            <div class="border rounded px-2 flex-fill">
                <div class=my-2>
                    <h6>案由</h6>
                    <input class="form-control motion-form" aria-label=MotionDescription>
                </div>
                <div class=mb-2><h6>狀態</h6>
                    <select class="selectpicker motion-form" data-style=bg-white 
                            data-width=100% aria-label=MotionStatus>
                        <option value=InDiscussion selected>討論中</option>
                        <option value=InExecution>執行中</option>
                        <option value=Closed>結案</option>
                    </select></div>
                <div class=mb-2>
                    <h6>內容</h6>
                    <textarea type=text class="form-control motion-form" 
                              rows=3 aria-label=MotionContent></textarea>
                </div>
                <div class=mb-2>
                    <h6>決策</h6>
                    <textarea type=text class="form-control motion-form" 
                              rows=3 aria-label=MotionResolution></textarea>
                </div>
                <div class=mb-2>
                    <h6>執行</h6>
                    <textarea type=text class="form-control motion-form" 
                              rows=3 aria-label=MotionExecution></textarea>
                </div>
            </div>
            <a href=javascript:void(0) class="my-auto ms-2">
                <img src=/static/images/trash-fill.svg width=20 alt="">
            </a>
        </div>
    `;
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

// Set up the form validator
newMeetingForm.validate({
    'errorElement': 'span',
    'rules': {
        'mTitleInput': 'required',
        'mTimeInput': 'required',
        'mLocationInput': 'required',
        'mTypeInput': 'required',
        'mChairInput': 'required',
        'mMinuteTakerInput': 'required',
        'mAttendeeInput': 'required',
        'mGuestInput': 'required',
        'mAttachmentInput[]': {
            'accept':
                'image/jpeg,' +
                'image/png,' +
                'application/msword,' +
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document,' +
                'application/vnd.ms-powerpoint,' +
                'application/vnd.openxmlformats-officedocument.presentationml.presentation,' +
                'application/vnd.ms-excel,' +
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,' +
                'application/pdf',
            'maxsize': 104857600,
        }
    },
    'messages': {
        'mAttachmentInput[]': {
            'accept': '只接受圖片與文件',
            'maxsize': '檔案大小應小於 100 MB'
        }
    },
    'onfocusout': function (element) {
        if (element.id === "mAttachmentInput[]") {
            this.element(element);
        }
    },
    'invalidHandler': function (form, validator) {
        let numberOfInvalids = validator.numberOfInvalids();
        if (numberOfInvalids) {
            $('#newMeetingFormError').removeClass('d-none').children().children('div')
                .html('有 ' + numberOfInvalids + ' 個欄位不正確');
        }
    }
});

newMeetingForm.on('change', function () {
    // If fields in the form changes -> refresh form validation state
    if (newMeetingForm.hasClass('has-validated') && newMeetingForm.valid()) {
        $('#newMeetingFormError').addClass('d-none');
    }
});

$('#newMeetingBtn').on('click', function () {
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

    $('#pAnnouncement').children().each(function () {
        announcementList.push($(this).children().val());
    })

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

    $('#pExtempore').children().each(function () {
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
});