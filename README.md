# Project One
- Northwestern Data Science Bootcamp
- Team members: ayang2012, haneenammouri, Michele-Lodl, jzefron, sponre01

## Thesis
- We are using the __BreweryDB sandbox API__ to explore trends in our favorite brews.
- Starting one's own brewery is as easy as an API connection! Jk. Once we started exploring the data we had to change our thesis: 
#### Activity within the brewing industry will organize into routine consumer behaviors and preferences that will provide market research insights for a Brew Crew aka Brewery entrepreneurs. 

## Questions
__1. Do Budweiser and Miller dominate the database?__
       - JONATHAN 
***     
__2. Styles:__ 
       - Are organic options available?
       - YES! The North American styles category presented the most organic options. This conclusion required accessing and merging two dictionaries within the API -- Styles and Beers -- and simplying this new data from to contain only the Category (which I called Super Style), Style and Organic (Y/N) indicator for the style. The most challenging part of this clean up was being able to manipulate single-style findings reporting to multiple indexes. 
       - (See: organic_only_bar.png)
       - Which styles of beers are within a binned range of abv?
     The NORTH AMERICAN styles presented the most option for the range of abv bins. The challenging element of synthesizing this data was the same challenge presented in the organic challenge above. 
       - (See: which_play_bar.png)
***
__3. How does the established date of a brewery correlate to its distance from Chicago?__
       - _Why Chicago?_ Chicago was one of the “hot-spots” for brewing in early America, thanks to the large population of German immigrants living here. If the trends from this historical context are still present today, then I expect to see a clustering of older American breweries appear closer to Chicago. 
       - _Challenges overcome_: In the data cleaning process, we got stuck on importing data with locations because it was not the default api set up. Jonathan figured out out to access the data with ingredients included, so I used that logic to access the data with locations. Thanks Jonathan! 
        - _More challenges overcome?_: Due to the fact that we were using the sandbox, we only had access to __17 breweries__. Still, plotting the trend using the accessible breweries will give us an idea of whether or not paying for the full version will be worth it. 
        - _Result_: From the scatterplot below, we see there may still be a rough correlation! At the very least, if I wanted to do more with this, I would be convinced by this data to go purchase the full access to the BreweryDB API.
![alt text](https://github.com/sponre01/project-one/blob/master/Images/Distance%20from%20Chicago%20vs.%20Established%20Year.png "Distance from Chicago vs. Established Year")
***
__4. How does the alcohol content of a beer coorelate to styles?__
       - The average alcohol content over all beers is 6.92% by volume. Our data set includes: 1109 individual beers Note: the average abv for beer according to Google is 4.5%. 
       - For this data set, I combined the beer data and the style data and overlayed the two-tailed t-test statistical logic. 
       - (See: Alcohol by Volume Distribution for All Beers.png)
       - In the web application created below highlights the above finding in a user-friendly format. 
       - (See: http://beer-styles.us-east-2.elasticbeanstalk.com/) 
***
__5. Ingredients:__ 
   A. Which breweries report ingredients data base most completely with ingredients data?
   B. SOMETHING WITH HOPS
     JONATHAN
