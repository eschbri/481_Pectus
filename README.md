link to github: https://github.com/eschbri/481_Pectus.git

Option 1 run from exe file

1. This is a link to our mBox https://drive.google.com/drive/folders/0BwM6SpLL5_1uX2dTclZXUWVLUEk?usp=sharing. Download all dist files and make sure the images are all in the same directory as the exe file.

2. open dist file and click on qtArea.exe and the application should open up

Option 2 Run from Source

1. First you will need to get pyqt5, scipy, numpy. We used python 2.7. We all just downloaded anaconda and used that, because we had problems getting the dependencies.

2. Get the source code from github the qt project is contained within areapython.

3. run the script python qtArea.py

How to use application

1. The gui shows three buttons at the top row that allow you to set the boundaries for the left, right defect, and a center line for the calculate defect / chest ratio button and the calculate left / right asymmetry ratio button. The switch back to default image button allows you to switch back to the default image of the slice you are on. The display boundies button allows you to see the set boundary lines.

2. Next you have the set haller index buttons. The haller index is the ratio of distance lung width from left side to right side and the distance from vertebre to sternum. To set the horizontal points you want to include in your index, click on the set horizontal haller button and click on the two points of the image you want to set the horizontal component of the haller index to. Then you have to set the vertical component of the index, click on the set vertical haller button and choose the two points on the image that you want to include in the index.

3. Lastly you have the set vertical lung front to lung back and the set vertical from the sternum to vertebre buttons. You must click on both buttons and set two points for each button to output a lung back to front / sternum to vertebre ratio.

4. Also there is a blue slider widget component between the 2d slice image and the large chest image. You can move the slider widget up and down to see different slices of the 3d object. You can perform any of the mentioned computations to any of the slices included.