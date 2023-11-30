import cv2
import os # for directory reading operations

if __name__ == "__main__":        
    # establish how to name/id output images
    # count number of files in images folder
    dir_path = 'images\calibration'
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    if count % 2 != 0:
        count += 1 #in case number of files is odd for any reason
        
    # OpenCV webcam test
    print('opening cam 1')
    cam0 = cv2.VideoCapture(0, cv2.CAP_DSHOW) #left
    print('cam 1 opened')
    cam0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam0.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam0.set(cv2.CAP_PROP_FPS, 10)
    print('cam 1 configured')
    
    print('opening cam 2')
    cam1 = cv2.VideoCapture(1, cv2.CAP_DSHOW) #right
    print('cam 2 opened')
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam1.set(cv2.CAP_PROP_FPS, 10)
    print('cam 2 configured')
    
    # cv2.namedWindow('cam left', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('cam right', cv2.WINDOW_NORMAL)
    
    while True:
        check0, i0 = cam0.read()
        assert(check0)
        # i0 = cv2.cvtColor(i0, cv2.COLOR_BGR2GRAY)
        # i0 = cv2.cvtColor(i0)
        
        check1, i1 = cam1.read()
        assert(check0)
        # i1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
        # i1 = cv2.cvtColor(i1)
        
        cv2.imshow('cam left', i0)
        cv2.imshow('cam right', i1)

        key = cv2.waitKey(50)
        if key == 27:
            break
        elif key == ord('s') or key == ord('.'):
            print('Saving image pair ' + str(count//2))
            cv2.imwrite('images/calibration/webcam_left_' + str(count // 2) + '.png', i0)
            cv2.imwrite('images/calibration/webcam_right_' + str(count // 2) + '.png', i1)
            count += 2
        # else:
        #     print('Saving image pair ' + str(count//2))
        #     cv2.imwrite('./images/webcam_left_' + str(count // 2) + '.png', i0)
        #     cv2.imwrite('./images/webcam_right_' + str(count // 2) + '.png', i1)
        #     count += 2
    
    cam0.release()
    # cam1.release()
    cv2.destroyAllWindows()
