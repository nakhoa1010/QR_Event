import mysql.connector
import cv2
from datetime import datetime
import takeimage as takeimage

def get_image_name(QRID):
  image_name = QRID + '.jpg'
  return image_name

def current_time():
  now = datetime.now()
  dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
  return dt_string

def return_status(flag):
  if flag == 0:
    return "vao lan dau"
  elif flag == 1:
    return "da ra giua gio"

def return_sex(sex):
  if sex == "Nam":
    return "Ong"  
  elif sex == "Nu":
    return "Ba"

def connect_database():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="qrevent"
  )
  return mydb

def check_available(QRID): 
  mydb = connect_database()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT ID FROM yourtablename WHERE QRID = %s",(QRID,))
  available = mycursor.fetchone()
  return available
  
def check(datain):
  mydb = connect_database()
  
  QRID = datain
  
  mycursor = mydb.cursor()
  mycursor.execute("SELECT Flag, GioiTinh, Ten, TimeIn, FacePath FROM yourtablename WHERE QRID = %s",(QRID,))
  myresult = mycursor.fetchall()
  result = list(myresult[0])
  
  flag = result[0]
  sex = result[1]  
  name = result[2]
  timein = result[3]
  facepath = result[4]
  # print ("Ho Va Ten: ",name,"\nGioiTinh: ",sex,"\nTrang thai: ",check_status(flag),"\nHinh anh:",facepath,"Thoi gian vao: ",timein)
  print("Xin chao",return_sex(sex), name)
  print("Quy khach",return_status(flag))
  if (flag == 0):
    
    #__Chen code chup hinh vao day_
    img_path = takeimage.capture(get_image_name(QRID))
    print('Created ' + get_image_name(QRID) + ' image.')
    print('Save to: ' + img_path)
    #______________________________
    newdate = current_time()
      
    mycursor.execute("UPDATE yourtablename SET flag = 1, TimeIn = %s, FacePath = %s WHERE QRID = %s",(newdate,img_path,QRID,))
    mydb.commit()
    print("Thoi gian: ", newdate)
  elif (flag==1):
    print("Thoi gian vao lan dau: ", timein)

    
if __name__ == "__main__":
  check('EventA-abc124xyz')