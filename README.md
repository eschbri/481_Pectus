link to github: https://github.com/eschbri/481_Pectus.git

Option 1 run from exe file

1. This is a link to our mBox https://drive.google.com/open?id=0ByFFHp27P4hAN3ZfU3pfek40dUU. Download all dist files and make sure the images are all in the same directory as the exe file.

2. open dist file and click on exec.exe and the application should open up

3. Open the .obj file included in the box folder

Option 2 Run from Source

1. First you will need to get pyqt5, scipy, numpy. We used python 2.7. We all just downloaded anaconda and used that, because we had problems getting the dependencies.

2. Get the source code from github the qt project is contained within mPect/

3. run the script python exec.py

4. An obj file is included in the google drive folder: https://drive.google.com/open?id=0ByFFHp27P4hAN3ZfU3pfek40dUU

Our application reads in an obj file for a patient's chest, and displays it to them. Once the obj file is displayed, the user can select a 2D slice of the chest. Calculations can then be performed on this slice.

How to use application

1. Open up an obj file. Any obj of a patients chest will do but we recommend using PT18E.obj

2. After opening the obj file you will see a plot of the patient's chest. This is a 2D image constructed directly from the obj file. Some of the scans need to be flipped 180 degrees, others do not. To flip the image press the Flip Y button located in the bottom right.

3. To create a slice click anywhere on the patient's chest. We recommed clicking in the middle or upper-middle area of the chest to produce a slice with a prominent defect. Creating a slice takes a second or two, so be patient. Also if the first slice does not have a noticeable defect, just click on the of the chest image again to produce another slice. Some slices will have arms attached to them, and others will automatically be chopped off. See the next step for editing the slice.

4. Once you have a slice with a reasonable chest defect it is time to edit the slice. If there are no arms on the slice then you can skip this step :). Otherwise press the Edit Mode button, this will put you into editing mode. While in this mode press two points on the slice, one above where the arm connects to the chest and one below. This draws a line, then press the side of the slice which you would like to remove. Do this to both arms and then we can use the editing features.

5. With our edited slice we can press the Haller Index button, this will draw the Haller index on the chest and display the calculated value to the user. Make sure before you press the haller button the 2d slice has the arms properly cropped and that the slice has a standard concave at the Sternum otherwise the haller index will not be properly calculated. This step was manual but we have made it automated :)

6. Next lets calculate an asymmetry ratio, this is the area ratio between the left side of the chest and the right side of the chest. Press the Asymmetry Ratio button, this puts you into asymmetry mode. Then select the slice, you will see a red ine which divides the two the two sides. 

7. Finally lets calculate a defect ratio. Press the Defect/Chest Ratio button, then press point on the chest where the defect peaks, you will see a red dot appear. Then press another point where the chest peaks, but on the other side of the defect. This will create a line which cuts across the top of the defect and calculates the ratio.
