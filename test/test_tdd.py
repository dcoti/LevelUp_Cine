

class Test_Cine:
    def test_login(self):
        user_data={
            'user':"danielcoti7@gmail.com",
            'password': "123"
        }
        message=login(**user_data)
        assert message =='ok'
        from check import login
        