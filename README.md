# TTH
A Text - To - Handwriting converter written in python

Unlike the other online tools that convert text to handwriting, this converter uses actual images of the handwriting to create the complete page rather than using fonts made from handwriting. The advantage of this is that, the handwriting looks more realistic and believeable because it is real.

# Usage
## Capturing the Handwriting
First, we take a photo of our handwriting, then we crop all the individuals using the cropper tool which makes it a lot easier.

## Using the cropper tool
![image](https://user-images.githubusercontent.com/81752891/194687543-5cbfd310-d9ae-4287-bdcd-e561f172ce0d.png)   
The cropper is a python script that utilises the graphical capabilities of pygame module to help you crop the individual letters.

![image](https://user-images.githubusercontent.com/81752891/194687604-2a2beeef-cb81-41ef-aa44-0136f5582ea4.png)   
The black border box helps us to align the letters so that all of them lie on a straight line when they are concatenated.

## Keys
W -> Move the background up  
A -> Move the background left  
S -> Move the background down  
D -> Move the background right  
  
↑ -> Move the border box up  
→ -> Move the border box right  
← -> Move the border box left  
↓ -> Move the border box down  

## Getting the output
Once the cropping of Alphabet and symbols is done, all we have to do is copy some text into the 'text.txt' file and run main.py

# Input
![image](https://user-images.githubusercontent.com/81752891/194688054-3e2d1b18-28b7-4784-b672-3bfd1d0f9361.png)

# Output
![1](https://user-images.githubusercontent.com/81752891/194688038-67281af8-8a7b-4933-996c-94bda234007c.png)
