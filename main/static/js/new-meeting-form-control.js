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

// This is used for giving each extemporeElement a specific name
// because jQuery validate needs unique name to work
let announcementElementCounter = 0;
newAnnouncementBtn.on('click', function () {
    // Add an announcement to the meeting
    // noinspection HtmlUnknownTarget
    const announcementElement = `
        <div class="d-flex mt-2">
            <textarea class="form-control" rows="2" aria-label="AnnouncementContent"
                      name="AnnouncementContent-${announcementElementCounter}"
                      placeholder="內容" aria-describedby="AnnouncementContentError-${announcementElementCounter}"></textarea>
            <a href="javascript:void(0)" class="my-auto ms-2">
                <i class="bi bi-trash-fill fs-5 text-muted"></i>
            </a>
        </div>
        <span class="error invalid-feedback" id="AnnouncementContentError-${announcementElementCounter}"></span>
    `;
    announcementSection.append(announcementElement);
    $(`textarea[name='AnnouncementContent-${announcementElementCounter}']`).rules('add', {'required': true});
    announcementElementCounter++;
});

// This is used for giving each extemporeElement a specific name
// because jQuery validate needs unique name to work
let motionElementCounter = 0;
newMotionBtn.on('click', function () {
    // Add a motion to the meeting
    // noinspection HtmlUnknownTarget
    const motionElement = `
        <div class="d-flex mb-2">
            <div class="border rounded px-2 flex-fill">
                <div class=my-2>
                    <h6>案由</h6>
                    <input class="form-control motion-form" aria-label=MotionDescription 
                           name="MotionDescription-${motionElementCounter}" 
                           aria-describedby="MotionDescriptionError-${motionElementCounter}">
                    <span class="error invalid-feedback" id="MotionDescriptionError-${motionElementCounter}"></span>
                </div>
                <div class=mb-2><h6>狀態</h6>
                    <select class="selectpicker motion-form" data-style=bg-white 
                            name="MotionStatus-${motionElementCounter}"
                            data-width=100% aria-label=MotionStatus>
                        <option value=InDiscussion selected>討論中</option>
                        <option value=InExecution>執行中</option>
                        <option value=Closed>結案</option>
                    </select></div>
                <div class=mb-2>
                    <h6>內容</h6>
                    <textarea type=text class="form-control motion-form" 
                              name="MotionContent-${motionElementCounter}"
                              rows=3 aria-label=MotionContent 
                              aria-describedby="MotionContentError-${motionElementCounter}"></textarea>
                    <span class="error invalid-feedback" id="MotionContentError-${motionElementCounter}"></span>
                </div>
                <div class=mb-2>
                    <h6>決策</h6>
                    <textarea type=text class="form-control motion-form" 
                              name="MotionResolution-${motionElementCounter}"
                              rows=3 aria-label=MotionResolution></textarea>
                </div>
                <div class=mb-2>
                    <h6>執行</h6>
                    <textarea type=text class="form-control motion-form" 
                              name="MotionExecution-${motionElementCounter}"
                              rows=3 aria-label=MotionExecution></textarea>
                </div>
            </div>
            <a href=javascript:void(0) class="my-auto ms-2">
                <i class="bi bi-trash-fill fs-5 text-muted"></i>
            </a>
        </div>
    `;
    motionSection.append(motionElement);
    $('select').selectpicker();
    $(`input[name='MotionDescription-${motionElementCounter}']`).rules('add', {'required': true});
    $(`textarea[name='MotionContent-${motionElementCounter}']`).rules('add', {'required': true});
    motionElementCounter++;
});

// This is used for giving each extemporeElement a specific name
// because jQuery validate needs unique name to work
let extemporeElementCounter = 0;
newExtemporeBtn.on('click', function () {
    // Add an extempore to the meeting
    // noinspection HtmlUnknownTarget
    const extemporeElement = `
        <div class="d-flex mt-2">
            <textarea class="form-control" rows="2" aria-label="ExtemporeContent" 
                      name="ExtemporeContent-${extemporeElementCounter}"
                      placeholder="內容" aria-describedby="ExtemporeContentError-${extemporeElementCounter}"></textarea>
            <a href="javascript:void(0)" class="my-auto ms-2">
                <i class="bi bi-trash-fill fs-5 text-muted"></i>
            </a>
        </div>
        <span class="error invalid-feedback" id="ExtemporeContentError-${extemporeElementCounter}"></span>
    `;
    extemporeSection.append(extemporeElement);
    $(`textarea[name='ExtemporeContent-${extemporeElementCounter}']`).rules('add', {'required': true});
    extemporeElementCounter++;
});

announcementSection.on('click', 'div > a', function () {
    // Delete the announcement
    let elemIndex = $(this).siblings()[0].name.split('-')[1];
    $(this).parent().siblings('#AnnouncementContentError-' + elemIndex).remove();
    $(this).parent().remove();
})

motionSection.on('click', 'div > a', function () {
    // Delete the motion
    $(this).parent().remove();
})

extemporeSection.on('click', 'div > a', function () {
    // Delete the extempore
    let elemIndex = $(this).siblings()[0].name.split('-')[1];
    $(this).parent().siblings('#ExtemporeContentError-' + elemIndex).remove();
    $(this).parent().remove();
})

// Detect duplicates in selecting person section
// If someone is selected -> Disable the option for the other picker
let oldChairIndex = 0
let oldMinuteTakerIndex = 0
chairInput.on('changed.bs.select', function (e, clickedIndex) {
    minuteTakerInput.children()[clickedIndex].disabled = true;
    minuteTakerInput.children()[oldChairIndex].disabled = false;

    if (clickedIndex) {
        attendeeInput.children()[clickedIndex - 1].disabled = true;
        guestInput.children()[clickedIndex - 1].disabled = true;
    }
    if (oldChairIndex > 0) {
        attendeeInput.children()[oldChairIndex - 1].disabled = false;
        guestInput.children()[oldChairIndex - 1].disabled = false;
    }
    minuteTakerInput.selectpicker('refresh');
    attendeeInput.selectpicker('refresh');
    guestInput.selectpicker('refresh');

    oldChairIndex = clickedIndex;
});

minuteTakerInput.on('changed.bs.select', function (e, clickedIndex) {
    chairInput.children()[clickedIndex].disabled = true;
    chairInput.children()[oldMinuteTakerIndex].disabled = false;

    if (clickedIndex > 0) {
        attendeeInput.children()[clickedIndex - 1].disabled = true;
        guestInput.children()[clickedIndex - 1].disabled = true;
    }
    if (oldMinuteTakerIndex > 0) {
        attendeeInput.children()[oldMinuteTakerIndex - 1].disabled = false;
        guestInput.children()[oldMinuteTakerIndex - 1].disabled = false;
    }
    chairInput.selectpicker('refresh');
    attendeeInput.selectpicker('refresh');
    guestInput.selectpicker('refresh');

    oldMinuteTakerIndex = clickedIndex;
});

attendeeInput.on('changed.bs.select', function (e, clickedIndex, newValue) {
    if (newValue) {
        chairInput.children()[clickedIndex + 1].disabled = true;
        minuteTakerInput.children()[clickedIndex + 1].disabled = true;
        guestInput.children()[clickedIndex].disabled = true;
    } else {
        chairInput.children()[clickedIndex + 1].disabled = false;
        minuteTakerInput.children()[clickedIndex + 1].disabled = false;
        guestInput.children()[clickedIndex].disabled = false;
    }
    chairInput.selectpicker('refresh');
    minuteTakerInput.selectpicker('refresh');
    guestInput.selectpicker('refresh');
});

guestInput.on('changed.bs.select', function (e, clickedIndex, newValue) {
    if (newValue) {
        chairInput.children()[clickedIndex + 1].disabled = true;
        minuteTakerInput.children()[clickedIndex + 1].disabled = true;
        attendeeInput.children()[clickedIndex].disabled = true;
    } else {
        chairInput.children()[clickedIndex + 1].disabled = false;
        minuteTakerInput.children()[clickedIndex + 1].disabled = false;
        attendeeInput.children()[clickedIndex].disabled = false;
    }
    chairInput.selectpicker('refresh');
    minuteTakerInput.selectpicker('refresh');
    attendeeInput.selectpicker('refresh');
});

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
                'text/plain,' +
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
        'url': $SCRIPT_ROOT + '/new/meeting',
        'data': formData,
        'success': (data) => {
            if (data['message'] === 'Success') {
                // Redirect to homepage if the submission is successful
                window.location.href = '/';
            } else {
                // TODO: If validation failed -> show error message
                console.log(data['message']);
            }
        },
        'contentType': false,
        'processData': false,
    });
});

const attendanceInput = $('#mAttendanceInput');
$('.person-select').on('change', function () {
    // Add selected people to AttendanceCheckList
    if (this.id === 'mAttendeeInput' || this.id === 'mGuestInput') {
        // Clear the section
        appendPresentTag();
    }
});

attendanceInput.on('click', 'div > a', function () {
    const checkBox = $(this).siblings('input');
    if (checkBox.prop('checked') === true) {
        checkBox.prop('checked', false);
        $(this).css('background-color', '#ffcdd2');
        $(this).removeClass('border border-success');
        $(this).addClass('border border-danger');
    } else {
        checkBox.prop('checked', true);
        $(this).css('background-color', '#c8e6c9');
        $(this).removeClass('border border-danger');
        $(this).addClass('border border-success');
    }
});

function appendPresentTag() {
    attendanceInput.html('');
    let personSet = new Set(attendeeInput.val().concat(guestInput.val()));
    // Add people to the section
    personSet.forEach(function (value) {
        const name = $(`#mChairInput option[value=${value}]`).html().trim();
        attendanceInput.append(`
                <div>
                    <a href="javascript:void(0)" style="background-color: #c8e6c9" id="attendace-${value}"
                       class="attendanceCheck px-2 border border-success 
                              rounded-pill text-decoration-none text-dark">${name}</a>
                    <input type="checkbox" class="d-none" autocomplete="off" aria-label="" checked>
                </div>
            `);
    });
}