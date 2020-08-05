import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=5&ti=34&pt=1&ch=3&sch=O&rl=Y"
base_url = "https://texreg.sos.state.tx.us/public/"

def get_first_page(url):
    return requests.get(url)

def get_first_page_tags(url):
    return bs(get_first_page(url).text, "html.parser")

def get_table_regs_and_type(url):
    regs_table = pd.read_html(get_first_page(url).text)[1]
    regs_table.columns = ["regulation", "service_type"]
    return regs_table

def get_list_of_links(url):
    linklist = list()
    soup = get_first_page_tags(url)
    for row in soup.find_all("table"):
        for cell in row.find_all("tr"):
            for c in cell.find_all("a"):
                link = c["href"]
                if "TacPage?" in link:
                    linklist.append(f"{base_url}{link}")
    return linklist

def regs_table_with_links(url):
    df = get_table_regs_and_type(url)
    df['urls'] = get_list_of_links(url)
    return df

def get_cont(url):
    page = bs(requests.get(url).text, "html.parser")
    contlink = base_url
    cont_list = list()
    [cont_list.append(f"{base_url}{x['href']}") for x in page.find_all('a') if x.text == "Cont'd..."]
    if not cont_list:
        return None
    else:
        return cont_list[0]

def scrape_reg_text(url):
    outdf = pd.read_html(url)[2].iloc[0].values[0]
    return outdf

def get_all_text(url):
    regs_list = list()
    if get_cont(url):
        newlink = get_cont(url)
        contlist = [scrape_reg_text(url)]
        while newlink:
            contlist.append(scrape_reg_text(newlink))
            newlink = get_cont(newlink)
        regs_list.append(contlist)
    else:
        regs_list.append(scrape_reg_text(url))
    out_str = "".join(str(x) for x in regs_list)
    if out_str[0] == "[":
        out_str = out_str[2:-2]
    return out_str.replace("Cont'd...", "")



# reg_url = "https://statutes.capitol.texas.gov/Docs/TX/htm/TX.151.htm"

# statutes = get_first_page_tags(reg_url)
# with open("/Users/stephenhage/Github/texas_sos_statutes/statutes/data/statutes_text.txt", "w+") as statutes_file:
#     statutes_file.write(statutes.text)

df = regs_table_with_links(url)
df['regulation_text'] = df.urls.apply(get_all_text)
df.to_excel("/Users/stephenhage/Github/texas_sos_statutes/statutes/data/tx_sales_tax_regulations.xlsx", sheet_name = "regulations", index = False)