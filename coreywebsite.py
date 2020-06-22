from bs4 import BeautifulSoup
import requests
import re
import csv

csv_file = open('cms_scrape.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline','summary','video_link'])

page=-1
while(1):
    page=page+1
    concat=str(page)
    source = requests.get('http://coreyms.com/page/'+concat).text
    soup = BeautifulSoup(source,'html5lib')
    


    error404=soup.find('h1',class_='entry-title')
    if(error404==None):
        error404="Page is found"
    else:
        error404=error404.text
    if (error404=='Not found, error 404') :
        print("page not found")
        break
    else:
        
        for article in soup.find_all('article'):
            heading=article.header.h2.a.text
            print(heading)
            print()
            description = article.div.p.text
            print(description)
            print()
            try:
                youtube_link = article.find('iframe', class_='youtube-player')['src']
                pattern = re.compile(r'https://www.youtube.com/embed/[a-zA-Z0-9_.+-]+')
                link=pattern.findall(youtube_link)
                link=link[0]
                video_id=link.split('/')
                video_id=video_id[4]
                video_link = f"https://youtube.com/watch?v={video_id}"
                print(video_link)

                

            except AttributeError:
                print("no link available for this article")
            
            except TypeError:
                print("no link available for this article")
            print()
            print()

            csv_writer.writerow([heading,description,video_link])
        

csv_file.close()
