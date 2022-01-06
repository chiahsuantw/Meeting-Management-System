const person_name = $('#person-data-name').text();
const person_gender = $('#person-data-gender').text();
const person_phone = $('#person-data-phone').text();
const person_email = $('#person-data-email').text();
const person_type = $('#person-data-type').text();
const person_company_name = $('#person-data-company_name').text();
const person_job_title = $('#person-data-job_title').text();
const person_office_tel = $('#person-data-office_tel').text();
const person_address = $('#person-data-address').text();
const person_bank_account = $('#person-data-bank_account').text();
const person_univ_name = $('#person-data-univ_name').text();
const person_dept_name = $('#person-data-dept_name').text();
const person_student_id = $('#person-data-student_id').text();
const person_program = $('#person-data-program').text();
const person_study_year = $('#person-data-study_year').text();

$(document).ready(function () {
    $('#pNameInput').val(person_name);
    if (person_gender === 'Male') {
        $('#pGenderInput1').prop('checked', true);
    } else {
        $('#pGenderInput2').prop('checked', true);
    }
    $('#pPhoneInput').val(person_phone);
    $('#pEmailInput').val(person_email);

    $('#pTypeInput').val(person_type).selectpicker('refresh');

    switch (person_type) {
        case 'DeptProf':
            jobTitleInput.parent().show();
            jobTitleInput.val(person_job_title);
            officeTelInput.parent().show();
            officeTelInput.val(person_office_tel);
            break;
        case 'Assistant':
            officeTelInput.parent().show();
            officeTelInput.val(person_office_tel);
            break;
        case 'OtherProf':
            univNameInput.parent().show();
            univNameInput.val(person_univ_name);
            deptNameInput.parent().show();
            deptNameInput.val(person_dept_name);
            jobTitleInput.parent().show();
            jobTitleInput.val(person_job_title);
            officeTelInput.parent().show();
            officeTelInput.val(person_office_tel);
            addressInput.parent().show();
            addressInput.val(person_address);
            bankAccountInput.parent().show();
            bankAccountInput.val(person_bank_account);
            break;
        case 'Expert':
            companyNameInput.parent().show();
            companyNameInput.val(person_company_name);
            jobTitleInput.parent().show();
            jobTitleInput.val(person_job_title);
            officeTelInput.parent().show();
            officeTelInput.val(person_office_tel);
            addressInput.parent().show();
            addressInput.val(person_address);
            bankAccountInput.parent().show();
            bankAccountInput.val(person_bank_account);
            break;
        case 'Student':
            studentIdInput.parent().show();
            studentIdInput.val(person_student_id);
            programInput.parent().parent().show();
            programInput.val(person_program).selectpicker('refresh');
            studyYearInput.parent().parent().show();
            studyYearInput.val(person_study_year).selectpicker('refresh');
            break;
    }
});

$('#editPersonBtn').on('click', function () {
    // The form validation state updates when changes were made in the form
    // And it triggers the validation process before clicking the submit button
    // We add .has-validated class to mark if the button was clicked
    // and remove it if the user decided to cancel the process
    newPersonForm.addClass('has-validated');

    if (!newPersonForm.valid()) {
        // If NewMeetingForm is invalid -> Don't send form post
        $('#personFormArea').animate({scrollTop: 10000}, 1);
        return;
    }

    newPersonForm.submit();
});