def find_users(file_name):
    users = []
    f = open(file_name, "r", encoding="UTF8")
    f = f.read()
    f = f.split("<span class")
    for item in f:
        if "_ap3a _aaco _aacw _aacx _aad7 _aade" in item:
            users.append(item[50:item.find("</span")])

    
    return users

def check_for_new_unfollowers():
    old_followers = find_users("my_followers_OLD_LATEST.txt")
    new_followers = find_users("my_followers_current.txt")

    print("Old count: ",len(old_followers),"New count: ",len(new_followers))

    olds = []
    for old in old_followers:
        if old not in new_followers:
            olds.append(old)
        

    news = []
    for new in new_followers:
        if new not in old_followers:
            news.append(new)

    print("Those who left: ",olds,"\n\n\n","Those who came: ",news)


def check_not_following():
    following = find_users("my_following.txt")
    followers = find_users("my_followers_current.txt")

    not_following_me_back = []
    for person in following:
        if person not in followers:
            not_following_me_back.append(person)
    print("Not following you back: ",not_following_me_back,"\n",len(not_following_me_back),"\n")

    not_following_them_back = []
    for person in followers:
        if person not in following:
            not_following_them_back.append(person)
    print("Not following them back: ",not_following_them_back)
    print(len(not_following_them_back),"\n")

if __name__ == "__main__":
    op = input("1 to check new unfollowers, 2 to check current follower vs following difference\n")
    if "check new" in op or "1" in op:
        check_for_new_unfollowers()
    elif "not following" in op or "2" in op:
        check_not_following()
    