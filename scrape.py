import parameters
import requests
from bs4 import BeautifulSoup
import io

def run():
    top_links = []

    for page in range(parameters.NUM_OF_PAGES):
        res = requests.get(parameters.WEBPAGE + '?p=' + str(page + 1))
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titlelink')
        subtexts = soup.select('.subtext')
        top_links += (scrapePage(links, subtexts))

    top_links.sort(key=lambda dict: dict['score'], reverse=True)
    recordNewTop(top_links)
    return

def scrapePage(links, subtexts):
    link_list = []

    for index, item in enumerate(links):
        cur_sub = subtexts[index].select('.score')
        if len(cur_sub) == 0:            # if a score doesnt exist, move on
            continue

        cur_score = int(cur_sub[0].text.split(' ')[0])
        if cur_score >= parameters.SCORE_LIMIT:
            cur_title = item.text
            cur_link = item.get('href', None)
            link_list.append({'title': cur_title, 'link': cur_link, 'score': cur_score})
            
    return link_list

def recordNewTop(top_list):
    try:
        with open(parameters.OUTPUT_FILE, 'w') as file:
            file.write('''
These are the top stories from https://news.ycombinator.com/news
    scraped and organized by Leo
        V1.3

''')
            for item in top_list:
                file.write(f"\t< {item['title']} >\nlink:\t{item['link']}\nvotes:\t{item['score']}\n\n")
    except:
        print('something went wrong!')
    
    return


if __name__ == '__main__':
    run()