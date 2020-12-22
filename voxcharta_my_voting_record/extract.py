import re
from bs4 import BeautifulSoup
import json
import pandas as pd

from .logger import log_stdout


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

    Methods
    -------
    import_data(filename)
      Import data

    soup_it()
      Construct BeautifulSoup data structure -> page_content

    get_records(page_content)
      Retrieve records -> records_dict

    export_data(records_dict)
      Write JSON and csv files
    """

    def __init__(self, filename, json_outfile, csv_outfile, log=None):

        if log is None:
            log = log_stdout()

        self.log = log
        self.filename = filename
        self.json_outfile = json_outfile
        self.csv_outfile = csv_outfile

        self.content = self.import_data()

    def import_data(self):
        """Import data"""

        self.log.info("Importing data ...")
        self.log.info(f"Reading: {self.filename}")
        with open(self.filename, 'r') as f:
            content = f.read()
        f.close()

        self.log.info("finished ...")
        return content

    def soup_it(self):
        """Construct BeautifulSoup data structure"""

        self.log.info("BeautifulSoup-ing data ...")

        page_content = BeautifulSoup(self.content, "html.parser")

        self.log.info("finished ...")
        return page_content

    def get_records(self, page_content):
        """Retrieve records"""

        self.log.info("Retrieving records ...")

        records = page_content.find_all('span', {'id': re.compile('votecount*')})
        n_records = len(records)
        self.log.info(f"Number of records: {n_records}")

        # Note this is larger than [records] because of extra h3 heading at footer
        h3 = page_content.find_all('h3')

        postinfometa = page_content.find_all('span', {'class': 'postinfometa'})
        postinfocats = page_content.find_all('span', {'class': 'postinfocats'})
        abstract = page_content.find_all('div', {'class': 'post-content clearfix'})

        # Get VoxCharta links, titles
        records_dict = dict()

        for ii in range(len(records)):
            link = h3[ii].find('a')['href']
            title = h3[ii].find('a').text
            self.log.info(f"{ii} : {title}")

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

        self.log.info("finished ...")
        return records_dict

    def export_data(self, records_dict):
        """Write JSON and csv files"""

        self.log.info("Exporting data files ...")

        self.log.info(f"Writing: {self.json_outfile}")
        with open(self.json_outfile, 'w') as outfile:
            json.dump(records_dict, outfile)

        df = pd.DataFrame.from_dict(records_dict, orient='index')
        self.log.info(f"Writing: {self.csv_outfile}")
        df.to_csv(self.csv_outfile)

        self.log.info("finished ...")
