import mysql.connector
import fpdf
from datetime import datetime
now = datetime.now()
# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="9920",
  database="tedx"
)
mycursor = mydb.cursor(buffered=True)
############################################################################33
def extract_integer(string):
    # Split the string into characters
    characters = list(string)
    
    # Iterate over the characters, appending only digits to a separate list
    digits = []
    for char in characters:
        if char.isdigit():
            digits.append(char)
    
    # Join the digits list into a single string
    digit_string = "".join(digits)
    
    # Convert the digit string to an integer
    integer = int(digit_string)
    
    return integer

def generate_unique_id(email,count):
    # Extract the first three characters of the email
    first_three = email[:3].upper()
    count += 1
    unique_id = first_three + str(count).zfill(3)   
    id_andcntr=[unique_id,count]
    return id_andcntr

def last_id():
    email=input("Enter Last Email in database:")
    sql = "SELECT id FROM tedx WHERE email = %s"
    print(email)
# Execute the query
    mycursor.execute(sql, (email,))
# Fetch the result
    result = mycursor.fetchone()
# Extract the ID from the result
    uid = result[0]
    count=extract_integer(uid)
    return count

def databse_unique_id(email,unique_id):
    sql = "INSERT INTO tedx (email, id) VALUES (%s, %s)"
    val = (email, unique_id)
    mycursor.execute(sql, val)
    mydb.commit()

# Function to send a PDF containing the unique ID
def send_pdf(email, unique_id,name,phno,transid,choice):
    fname=name.split(" ")
    pdf = fpdf.FPDF(orientation = 'P', unit = 'mm', format = 'A4')
    pdf.add_page()
    pdf.set_font('Courier', 'B', 14)
    pdf.set_text_color(0,0,0)
    pdf.image('./pics/t.png', x = 5, y = 80, w = 200, h = 70)
    pdf.set_x(167)
    pdf.cell(600, 215, txt=fname[0].upper(),)
    pdf.set_x(167)
    pdf.cell(600, 247, txt=unique_id,)
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)

    pdf.image('./pics/1.png', x = 0, y = 0, w = 210, h = 300)
    pdf.set_x(163)
    pdf.cell(200, 15, txt=str(now.strftime("%d/%m/%Y")),)
    pdf.set_x(33)
    pdf.cell(200, 115, txt=name,)
    pdf.set_x(43)
    pdf.cell(200, 140, txt=email.upper(),)  
    pdf.set_x(87)
    pdf.cell(200, 165, txt=choice.upper(),)
    pdf.set_x(70)
    pdf.cell(200, 190, txt=phno,)
    pdf.set_x(70)
    pdf.cell(200, 216, txt=transid,)
    pdf.add_page()
    pdf.image('./pics/tt1.png', x = 0, y = 0, w = 200, h = 290)
    pdf.add_page()
    pdf.image('./pics/tt2.png', x = 0, y = 0, w = 200, h = 290)
    pdf.output(f"{unique_id}.pdf")
                                    
#####################################################################################



choice=input("is this first time running the script is so write 'y':  ")
if choice.lower()=="y":
    count=last_id()


while(True):
    c=input("do you wanna countine if not press 'n':   ")
    if c=="n":
        break
    name=input("Enter name:")
    email=input("Enter Email:")
    phno=input("Enter Phone Number:")
    tid=input("Enter Transaction Id:")
    choice=input("Enter A for Adhaar and P for Pancard: ")
    if choice.upper()=="A":
        userid="AADHAR CARD"
    else:
        userid="PAN CARD"
    unique_id=generate_unique_id(email,count)
    databse_unique_id(email,unique_id[0])
    send_pdf(email,unique_id[0],name,phno,tid,userid)
    count=unique_id[1]

