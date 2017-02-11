
import java.io.*;
import processing.core.PImage;
import processing.core.*;

public class AreaRatio extends PApplet{
	PImage chest;
	public void setup() {
		chest = loadImage("paintfinal2dchest100.png");
		System.out.println("SETUP!");
		int totalPixels = chest.height * chest.width;
		chest.loadPixels();
		double blackPixelCount = 0;
		double whitePixelCount = 0;
		for(int i = 0; i < totalPixels; ++i){
			if(chest.pixels[i] == color(0,0,0))
				blackPixelCount += 1;
			else if(chest.pixels[i] == color(255,255,255))
				whitePixelCount += 1;
		}
		System.out.println("black pixels: " + blackPixelCount);
		System.out.println("white pixels: " + whitePixelCount);
		System.out.println("grey pixels: " + (totalPixels - (whitePixelCount + blackPixelCount)));
		System.out.println("defect / chest ratio: " + (whitePixelCount / blackPixelCount));
	}
	
	public static void main(String[] args) {
		System.out.println("HELLO JAVA!");
		PApplet.main("AreaRatio");
		/*
	  	HELLO JAVA!
			SETUP!
			black pixels: 299602.0
			white pixels: 17332.0
			grey pixels: 54294.0
			defect / chest ratio: 0.05785008110760275
		 */
	}

}
