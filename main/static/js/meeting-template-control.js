const templateSaveForm = $('#templateSaveForm');
const templateNameInput = $('#templateNameInput');
const templateList = $('#templateList');
let templateContentList = {};

$(document).ready(function () {
    updateTemplateList()
});

templateSaveForm.validate({
    'errorElement': 'span',
    'rules': {
        'templateNameInput': 'required'
    },
});

$('#templateSaveBtn').on('click', function () {
    if (!newMeetingForm.valid() || !templateSaveForm.valid()) {
        return;
    }
    let formData = new FormData();
    let meetingTemplate = {};
    meetingTemplate['name'] = templateNameInput.val();
    meetingTemplate['title'] = titleInput.val();
    meetingTemplate['time'] = timeInput.val();
    meetingTemplate['location'] = locationInput.val();
    meetingTemplate['type'] = typeInput.val();
    meetingTemplate['chair'] = chairInput.val();
    meetingTemplate['minuteTaker'] = minuteTakerInput.val();
    meetingTemplate['attendee'] = attendeeInput.val();
    meetingTemplate['guest'] = guestInput.val();
    formData.append('json_form', JSON.stringify(meetingTemplate));
    $.ajax({
        method: 'POST',
        url: $SCRIPT_ROOT + '/template/add',
        data: formData,
        'success': function () {
            console.log('add template successfully')
            updateTemplateList();
        },
        contentType: false,
        processData: false,
    });
});

templateList.on('click', 'li > a:nth-child(1)', function (e) {
    let data = templateContentList[$(this).data('id')];
    titleInput.val(data['title']);
    let datetime = new Date(data['time']).toISOString();
    timeInput.val(datetime.substring(0, datetime.length - 1));
    locationInput.val(data['location']);
    typeInput.val(data['type']);
    chairInput.val(data['chair']);
    minuteTakerInput.val(data['minuteTaker']);
    attendeeInput.val(data['attendees']);
    guestInput.val(data['guests']);

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
        } else if (data['attendees'][0] === parseInt(value)) {
            data['attendees'].shift();
            chairBar[index].disabled = true;
            minuteTakerBar[index].disabled = true;
            guestBar[index - 1].disabled = true;
        } else if (data['guests'][0] === parseInt(value)) {
            data['guests'].shift();
            chairBar[index].disabled = true;
            minuteTakerBar[index].disabled = true;
            attendeeBar[index - 1].disabled = true;
        }
    })
    $('.selectpicker').selectpicker('refresh');
    appendPresentTag();
});

templateList.on('click', 'li > a:nth-child(2)', function (e) {
    let formData = new FormData();
    formData.append('id', $(this).data('id'));
    $.ajax({
        method: 'POST',
        url: $SCRIPT_ROOT + '/template/delete',
        data: formData,
        success: function () {
            updateTemplateList();
        },
        contentType: false,
        processData: false,
    });
});

function updateTemplateList() {
    $.ajax({
        method: 'GET',
        url: $SCRIPT_ROOT + '/template/get',
        success: function (data) {
            templateList.empty();
            templateContentList = {}
            for (let i = 0; i < data.templateList.length; i++) {
                templateContentList[data.templateList[i]['id']] = data.templateList[i];
                templateList.append(`
                    <li class="d-flex">
                        <a class="dropdown-item" data-id=${data.templateList[i]['id']} href="#">
                            ${data.templateList[i]['name']}
                        </a>
                        <a class="d-flex align-items-center px-3" data-id=${data.templateList[i]['id']} href="#"
                           onmouseover="this.style.background='#E9ECEF'"
                           onmouseout="this.style.background=''">
                            <i class="bi bi-trash-fill text-muted"></i>
                        </a>
                    </li>
                `);
            }
        },
        contentType: false,
        processData: false,
        dataType: 'json'
    });
}