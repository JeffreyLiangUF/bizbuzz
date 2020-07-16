from urllib.request import urlopen
from django.core.management.base import BaseCommand
from bizzbuzz.models import News
from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):
    def _delete_everything(self):   #clear out all news in DB, just in case
        News.objects.all().delete()

    def _forbes(self):
        req = requests.get('https://www.forbes.com/business')
        soup = BeautifulSoup(req.content, features='html.parser')

        # replaces punctuation with space so companies can be parsed
        punctuations = '''!()-[]{};:\'\"\\”“’’‘‘,<>./?@#$%^&*_~'''
        translator = str.maketrans(punctuations, ' ' * len(punctuations))

        company_master_list = ['AMAZON', 'SAMSUNG', 'IBM', 'TWITTER', 'NETFLIX',
                               'ORACLE', 'SAP', 'SALESFORCE', 'TESLA', 'SPACEX',
                               'MICROSOFT', 'APPLE', 'GOOGLE', 'FACEBOOK']

        # finds each article
        articles = soup.findAll('h2')

        for article in articles:
            if article.a is not None:
                url = (article.a['href'])
                req = requests.get(url)
                soup = BeautifulSoup(req.content, features='html.parser')
                first_para = soup.find('div', class_="article-body-container")
                if first_para is None:
                    continue
                sum = first_para.find('p').text
                title = soup.find('title').text
                new_title = title.translate(translator)
                company_check = set(company_master_list).intersection(new_title.upper().split(' '))
                if company_check:
                    article = News(title=title, url=url, summary=sum, company=company_check)
                    article.save()

    def _BI(self):
        # In order: Tech, Finance, Strategy, Retail, Executive, Prime, Intelligence, Politics, Transportation, Markets,
        # Science, News, Media, Enterprise
        BIurls = ["https://www.businessinsider.com/sai", "https://www.businessinsider.com/clusterstock",
                  "https://www.businessinsider.com/warroom", "https://www.businessinsider.com/retail",
                  "https://www.businessinsider.com/thelife", "https://www.businessinsider.com/prime",
                  "https://www.businessinsider.com/research", "https://www.businessinsider.com/politics",
                  "https://www.businessinsider.com/transportation", "https://www.businessinsider.com/moneygame",
                  "https://www.businessinsider.com/science", "https://www.businessinsider.com/news",
                  "https://www.businessinsider.com/media", "https://www.businessinsider.com/enterprise"]

        punctuations = '''!()-[]{};:\'\"\\”“’’‘‘,<>./?@#$%^&*_~'''
        translator = str.maketrans(punctuations, ' ' * len(punctuations))

        company_master_list = ['AMAZON', 'SAMSUNG', 'IBM', 'TWITTER', 'NETFLIX',
                               'ORACLE', 'SAP', 'SALESFORCE', 'TESLA', 'SPACEX',
                               'MICROSOFT', 'APPLE', 'GOOGLE', 'FACEBOOK']

        urls = []

        for scrape in BIurls:
            req = requests.get(scrape)
            soup = BeautifulSoup(req.content, 'lxml')

            for div in soup.find_all("div", class_="top-vertical-trio-item"):
                a_tag = div.find("a", class_="tout-title-link")
                title = a_tag.text
                if a_tag.attrs["href"][0] == "/":
                    url = "https://businessinsider.com" + a_tag.attrs["href"]
                else:
                    url = a_tag.attrs["href"]
                if url in urls:
                    continue
                sum = div.find("div", class_="tout-copy three-column body-regular").text.strip()
                new_title = title.translate(translator)
                company_check = set(company_master_list).intersection(new_title.upper().split(' '))
                if company_check:
                    urls.append(url)
                    article = News(title=title, url=url, summary=sum, company=company_check)
                    article.save()

    def _NYT(self):
        NYTurls = ["https://www.nytimes.com/section/technology", "https://www.nytimes.com/section/business",
                   "https://www.nytimes.com/section/business/economy",
                   "https://www.nytimes.com/section/business/energy-environment",
                   "https://www.nytimes.com/section/science", "https://www.nytimes.com/section/science/space"]

        # replaces punctuation with space so companies can be parsed
        punctuations = '''!()-[]{};:\'\"\\”“’’‘‘,<>./?@#$%^&*_~'''
        translator = str.maketrans(punctuations, ' ' * len(punctuations))

        company_master_list = ['AMAZON', 'SAMSUNG', 'IBM', 'TWITTER', 'NETFLIX',
                               'ORACLE', 'SAP', 'SALESFORCE', 'TESLA', 'SPACEX',
                               'MICROSOFT', 'APPLE', 'GOOGLE', 'FACEBOOK']

        urls = []

        for scrape in NYTurls:
            req = requests.get(scrape)
            soup = BeautifulSoup(req.content, 'lxml')

            for div in soup.find_all("li", class_="css-ye6x8s"):
                a_tag = div.find("a")
                title = a_tag.find("h2").text
                if a_tag.attrs["href"][0] == "/":
                    url = "https://nytimes.com" + a_tag.attrs["href"]
                else:
                    url = a_tag.attrs["href"]
                if url in urls:
                    continue
                sum = a_tag.find("p")
                if not sum:
                    continue
                sum = sum.text
                new_title = title.translate(translator)
                company_check = set(company_master_list).intersection(new_title.upper().split(' '))
                if company_check:
                    urls.append(url)
                    article = News(title=title, url=url, summary=sum, company=company_check)
                    article.save()

    def _TT(self):
        # Tech, Science, Business, Features
        TTurls = ["https://www.techtimes.com/personaltech", "https://www.techtimes.com/science",
                  "https://www.techtimes.com/biztech", "https://www.techtimes.com/feature"]

        # replaces punctuation with space so companies can be parsed
        punctuations = '''!()-[]{};:\'\"\\”“’’‘‘,<>./?@#$%^&*_~'''
        translator = str.maketrans(punctuations, ' ' * len(punctuations))

        company_master_list = ['AMAZON', 'SAMSUNG', 'IBM', 'TWITTER', 'NETFLIX',
                               'ORACLE', 'SAP', 'SALESFORCE', 'TESLA', 'SPACEX',
                               'MICROSOFT', 'APPLE', 'GOOGLE', 'FACEBOOK']
        for scrape in TTurls:
            req = requests.get(scrape)
            soup = BeautifulSoup(req.content, 'lxml')

            for div in soup.find_all("div", class_="list2"):
                a_tag = div.find("h2").find("a")
                url = a_tag.attrs["href"]
                title = a_tag.text
                p_tag = div.find("p", class_="summary")
                sum = p_tag.text
                new_title = title.translate(translator)
                company_check = set(company_master_list).intersection(new_title.upper().split(' '))
                if company_check:
                    article = News(title=title, url=url, summary=sum, company=company_check)
                    article.save()

    def handle(self, *args, **options):
        self._delete_everything()
        self._forbes()
        self._BI()
        self._NYT()
        self._TT()