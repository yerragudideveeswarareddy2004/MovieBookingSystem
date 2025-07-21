import smtplib
import random

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    sender = 'your_email@gmail.com'  # Replace with your email
    password = 'your_email_password'  # Replace with your app password
    message = f"Subject: Your OTP\n\nYour OTP is {otp}"

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, email, message)
    return otp

if __name__ == "__main__":
    email = input("Enter your email: ")
    print("OTP sent:", send_otp(email)) 