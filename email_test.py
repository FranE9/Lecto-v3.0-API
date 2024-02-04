from smtplib import SMTP

email = input("SENDER EMAIL: ")
receiver_email = input("RECEIVE EMAIL: ")

subject = input("SUBJECT: ")
message = input("MESSAGE: ")

text = f"Subject: {subject}\n\n{message}"

server = SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, "ytfmskwmperussmm")

server.sendmail(email, receiver_email, text)

print("El correo ha sido enviado a " + receiver_email)