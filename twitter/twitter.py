from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """

    def __init__(self):
        self.logged_in = False
        self.handle = None
        self.current_user = None

    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        registered = False
        while (registered == False):
            handle = input("What will your twitter handle be? ")
            init_pass = input("Enter a password: ")
            check_pass = input("Re-enter the password: ")
            existing_user = db_session.query(User).filter(User.username == handle).first()
            if (existing_user):
                print("This handle is taken.")
            elif (init_pass != check_pass):
                print("The passwords don't match.")
            else:
                registered = True
                final_pass = init_pass
        print("Welcome: " + handle)
        new_user = User(username = handle, password = final_pass)
        db_session.add(new_user)
        db_session.commit()         
                  
    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        username_check = None
        password_check = None
        while (self.logged_in == False):
            username_check = input("Username: ")
            password_check = input("Password: ")
            user = db_session.query(User).filter((User.username == username_check) & (User.password == password_check)).first()
            if(user):
                self.logged_in = True
                self.current_user = user
            else:
                print("Invalid username or password")

        

    
    def logout(self):
        self.logged_in = False
    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        user_input = input("Welcome to ATCS Twitter" + "\n" + "Please select a menu option" + "\n" + 
                            "1. Login" + "\n" + "2. Register" + "\n" + "0. Exit")
        if user_input == "1":
            self.login()
        elif user_input == "2":
            self.register_user()
        elif user_input == "0":
            self.end()
        

    def follow(self):
        other_user_username = input("Who would you like to follow?" + "\n")
        other_user = db_session.query(User).filter(User.username == other_user_username).first()
        
        if other_user is not None:
            db_session.add(Follower(follower_id = self.current_user.username, following_id = other_user.username))
            print("\n\nYou now follow @" + other_user.username)
        else:
            print("Username entered incorrectly")
        db_session.commit()

    def unfollow(self):
        following_username = input("Who would you like to unfollow\n")
        followed = db_session.query(Follower).where((Follower.follower_id==self.current_user.username) & (Follower.following_id==following_username)).first()
        if followed is not None:
            db_session.delete(followed)
            print("\n\nYou unfollowed @" + following_username)
        else:
            print("You dont follow @" + following_username)
        db_session.commit()

    def tweet(self):
        message = input("Create Tweet: ")
        tags = input("Enter your tags separated by spaces: ").split()
        tags = [Tag(content = tag) for tag in tags]
        db_session.commit()
        new_tweet = Tweet(message, datetime.now(), tags, self.current_user.username)
        db_session.add(new_tweet)
        db_session.commit()

    
    def view_my_tweets(self):
        my_tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username).all()
        self.print_tweets(my_tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        following_usernames = [user.username for user in self.current_user.following]
        tweets = db_session.query(Tweet).where(Tweet.username.in_(following_usernames)).order_by(Tweet.timestamp).limit(5).all()
        self.print_tweets(tweets)

    def search_by_user(self):
        username = input("Username: ")
        user = db_session.query(User).where(User.username == username).first()
        if (user):
            user_tweets = db_session.query(Tweet).where(Tweet.username == username)
            self.print_tweets(user_tweets)
        else:
            print("There is no user by that name.")

    def search_by_tag(self):
        tag = input("Tag: ")
        check_tag = db_session.query(Tag).where(Tweet.tags.has(tag))
        if check_tag:
            
            tagged_tweets = db_session.query(Tweet).where(Tweet.tags == tag)
        else:
            print("There is no tweets with this tag.")


    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while(self.logged_in == True):
            self.print_menu()
            option = int(input(""))
            db_session.commit()
            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
            
            self.end()
