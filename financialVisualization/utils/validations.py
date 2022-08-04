import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator():
    msg = 'パスワードには数字と英字を含めてください。'

    def __init__(self):
        pass

    def validate(self, password, user=None):
        # バリデーションを追加する
        if all((re.search('[0-9]', password), re.search('[a-zA-Z]', password))):
            return
        raise ValidationError(self.msg)
