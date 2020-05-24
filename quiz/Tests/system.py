import unittest, os, time
from selenium import webDriver
from app import app,db
from app.models import User
basedir = os.path.abspath(os.path.dirname(__file__))


class SystemTest(unittest.TestCase):

    def setUp(self):
        self.driver = webDriver(Firefox(executable_path = os.path.join(basedir,'geckodriver')))
        if not self.driver:
            self.skipTest
        else:
            db.init_app(app)
            db.create_all()
            db.session.query(User).delete()
            u = User(id = 1, username = 'testman', admin = True, email = 'testman@test.com')
            u.set_password('Password1')
            db.session.add(u)
            db.session.commit()
            self.diver.maximise_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()
    
    def test_index(self):
        u = User.query.get(1)
        name =  u.get()
        self.assertFalse(u.check_password('pw'))
        self.assertTrue(u.check_password('Password1'))

    def test_password_sensitivity(self):
        u = User.query.get(1)
        u.set_password('Password1')
        self.assertFalse(u.check_password('password1'))
        self.assertTrue(u.check_password('Password1'))

    
    
if __name__ == '__main__' :
    unittest.main(verbosity=2)