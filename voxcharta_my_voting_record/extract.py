import re
from bs4 import BeautifulSoup
import json
import pandas as pd


class Extract:
    """
    Purpose:
      Extract metadata from VoxCharta My Voting Records HTML and
      write JSON and CSV files:

    :param filename: str. Full path to MHTML
    :param json_outfile: str for JSON output file
    :param csv_outfile: str for CSV output file

    Attributes
    ----------
    content: str (from import_data)
    page_content: BeautifulSoup4 data structure object (from soup_it)
    records_dict: dict (nested) containing records (from get_records)

    Methods
    -------
    import_data(filename)
      Import data

    soup_it()
      Construct BeautifulSoup data structure

    get_records()
      Retrieve records

    export_data()
      Write JSON and csv files
    """

    def __init__(self, filename, json_outfile, csv_outfile):

        self.filename = filename
        self.json_outfile = json_outfile
        self.csv_outfile = csv_outfile

        self.content = self.import_data()

    def import_data(self):
        """Import data"""

        print("Importing data ...")
        print(f"Reading: {self.filename}")
        with open(self.filename, 'r') as f:
            content = f.read()
        f.close()

        return content

    def soup_it(self):
        """Construct BeautifulSoup data structure"""

        print("BeautifulSoup-ing data ...")

        page_content = BeautifulSoup(self.content, "html.parser")

        return page_content

    def get_records(self):
        """Retrieve records"""

        print("Retrieving records ...")

        records = self.page_content.find_all('span', {'id': re.compile('votecount*')})
        n_records = len(records)
        print(f"Number of records: {n_records}")

        # Note this is larger than [records] because of extra h3 heading at footer
        h3 = self.page_content.find_all('h3')

        postinfometa = self.page_content.find_all('span', {'class': 'postinfometa'})
        postinfocats = self.page_content.find_all('span', {'class': 'postinfocats'})
        abstract = self.page_content.find_all('div', {'class': 'post-content clearfix'})

        # Get VoxCharta links, titles
        records_dict = dict()

        for ii in range(len(records)):
            link = h3[ii].find('a')['href']
            title = h3[ii].find('a').text
            print(f"{ii} : {title}")

            para = postinfometa[ii].find_all('p')
            n_para = len(para)
            authors = para[0].text
            try:
                affil = postinfometa[ii].find_next('p', {'class': 'metafoot'}).text
            except AttributeError:
                affil = ''  # No affiliation

            # This handles discussion cases
            if n_para > 3:
                # This handles footnote for "Listed affiliation ..."
                if 'Listed affiliation' in para[2].text:
                    arxiv = para[4]
                    comments = para[5].text
                else:
                    arxiv = para[3]
                    comments = para[4].text
                arxiv_id = arxiv.find('a').text

                # get instruments
                postinfocats[ii].text.split('\n')
                categories_list = [val.replace(' ', '') for
                                   val in postinfocats[2].text.split('\n') if val]
                categories = ';'.join(categories_list)
                urls = arxiv.find_all('a')
                abs_url = urls[0]['href']
                pdf_url = urls[1]['href']
                ps_url = urls[2]['href']
                ads_url = urls[3]['href']
                papers_url = urls[4]['href']
                others_url = urls[5]['href']
            else:
                arxiv_id = ''

            records_dict[ii] = {
                'arxiv_id': arxiv_id,
                'link': link,
                'title': title,
                'authors': authors,
                'affil': affil,
                'abstract': abstract[ii].text.replace('\n', '')
            }

            # This handles discussion cases
            if n_para > 3:
                records_dict[arxiv_id].update({
                    'categories': categories,
                    'abs_url': abs_url,
                    'pdf_url': pdf_url,
                    'ps_url': ps_url,
                    'ads_url': ads_url,
                    'papers_url': papers_url,
                    'others_url': others_url,
                    'comments': comments
                })

        return records_dict

    def export_data(self):
        """Write JSON and csv files"""

        print("Exporting data files ...")

        print(f"Writing: {self.json_outfile}")
        with open(self.json_outfile, 'w') as outfile:
            json.dump(self.records_dict, outfile)

        df = pd.DataFrame.from_dict(self.records_dict, orient='index')
        print(f"Writing: {self.csv_outfile}")
        df.to_csv(self.csv_outfile)
