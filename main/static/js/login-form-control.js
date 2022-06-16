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
        'newPassword': {
            'required': true
        },
        'oldPassword': {
            'required': true
        },
        'repeatPassword': {
            'required': true
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
        'newPassword': {
            'required': '必須填寫'
        },
        'oldPassword': {
            'required': '必須填寫'
        },
        'repeatPassword': {
            'required': '必須填寫'
        }
    }
});