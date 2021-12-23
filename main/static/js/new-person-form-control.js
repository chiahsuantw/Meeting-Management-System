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
const allSelectPicker = $('.selectpicker');

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
    programInput.val('');
    studyYearInput.parent().parent().hide();
    studentIdInput.val('');
    allSelectPicker.selectpicker('refresh');

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
        let form_data = new FormData();

        form_data.append('name', $('#pNameInput').val());
        form_data.append('gender', $('#pGenderInput1').prop('checked') ? 'Male' : 'Female');
        form_data.append('phone', $('#pPhoneInput').val());
        form_data.append('email', $('#pEmailInput').val());
        form_data.append('type', $('#pTypeInput').val());

        switch (personType.val()) {
            case 'DeptProf':
                form_data.append('jobTitle', jobTitleInput.val());
                form_data.append('officeTel', officeTelInput.val());
                break;
            case 'Assistant':
                form_data.append('officeTel', officeTelInput.val());
                break;
            case 'OtherProf':
                form_data.append('univName', univNameInput.val());
                form_data.append('deptName', deptNameInput.val());
                form_data.append('jobTitle', jobTitleInput.val());
                form_data.append('officeTel', officeTelInput.val());
                form_data.append('address', addressInput.val());
                form_data.append('bankAccount', bankAccountInput.val());
                break;
            case 'Expert':
                form_data.append('companyName', companyNameInput.val());
                form_data.append('jobTitle', jobTitleInput.val());
                form_data.append('officeTel', officeTelInput.val());
                form_data.append('address', addressInput.val());
                form_data.append('bankAccount', bankAccountInput.val());
                break;
            case 'Student':
                form_data.append('studentId', studentIdInput.val());
                form_data.append('program', programInput.val());
                form_data.append('studyYear', studyYearInput.val());
                break;
        }

        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: $SCRIPT_ROOT + '/new/person',
            data: form_data,
            success: (data) => {
                if (data.validate === 'Success') {
                    // Reset the form
                    $('#newPersonForm').trigger('reset');
                    personType.val('');
                    personType.selectpicker('refresh');
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
                    console.log(data.validate);
                }
            },
            contentType: false,
            processData: false,
        });
    }
);

$('.close-new-person').on('click', function () {
    $('#newPersonForm').trigger('reset');
    personType.val('');
    personType.selectpicker('refresh');
    personTypeFormControl();
});