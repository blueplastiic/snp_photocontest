import re

def validate_password(password):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@?#$%^&+=-_]).{8,20}$"
    return re.match(pattern, password)

#between 8 and 20 characters
#at least one digit
#at least one lowercase
#at least one uppercase
#at least one special symbol (@ ? # $ % ^ & + =)
