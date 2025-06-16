def auth_decorator(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if role!="ADMIN":
                print("Access Denied")
                return
            else:
                print("Authorized")
                return func(*args, **kwargs)
        return wrapper
    return decorator

@auth_decorator("ADMIN")
def updateUser():
    print("User Updated")


@auth_decorator("USER")
def deleteUser():
    print("User Updated")

updateUser()
deleteUser()
                
