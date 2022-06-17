$('#loginForm').validate({
    'errorElement': 'span',
    'rules': {
        'email': {
            'required': true,
            'email': true
        },
        'password': {
            'required': true
        },
        'oldPassword': {
            'required': true
        },
        'newPassword': {
            'required': true
        },
        'repeatPassword': {
            'required': true,
            'equalTo': 'input[name="newPassword"]'
        }
    },
    'messages': {
        'email': {
            'required': '必須填寫',
            'email': '請輸入有效的電子郵件'
        },
        'password': {
            'required': '必須填寫'
        },
        'oldPassword': {
            'required': '必須填寫'
        },
        'newPassword': {
            'required': '必須填寫'
        },
        'repeatPassword': {
            'required': '必須填寫',
            'equalTo': '必須和新密碼欄位相同'
        }
    }
});