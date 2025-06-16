import bcrypt
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    def __post_init__(self):
        # Any initialization after the dataclass is created
        if self.password:
            self._hash_password()
    
    def _hash_password(self):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), salt)
    
    def verify_password(self, password: str) -> bool:
        if not self.password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
    
    def print(self):
        # Method 1: Using or operator for default values
        name = self.name or "No name"
        username = self.username or "No username"
        
        # Method 2: Using getattr with defaults
        dob = getattr(self, 'dob', 'Not specified')
        address = getattr(self, 'address', 'Not specified')
        
        # Method 3: Using is operator for explicit None check
        if self.password is not None:
            password_str = f"My password is {str(self.password)}"
        else:
            password_str = "No password set"
            
        # Method 4: Using ternary operator
        email = f"My email is {self.email}" if self.email is not None else "No email set"
        phone = f"My phone is {self.phone}" if self.phone is not None else "No phone set"
        
        # Print all information
        print(f"Hi my name is {name}, My username is {username}, {password_str}")
        print(f"My Date of Birth is {dob}, My address is {address}")
        print(f"{email}, {phone}")

# Example usage:
# Method 1: Using dataclass initialization
user1 = User(name="John", email="john@example.com")

# Method 2: Using builder pattern (still works)
user2 = User()
user2.name = "Alice"
user2.email = "alice@example.com"
user1.password="mySecurePassword"

# Method 3: Using setattr
user3 = User()
setattr(user3, 'name', 'Bob')
setattr(user3, 'email', 'bob@example.com')

# Print all users
user1.print()
user2.print()
user3.print()


        