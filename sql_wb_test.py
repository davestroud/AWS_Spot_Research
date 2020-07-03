
import mysql.connector

mydb = mysql.connector.connect(
    host = "aws-spot.cbxr4ccqwh4f.us-east-1.rds.amazonaws.com", 
    user = "admin",
    password = "Barron12#"
)

print(mydb)




