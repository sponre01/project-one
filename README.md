# project-one
Data Science Bootcamp - first project

# Thesis
- Starting one's own brewery is as easy as an API connection! Jk. Once we started exploring the data we had to change our thesis: 
### Activity within the brewing industry will organize into routine consumer behaviors and preferences that will provide market research insights for a Brew Crew aka Brewery entrepreneurs. 

# Questions
1. Do Budweiser and Miller dominate the database?
     JONATHAN 
     
2. Styles: 
     - Are organic options available?
     
     YES! The North American styles category presented the most organic options. This conclusion required accessing and merging two dictionaries within the API -- Styles and Beers -- and simplying this new data from to contain only the Category (which I called Super Style), Style and Organic (Y/N) indicator for the style. The most challenging part of this clean up was being able to manipulate single-style findings reporting to multiple indexes. 
     - (See: organic_only_bar.png)
       
     - Which styles of beers are within a binned range of abv?
     The NORTH AMERICAN styles presented the most option for the range of abv bins. The challenging element of synthesizing this data was the same challenge presented in the organic challenge above. 
     - (See: which_play_bar.png)
     
3. How does the established date of a brewery correlate to its distance from Chicago?
     - Why Chicago? Chicago was one of the “hot-spots” for brewing in early America, thanks to the large population of German immigrants living here.
     - Do we still see a clustering of older breweries closer to Chicago? With enough time (and prohibition) this trend might no longer exist.
     - Results:
![alt text](https://github.com/sponre01/project-one/tree/master/Images/Distance from Chicago vs. Established Year.png "Distance from Chicago vs. Established Year")
     - In the data cleaning process, we got stuck on importing data with locations because it was not the default api set up. Jonathan figured out out to access the data with ingredients included, so I used that logic to access the data with locations. 

3. How does the alcohol content of a beer coorelate to styles? 
     - The average alcohol content over all beers is 6.92% by volume. Our data set includes: 1109 individual beers Note: the average abv for beer according to Google is 4.5%. 
     - For this data set, I combined the beer data and the style data and overlayed the two-tailed t-test statistical logic. 
     - (See: Alcohol by Volume Distribution for All Beers.png)
     - In the web application created below highlights the above finding in a user-friendly format. 
     - (See: http://beer-styles.us-east-2.elasticbeanstalk.com/) 

4. Ingredients: 
   A. Which breweries report ingredients data base most completely with ingredients data?
   B. SOMETHING WITH HOPS
     JONATHAN
