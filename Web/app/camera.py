import cv2
from views import * 

def takePicture(naam):
        
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")
    cv2.namedWindow("img")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            cv2.imshow("img" , frame)
            #if k2%256 == 13:
            img_name = "opencv_frame_{}.png".format(img_counter)
            img_path = "app/static/img/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_path, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            url = img_path 
            filename = img_name
            person = Persons.query.filter_by(person_name = naam).first()
            image = AuthImageGallery(image_filename= filename, image_path= url, person_id = person.person_id )
            db.session.add(image)
            db.session.commit()
        


    cv2.destroyAllWindows()