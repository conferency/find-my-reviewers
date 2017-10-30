from bs4 import BeautifulSoup
import requests

request_headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-charset': 'utf-8',
    'accept-language': 'en',
    'accept-encoding': 'gzip, deflate, br'
}


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=request_headers)
    status_code = response.status_code
    if status_code != 200:
        raise RuntimeError('Status code of response for url {} is {}'.format(url, status_code))
    return response.text


def toint(s):
    if not s:
        return 0
    return int(s)


def crawl(url: str) -> dict:
    soup = BeautifulSoup(fetch_page(url), 'html5lib')

    full_name = soup.find('div', id='gsc_prf_in').text

    brief_info_divs = soup.find_all('div', class_='gsc_prf_il')
    occupation = brief_info_divs[0].text
    email_suffix = brief_info_divs[1].text.split(' ')[-1]
    labels = {a.text: a['href'] for a in brief_info_divs[2].contents}

    # Overall citations
    # Format: [All, Last 5 years, h-index all, h-index last 5 years, i10-index all, i10-index last 5 years]
    overall_citations_list = [int(x.text) for x in soup.find_all('td', class_='gsc_rsb_std')]

    # Citations by year
    citations_popup_body = soup.find('div', id='gsc_md_hist-bdy')
    citations_target_div = citations_popup_body.find('div', class_='gsc_md_hist_b')
    if not citations_target_div:  # No details, retrieve data outside popup instead
        citations_target_div = soup.find('div', class_='gsc_md_hist_b')
    years_list = [int(x.text) for x in citations_target_div.find_all('span', class_='gsc_g_t')]
    citations_list = [int(x.text) for x in citations_target_div.find_all('span', class_='gsc_g_al')]
    citations_by_year = dict(zip(years_list, citations_list))

    # Papers
    papers = []
    papers_body = soup.find('tbody', id='gsc_a_b')
    for paper_item in papers_body.contents:
        paper_item_contents = paper_item.contents

        paper_title_a = paper_item_contents[0].a
        paper_title = paper_title_a.text
        paper_data_url = paper_title_a.attrs['data-href']

        paper_citations = toint(paper_item_contents[1].a.text)

        paper_year = toint(paper_item_contents[2].span.text)

        papers.append({
            'title': paper_title,
            'data_url': paper_data_url,
            'citations': paper_citations,
            'year': paper_year
        })

    ret = {
        'full_name': full_name,
        'occupation': occupation,
        'email_suffix': email_suffix,
        'labels': labels,
        'overall_citations_list': overall_citations_list,
        'citations_by_year': citations_by_year,
        'papers': papers
    }
    return ret
