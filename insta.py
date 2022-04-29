import instaloader
from instaloader import Profile

db = 'fatkhullaev_b'
pascode = '.bahrullo.2003.'
L = instaloader.Instaloader()


def insta(x):
    L.login(db, pascode)
    profile = instaloader.Profile.from_username(L.context, db)
    followers = profile.get_followers()
    for follower in followers:
        if follower.username == x:
            return True

    return False