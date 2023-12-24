Collection of very small pet-projects. Contents as of now: -

- Web scrapping of exonyms and endonyms for Czech Republic, Poland, Latvia, Lithuania and Estonia. ([Dataset](https://huggingface.co/datasets/DebasishDhal99/German-Names-Middle-And-Eastern-Europe))
  
- Random walk visualization. 2D Random walk consisting of single and multi-agents. ([Application](https://huggingface.co/spaces/DebasishDhal99/Random-Walk-Visualization))
  
- Images and Colors - It takes an image as its input and you get to play with the RGB channels for the image.
  - It's working perfectly in my VSCode, for some reason it's malfunctioning in HuggingFace. It appears that the ordering of RGB channels is different in VSCode and HuggingFace (It sounds weird but this is what it seems to be happening).
    
- Video shuffling -It takes a video adress as input, cuts out chunks out of it randomly and stiches them together to create a new video clip.
  -  Only problem is that the library is throwing error for long videos. For small videos (50 seconds or so), it's working fine. Using this script, I created a mashup video of a video of nature with horses and penguins. This script can be further expanded to use multiple videos at once.
    
- Automated LeetCode Rank Retrieval : - A small Python script that scraps the rank from Leetcode everyday. The script is triggered by a scheduler.
