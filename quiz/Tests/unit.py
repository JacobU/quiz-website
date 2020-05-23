import unittest
from app import app,db
from app.models import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        try:
            db.session.query(User).delete()
        except:
            print("no db to delete")
        db.create_all()
        u = User(id = 1, username = 'testman', admin = True, email = 'testman@test.com')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_set_password(self):
        u = User.query.get(1)
        u.set_password('Password1')
        self.assertFalse(u.check_password('pw'))
        self.assertTrue(u.check_password('Password1'))

    def test_password_sensitivity(self):
        u = User.query.get(1)
        u.set_password('Password1')
        self.assertFalse(u.check_password('password1'))
        self.assertTrue(u.check_password('Password1'))

    
    
if __name__ == '__main__' :
    unittest.main(verbosity=2)