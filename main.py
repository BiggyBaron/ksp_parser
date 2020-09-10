from requests_html import HTMLSession
from pprint import pprint
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

session = HTMLSession()

megagroups = []

def list_of_megagroups():
    r = session.get('https://kaspi.kz/shop/c/categories/')
    r.html.render()
    first_level = str(r.html.find('.tree__items')[0].html)
    soup = BeautifulSoup(''.join(first_level), features="lxml")
    # print(soup.prettify())
    body = soup.contents[0].contents[0].contents[0]
    # print(body.prettify())



    # First level
    first_level = []
    for lvl1 in range(len(body.contents)):
        l1 = body.contents[lvl1]
        link = str(l1).split('href="')[1].split('"')[0]
        name = str(l1).split('/">')[1].split('</a>')[0]
        first_level.append({"name": name, "link": link, "sons": []})
        second_level = []
        third_level = []
        fourth_level = []

        for lvl11 in range(len(body.contents[lvl1].contents)):
            if body.contents[lvl1].contents[lvl11].string == None:
                for lvl2 in range(len(body.contents[lvl1].contents[lvl11].contents)):
                    l2 = body.contents[lvl1].contents[lvl11].contents[lvl2]
                    if str(l2).startswith("<li"):
                        link2 = str(l2).split('href="')[1].split('"')[0]
                        name2 = str(l2).split('/">')[1].split('</a>')[0]
                        for lvl21 in range(len(l2.contents)):
                            if l2.contents[lvl21].string == None:
                                for lvl3 in range(len(l2.contents[lvl21].contents)):
                                    l3 = l2.contents[lvl21].contents[lvl3]
                                    if (str(l3).startswith("<li")):
                                        link3 = str(l3).split('href="')[1].split('"')[0]
                                        name3 = str(l3).split('/">')[1].split('</a>')[0]
                                        for lvl31 in range(len(l3.contents)):
                                            if l3.contents[lvl31].string == None:
                                                for lvl4 in range(len(l3.contents[lvl31].contents)):
                                                    l4 = l3.contents[lvl31].contents[lvl4]
                                                    if (str(l4).startswith("<li")):
                                                        link4 = str(l4).split('href="')[1].split('"')[0]
                                                        name4 = str(l4).split('/">')[1].split('</a>')[0]
                                                        fourth_level.append({"name": name4, "link": link4})
                                        third_level.append({"name": name3, "link": link3, "sons": fourth_level})
                        second_level.append({"name": name2, "link": link2, "sons": third_level})
                first_level[lvl1]["sons"] = second_level
    return first_level


def analyze_product(url):
    r = session.get(url)
    r.html.render()

    name = str(r.html.find('.item__heading')[0].text)
    price = str(r.html.find('.item__price-once')[0].text)
    group = str(r.html.find('.breadcrumbs__item')[-1].text)
    characteristics = []

    all_c = r.html.find('.specifications-list__el')
    for el in all_c:
        father = el.find('.specifications-list__header')[0].text
        sons = []
        for son in el.find('.specifications-list__spec'):
            name = son.find('.specifications-list__spec-term-text')[0].text
            value = son.find('.specifications-list__spec-definition')[0].text
            sons.append({"name": name, "value": value})
        characteristics.append({"type": father, "characteristics": sons})
    
    return {"name": name, "price": price, "url": url, "group": group, "characteristics": characteristics}


def get_all_products():

    all_pros = []

    for i in tqdm(range(5000)):
        try:
            url = "https://kaspi.kz/shop/c/categories/?sort=rating&page=" + str(i+1)
            r = session.get(url)
            # r.html.render()
            products = r.html.find(".item-card__name-link")
            print(products)
            for el in products:
                name = el.text
                link = list(el.absolute_links)[0]
                all_pros.append([name, link])
            
            with open('products.json', 'a', encoding='utf-8') as f:
                json.dump(all_pros, f, ensure_ascii=False)
        except:
            pass


if __name__=="__main__":
    # pprint(analyze_product("https://kaspi.kz/shop/p/panasonic-eh-nd64-p865-rozovyi-100495935/"))

    get_all_products()


