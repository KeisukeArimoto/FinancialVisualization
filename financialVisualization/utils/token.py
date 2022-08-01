import jwt


class TokenGenerator:
    # TODO 鍵でやるかパスワードをDB保存でやる
    key = 'password'

    def __init__(self):
        pass

    def generateToken(self, payload_data):
        token = jwt.encode(payload=payload_data,
                           key=self.key)
        return token

    def decodeToken(self, token):
        return jwt.decode(jwt=token, key=self.key, algorithms='HS256')
