<p align="center">

# __NEXUS EZ DELETED MOD FILE FINDER__

## [Download NexusEZFileFinder.exe](https://www.dropbox.com/s/8ls9qeaprws9hpa/NexusEZFileFinder.exe?dl=1)
  
### What is NEZDMFF?

  
NEZDMFF is a tool used to find files from deleted mod pages on Nexus Mods.
  Ever since the Nexus policy change in Jul 2021, files have stayed on the website's server despite their main mod pages being unavailable. For less well-known mods not archived on Google or forums it can be difficult to know where to start searching.
  
### How does it work?
  
NEZDMFF uses a web-scraping algorithm which takes the original mod page number and calculates the average file ID for that mod, by scraping other mod pages and files published in a similar time frame. It then repeatedly increments the file ID number in that URL and connects to it, checking for files in that ID range, and prints all successfully found files to the console.
  This can drastically reduce headaches, and should find files instantly if the date of the file upload corresponds with the date of mod page creation.
  
  
![alt text](https://i.imgur.com/keX6ofh.png)
  
This method isn't always perfect, with deleted mods sometimes having been re-uploaded and maintained years after their initial publication. Because of this I have included a way to disable the auto-search algorithm and manually search for file IDs. It is useful to check other mod page files in the same date range to see what the typical file ID would be for that upload date. On the Nexus mod page you can hover your mouse over 'Manual Download' to __find id?=__ or __&file_id=__ depending on the type of link.
  
You can choose how big your sample data size should be by changing Max Pages to Scrape +/- in the Search Options. If you're not finding the file you want, and you know it was deleted after 1 Jul 2021, then changing the Max Pages to Scrape to either a bigger number or smaller number may help. The recommended size is between 3 - 15 pages.
 </p>
 
![alt text](https://i.imgur.com/lJwBG5X.png)

### What if a newer file was deleted on an older page?

The algorithm is fairly simple and might struggle to find newer files on older pages, so the best way is to try to find any files on different mod pages of the same game that have the same date.
You are looking for the ID number that will appear when you hover over the "Manual Download" button.

![alt text](https://i.imgur.com/cqX7FJZ.png)

### Future Plans

* More options for manual searching, such as estimating deleted mod file IDs based on game name and date uploaded
* Better implemented threading to avoid hanging during initial scraping algorithm
* A more sophisticated algorithm that can filter out obviously bad data if the sample size is too small / too big

### I am still relatively new to Python. If you would like to help improve this code then please get in contact at johnreedy01@gmail.com !
