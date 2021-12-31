const personType = $('#pTypeInput');
const companyNameInput = $('#pCompanyNameInput');
const univNameInput = $('#pUnivNameInput');
const deptNameInput = $('#pDeptNameInput');
const jobTitleInput = $('#pJobTitleInput');
const officeTelInput = $('#pOfficeTelInput');
const addressInput = $('#pAddressInput');
const bankAccountInput = $('#pBankAccountInput');
const studentIdInput = $('#pStudentIdInput');
const programInput = $('#pProgramInput');
const studyYearInput = $('#pStudyYearInput');

const personTypeSwitch = {
    'DeptProf': '系上教師',
    'Assistant': '系助理',
    'OtherProf': '校外教師',
    'Expert': '業界專家',
    'Student': '學生'
}

$(document).ready(function () {
    // Run this function after the Html has loaded
    personTypeFormControl();
    personType.on('change', personTypeFormControl);
});

function personTypeFormControl() {
    // Control the display of fields depending on personType
    companyNameInput.parent().hide();
    companyNameInput.val('');
    univNameInput.parent().hide();
    univNameInput.val('');
    deptNameInput.parent().hide();
    deptNameInput.val('');
    jobTitleInput.parent().hide();
    jobTitleInput.val('')
    officeTelInput.parent().hide();
    officeTelInput.val('');
    addressInput.parent().hide();
    addressInput.val('');
    bankAccountInput.parent().hide();
    bankAccountInput.val('');
    studentIdInput.parent().hide();
    studentIdInput.val('');
    programInput.parent().parent().hide();
    programInput.val('').selectpicker('refresh');
    studyYearInput.parent().parent().hide();
    studyYearInput.val('').selectpicker('refresh');

    switch (personType.val()) {
        case 'DeptProf':
            jobTitleInput.parent().show();
            officeTelInput.parent().show();
            break;
        case 'Assistant':
            officeTelInput.parent().show();
            break;
        case 'OtherProf':
            univNameInput.parent().show();
            deptNameInput.parent().show();
            jobTitleInput.parent().show();
            officeTelInput.parent().show();
            addressInput.parent().show();
            bankAccountInput.parent().show();
            break;
        case 'Expert':
            companyNameInput.parent().show();
            jobTitleInput.parent().show();
            officeTelInput.parent().show();
            addressInput.parent().show();
            bankAccountInput.parent().show();
            break;
        case 'Student':
            studentIdInput.parent().show();
            programInput.parent().parent().show();
            studyYearInput.parent().parent().show();
            break;
    }
}

$('#newPersonBtn').on('click', function () {
    let formData = new FormData();

    formData.append('name', $('#pNameInput').val());
    formData.append('gender', $('#pGenderInput1').prop('checked') ? 'Male' : 'Female');
    formData.append('phone', $('#pPhoneInput').val());
    formData.append('email', $('#pEmailInput').val());
    formData.append('type', $('#pTypeInput').val());

    switch (personType.val()) {
        case 'DeptProf':
            formData.append('jobTitle', jobTitleInput.val());
            formData.append('officeTel', officeTelInput.val());
            break;
        case 'Assistant':
            formData.append('officeTel', officeTelInput.val());
            break;
        case 'OtherProf':
            formData.append('univName', univNameInput.val());
            formData.append('deptName', deptNameInput.val());
            formData.append('jobTitle', jobTitleInput.val());
            formData.append('officeTel', officeTelInput.val());
            formData.append('address', addressInput.val());
            formData.append('bankAccount', bankAccountInput.val());
            break;
        case 'Expert':
            formData.append('companyName', companyNameInput.val());
            formData.append('jobTitle', jobTitleInput.val());
            formData.append('officeTel', officeTelInput.val());
            formData.append('address', addressInput.val());
            formData.append('bankAccount', bankAccountInput.val());
            break;
        case 'Student':
            formData.append('studentId', studentIdInput.val());
            formData.append('program', programInput.val());
            formData.append('studyYear', studyYearInput.val());
            break;
        }

        $.ajax({
            'type': 'POST',
            'dataType': 'json',
            'url': $SCRIPT_ROOT + '/new/person',
            'data': formData,
            'success': (data) => {
                if (data['message'] === 'Success') {
                    // Reset the form
                    $('#newPersonForm').trigger('reset');
                    personType.val('').selectpicker('refresh');
                    personTypeFormControl();
                    // Close the modal
                    // noinspection JSUnresolvedFunction
                    $('#newPersonModal').modal('hide');
                    // Add person options dynamically
                    const optionElement =
                        '<option value="' + data['person']['id'] +
                        '" data-subtext="(' + data['person']['email'] + ') ' +
                        personTypeSwitch[data['person']['type']] +
                        '">' + data['person']['name'] + '</option>'
                    $('.person-select > select').append(optionElement).selectpicker('refresh');
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

$('.close-new-person').on('click', function () {
    $('#newPersonForm').trigger('reset');
    personType.val('').selectpicker('refresh');
    personTypeFormControl();
});