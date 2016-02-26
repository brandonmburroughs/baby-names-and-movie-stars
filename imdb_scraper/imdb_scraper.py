import requests
from bs4 import BeautifulSoup


def get_full_link(relative_link):
    """
    Returns the fully qualified IMDB link when given the partial link

    Parameters
    ----------
    relative_link : str
        The link relative to imdb.com

    Returns
    -------
    full_link : str
        The full qualified IMDB link
    """

    full_link = 'http://www.imdb.com' + relative_link

    return full_link


def get_actor_page(actor_name):
    """
    Get an actor's IMDB page link

    Parameters
    ----------
    actor_name : str
        The name of the actor

    Returns
    -------
    actor_link : str
        The relative link to an actor's IMDB page
    """
    
    # Construct URL
    imdb_search = "http://www.imdb.com/find?q=%s&s=nm" % actor_name

    # Get page
    r = requests.get(imdb_search)

    # Soup HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get list of results
    search_results = soup.find('td', attrs={'class': 'result_text'})

    # Get links from first result (most likely to be the match)
    actor_link = search_results.find('a').get('href')

    return actor_link


def get_actor_gender(actor_name):
    # Get actor page
    actor_page = get_actor_page(actor_name)

    # Construct the biopage
    bio_page = get_full_link(actor_page.split('?')[0] + 'bio')

    # Get page
    r = requests.get(bio_page)

    # Soup HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get list of results
    search_results = soup.find('div', attrs={'class': 'soda odd'})

    # Separate bio paragraph
    bio = search_results.text.lower()

    # Male count
    male_count = bio.count(' he ') + bio.count(' him ') + bio.count(' his ')

    # Female count
    female_count = bio.count(' she') + bio.count(' her ')

    # Determine gender
    if male_count >= female_count:
        gender = 'M'
    else: 
        gender = 'F'

    return gender


def get_actor_known_for_links(imdb_page):
    """
    Get an actor's "Known For" links from their IMDB page

    Parameters
    ----------
    imdb_page : str
        The full path IMDB page to search

    Returns
    -------
    known_for_movies : list of dicts
        The list of "Known For" movies and attributes

    Note:  These links are relative to IMDB, i.e. do not contain 
        "http://www.imdb.com/".
    """
    # Get page
    r = requests.get(imdb_page)

    # Soup HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find "Known For" section
    knownfor = soup.find('div', attrs={'id': 'knownfor'})

    # Find all the links in the "Known For" section
    all_a = knownfor.findAll('a')

    # Get the titles and links
    known_for_movies = []
    for link in all_a:
        # Check for the appropriate link
        if link.has_attr('href') and link.text != ' \n':

            # Split the text to get the title and year
            title, year = link.text.split('(')

            # Clean up the title and year
            title = title.encode('ascii','ignore').strip()
            year = int(year[0:4])

            # Put this all in a dictionary
            movie_dict = {
                'link': get_full_link(link.get('href')),
                'title': title,
                'year': year
            }

            # Append the dictionary to the list
            known_for_movies.append(movie_dict)

    return known_for_movies


def get_actor_popular_movies(actor_name):
    """
    This is a wrapper function for getting an actor's page and then getting
    their popular movies.

    Parameters
    ----------
    actor_name : str
        The actor's name

    Returns
    -------
    popular_movies : list of dicts
        The list of "Known For" movies and attributes

    Note:  These links are relative to IMDB, i.e. do not contain 
        "http://www.imdb.com/".
    """
    # Get the actor's page
    actor_page = get_actor_page(actor_name)

    # Get the movies he or she is known for
    popular_movies = get_actor_known_for_links(get_full_link(actor_page))

    return popular_movies
    

# Main
if __name__ == '__main__':
    # The actor to search for
    actor_name = 'Leonardo DiCaprio'

    # Get the actor's popular movies
    popular_movies = get_actor_popular_movies(actor_name)

    # Construct string output of movies
    movie_list = [movie['title'] for movie in popular_movies]
    movie_list_output = ', '.join(movie_list[:-1]) + ', and ' + movie_list[-1]

    # Output
    print '%s is known for the movies %s.' % (actor_name, movie_list_output)