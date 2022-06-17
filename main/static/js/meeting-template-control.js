const templateSaveForm = $('#templateSaveForm');

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
    // TODO: 用 Ajax 儲存模板
});

// TODO: 更新套用模板列表
// TODO: 點擊套用模板列表 -> 套用模板