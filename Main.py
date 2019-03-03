# this runs the file

from ATM import *

def main():
    login = userLogin()
    user = login.getUser()
    interface= GraphicInterface()
    app = ATM(user, interface)
    app.run()
    interface.closeInterface()
    
main()
