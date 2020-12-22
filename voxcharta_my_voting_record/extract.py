import re
from bs4 import BeautifulSoup


def import_data(filename):
    """
    Purpose: Import data

    :param filename: str. Full path to MHTML

    :return content:
    """

    with open(filename, 'r') as f:
        content = f.read()
    f.close()

    return content


def soup_it(content):

    page_content = BeautifulSoup(content, "html.parser")

    return page_content


def get_records(page_content):
    records = page_content.find_all('span', {'id': re.compile('votecount*')})
    n_records = len(records)
    print(f"Number of records: {n_records}")

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
        print(f"title : {ii} {title}")

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

            urls = arxiv.find_all('a')
            abs_url = urls[0]['href']
            pdf_url = urls[1]['href']
            ps_url = urls[2]['href']
            ads_url = urls[3]['href']
            papers_url = urls[4]['href']
            others_url = urls[5]['href']
        else:
            arxiv_id = f"no_id_{ii}"

        records_dict[arxiv_id] = {
            'link': link,
            'title': title,
            'authors': authors,
            'affil': affil
        }

        # This handles discussion cases
        if n_para > 3:
            records_dict[arxiv_id].update({
                'abs_url': abs_url,
                'pdf_url': pdf_url,
                'ps_url': ps_url,
                'ads_url': ads_url,
                'papers_url': papers_url,
                'others_url': others_url,
                'comments': comments
            })

    return records_dict
