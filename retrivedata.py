import mysql.connector
import cv2
import time
from datetime import datetime
import takeimage as takeimage
def get_image_name(QRID):
  image_name = QRID + '.jpg'
  return image_name

def current_time():
  now = datetime.now()
  dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
  return dt_string

def return_status(facepath):
  if facepath == None:
    return "vao lan dau"
  else:
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

def capture(image_name):
    cap = cv2.VideoCapture(0) # 0 for default webcam
    start_time = time.time()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if 10 seconds have passed
        if time.time() - start_time >= 5:
            # Save the image
            save_path = "facepath\\" + image_name 
            cv2.imwrite(save_path, frame)
            break
        # Display the resulting frame
        cv2.putText(frame, 'Wait 5 seconds', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('frame', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    path = "facepath\\" +  image_name
    return path
    cap.release()
    cv2.destroyAllWindows()
  
def check(datain):
  mydb = connect_database()
  
  QRID = datain
  
  mycursor = mydb.cursor()
  mycursor.execute("SELECT GioiTinh, Ten, TimeIn, FacePath FROM yourtablename WHERE QRID = %s",(QRID,))
  myresult = mycursor.fetchall()
  result = list(myresult[0])
  
  
  sex = result[0]  
  name = result[1]
  timein = result[2]
  facepath = result[3]
  # print ("Ho Va Ten: ",name,"\nGioiTinh: ",sex,"\nTrang thai: ",check_status(flag),"\nHinh anh:",facepath,"Thoi gian vao: ",timein)
  print("Xin chao",return_sex(sex), name)
  print("Quy khach",return_status(facepath))
  if (facepath == None):
    
    #__Chen code chup hinh vao day_
    img_path = capture(get_image_name(QRID))
    print('Created ' + get_image_name(QRID) + ' image.')
    print('Save to: ' + img_path)
    #______________________________
    newdate = current_time()
      
    mycursor.execute("UPDATE yourtablename SET TimeIn = %s, FacePath = %s WHERE QRID = %s",(newdate,img_path,QRID,))
    mydb.commit()
    print("Thoi gian: ", newdate)
  else:
    print("Thoi gian vao lan dau: ", timein)

    
if __name__ == "__main__":
  check('EventA-abc124xyz')
