from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        user = User(username='john', email='john@example.com')
        self.assertEqual(user.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user1.followers.all(), [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, 'susan')
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, 'john')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        user3 = User(username='mary', email='mary@example.com')
        user4 = User(username='david', email='david@example.com')
        db.session.add_all([user1, user2, user3, user4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=user1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=user2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=user3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=user4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        user1.follow(user2)  
        user1.follow(user4) 
        user2.follow(user3) 
        user3.follow(user4)  
        db.session.commit()

        # check the followed posts of each user
        f1 = user1.followed_posts().all()
        f2 = user2.followed_posts().all()
        f3 = user3.followed_posts().all()
        f4 = user4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
