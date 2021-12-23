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

$(document).ready(function () {
    // Run this function after the Html has loaded
    personTypeFormControl();
    personType.change(personTypeFormControl);
});

function personTypeFormControl() {
    // Control the display of fields depending on personType
    companyNameInput.parent().hide();
    univNameInput.parent().hide();
    deptNameInput.parent().hide();
    jobTitleInput.parent().hide();
    officeTelInput.parent().hide();
    addressInput.parent().hide();
    bankAccountInput.parent().hide();
    studentIdInput.parent().hide();
    programInput.parent().parent().hide();
    studyYearInput.parent().parent().hide();

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