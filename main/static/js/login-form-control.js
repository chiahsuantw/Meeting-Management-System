$('#loginForm').validate({
    'errorElement': 'span',
    'rules': {
        'email': {
            'required': true,
            'email': true
        }
    },
    'messages': {
        'email': {
            'required': '必須填寫',
            'email': '請輸入有效的電子郵件'
        }
    }
});