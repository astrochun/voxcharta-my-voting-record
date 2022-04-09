import re
from bs4 import BeautifulSoup
import json

import pandas as pd
from rich.progress import open as r_open, track

from .logger import log_stdout


class Extract:
    """
    Purpose:
      Extract metadata from VoxCharta My Voting Records HTML and
      write JSON and CSV files:

    :param filename: str. Full path to MHTML
    :param out_prefix: Full path and prefix of output JSON/CSV files
    :param log: LogClass or logging object. Default uses log_stdout()

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

    def __init__(self, filename, out_prefix, log=None):

        if log is None:
            log = log_stdout()

        self.log = log
        self.filename = filename
        self.json_outfile = f"{out_prefix}.json"
        self.csv_outfile = f"{out_prefix}.csv"

        self.log.info("[italic yellow]Initializing ...")
        self.content = self.import_data()

        self.log.info(
            "[bold dark_green]:heavy_check_mark: Initialization complete!"
        )

    def import_data(self):
        """Import data"""

        self.log.debug(f"Importing data from {self.filename} ...")
        description = f"[italic yellow]Importing data ({self.filename}) ..."
        with r_open(self.filename, mode="rt", description=description) as f:
            content = f.read()

        self.log.debug("[bold dark_green]:heavy_check_mark: Finished!")
        return content

    def soup_it(self):
        """Construct BeautifulSoup data structure"""

        self.log.info("[italic yellow]BeautifulSoup-ing data ...")
        self.log.info("[bold]NOTE[/bold]: This can take up to a few minutes.")
        self.log.info("Please be patient.")
        page_content = BeautifulSoup(self.content, "html.parser")

        self.log.info("[bold dark_green]:heavy_check_mark: Finished!")
        return page_content

    def get_records(self, page_content):
        """Retrieve records"""

        records = page_content.find_all(
            "span", {"id": re.compile("votecount*")}
        )
        n_records = len(records)
        self.log.info(f"[italic yellow]Retrieving {n_records} records ...")

        # Note: larger than [records] because of extra h3 heading at footer
        h3 = page_content.find_all("h3")

        postinfometa = page_content.find_all("span", {"class": "postinfometa"})
        postinfocats = page_content.find_all("span", {"class": "postinfocats"})
        abstract = page_content.find_all(
            "div", {"class": "post-content clearfix"}
        )

        # Get VoxCharta links, titles
        records_dict = dict()

        for ii in track(range(n_records), description="Processing"):
            link = h3[ii].find("a")["href"]
            title = h3[ii].find("a").text
            self.log.debug(f"{ii + 1:04d}: {title}")

            para = postinfometa[ii].find_all("p")
            n_para = len(para)
            authors = para[0].text
            try:
                affil = (
                    postinfometa[ii].find_next("p", {"class": "metafoot"}).text
                )
            except AttributeError:
                affil = ""  # No affiliation

            arxiv_id = ""
            categories = ""
            abs_url = ""
            pdf_url = ""
            ps_url = ""
            ads_url = ""
            papers_url = ""
            others_url = ""
            comments = ""

            # This handles discussion cases
            if n_para > 3:
                # This handles footnote for "Listed affiliation ..."
                if "Listed affiliation" in para[2].text:
                    arxiv = para[4]
                    comments = para[5].text
                else:
                    arxiv = para[3]
                    comments = para[4].text
                arxiv_id = arxiv.find("a").text

                # get instruments
                postinfocats[ii].text.split("\n")
                categories_list = [
                    val.replace(" ", "")
                    for val in postinfocats[2].text.split("\n")
                    if val
                ]
                categories = ";".join(categories_list)
                urls = arxiv.find_all("a")
                abs_url = urls[0]["href"]
                pdf_url = urls[1]["href"]
                ps_url = urls[2]["href"]
                ads_url = urls[3]["href"]
                papers_url = urls[4]["href"]
                others_url = urls[5]["href"]

            records_dict[ii] = {
                "arxiv_id": arxiv_id,
                "link": link,
                "title": title,
                "authors": authors,
                "affil": affil,
                "abstract": abstract[ii].text.replace("\n", ""),
                "categories": categories,
                "abs_url": abs_url,
                "pdf_url": pdf_url,
                "ps_url": ps_url,
                "ads_url": ads_url,
                "papers_url": papers_url,
                "others_url": others_url,
                "comments": comments,
            }

        self.log.info("[bold dark_green]:heavy_check_mark: Finished!")
        return records_dict

    def export_data(self, records_dict):
        """Write JSON and csv files"""

        self.log.info("[italic yellow]Exporting data files ...")

        self.log.info(f"[italic yellow]Writing: {self.json_outfile} ...")
        with open(self.json_outfile, "w") as outfile:
            json.dump(records_dict, outfile, indent=4)

        df = pd.DataFrame.from_dict(records_dict, orient="index")
        self.log.info(f"[italic yellow]Writing: {self.csv_outfile} ...")
        df.to_csv(self.csv_outfile, index=False)

        # Write arxiv_id list
        arxiv_outfile = self.csv_outfile.replace(".csv", "_arxiv.txt")
        self.log.info(f"[italic yellow]Writing: {arxiv_outfile} ...")
        clean_df = df.loc[(df["arxiv_id"] != "") & (df["arxiv_id"].notna())]
        clean_df.to_csv(
            arxiv_outfile, index=False, header=False, columns=["arxiv_id"]
        )

        self.log.info("[bold dark_green]:heavy_check_mark: Finished!")
