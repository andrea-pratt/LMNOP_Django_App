import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import os
import django
import sys
import requests 

# include this file location on the path 
sys.path.append(os.getcwd())   
# explain where the settings are - these include where the db is 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lmnop_project.settings')
django.setup() 

from lmn.models import Venue, Show, Artist

# web scraping returns unuseful month data, dictionary changes it to MM format
month_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}


def scrape_first():
    """This function uses requests and beautifulsoup to get data from https://first-avenue.com/shows/, 
    The function iterates over the last 30 pages, identifies the html container with the info we want,
    and gets artist name, venue name, show date

    :param container_object: Constructed with beautifulsoup library from provided url
    :type container_object: Obj
    ...
    :raises django.db.utils.IntegrityError:


    """

    for page_number in range(30): # Loop over the first 30 pages on the first avenue website

        url = f'https://first-avenue.com/shows/page/{page_number}/?orderby=past_shows'

        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
        except Exception as e:
            print(e)
        
    # selecting elements with <div class="d-flex flex-column h-100 flex-fill">
        container_object = soup.find_all(class_="h-100")

    # finds children to pull out date information, artist name, and venue name
        for html_item in container_object:  
            day_bs4_result_set = html_item.select('.day') # checks if this is an appropriate entry, otherwise we capture bad data
            if day_bs4_result_set:  
                try:
                    band_name_bs4_result_set = html_item.select('a') # this item should be the band's name
                    band_name = str(band_name_bs4_result_set[0].text).strip()        

                    """Creates a new Artist instance
                    :param band_name: name of band
                    :type band_name: str
                    """
                    a = Artist(name=band_name)
                    a.save()
                    print(f'created new artist named {a.name}')
                except django.db.utils.IntegrityError as e:
                    print('Duplicate Artist entry, not added.')
                    break
                except Exception as e:
                    print(e)
                
                try:
                    venue_name_bs4_result_set = html_item.select('.venue_name')
                    venue_name = str(venue_name_bs4_result_set[0].text).strip()
                    """Creates a new Venue instance

                       :param name: name of music venue
                       :type name: str

                       :param city: city inwhich venue is located
                       :type city: str

                       :param state: state inwhich venue is located
                       :type state: str
                    """
                    v = Venue(name=venue_name, city='Minneapolis', state='MN')
                    v.save()
                    print(f'created new venue named {v.name}')
                except django.db.utils.IntegrityError as e:
                    print('Duplicate Venue entry, not added.')
                except Exception as e:
                    print(e)    
                
                try:
                    day_bs4_result_set = html_item.select('.day')
                    if day_bs4_result_set:
                        day = str(day_bs4_result_set[0].text).strip() # results are beautifulsoup4 objects
                        if len(day) == 1: # check to see if day is in range 1-9, needs '0' added before if so
                            day = '0' + day

                        month_bs4_result_set = html_item.select('.month')
                        month_char_format = str(month_bs4_result_set[0].text).strip()
                        month = month_dict[month_char_format]
                        year_bs4_result_set = html_item.select('.year')
                        year = str(year_bs4_result_set[0].text).strip()
                        event_date = year + '-' + month + '-' + day
                        date_time = date.fromisoformat(event_date)
                                             
                        """Created new show instance
                            :param show_date: date show was performed
                            :type show_date: datetime

                            :param artist_id: fk for artist table
                            :type artist_id: int
                            
                            :param venue_id: fk for venue table
                            :type venue_id: int
                        """
                        s = Show(show_date=date_time, artist=Artist.objects.filter(name__icontains=band_name)[0], venue=Venue.objects.filter(name__icontains=venue_name)[0])
                        s.save()
                        print(f'created new show on {date_time}')
                except django.db.utils.IntegrityError as e:
                    print('Duplicate Show entry, not added.')
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    scrape_first()
