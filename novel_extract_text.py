import re
from playwright.sync_api import Playwright, sync_playwright, expect
import os
from bili_font_secret import Decrypt

def run(playwright: Playwright) -> None:
    decrypt = Decrypt()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.linovelib.com/novel/2680/catalog")
    
    l = page.locator("xpath=/html/body/div[2]/div[3]/div[3]/div").all()
    # print(l)
    allhrefs = []
    booktitles = []
    titles = []
    for i in l:
        title = i.locator("xpath=./div/h2").nth(0)
        if (len(title.all_text_contents()) > 0 ):
            title = title.all_text_contents()[0]
            # print(title)
            booktitles.append(title)
            hrefselement = i.locator("xpath=./ul/li/a").all()
            hrefs = []
            title = []
            for href in hrefselement:
                hrefs.append(href.get_attribute("href"))
                title.append(href.all_text_contents()[0])
            # print(hrefs)
            allhrefs.append(hrefs)
            titles.append(title)
    # print(booktitles)
    # print(titles)
    # print(allhrefs)

    

    for b in range(0,len(booktitles)):
        for i in range(0,len(titles[b])):
            href = allhrefs[b][i]
            title = titles[b][i]
            print(href,title)

            if 'javascript' in href:
                continue
            page.goto("https://www.linovelib.com"+href)
            page.wait_for_timeout(2000)
            # title = page.locator("xpath=/html/body/div[2]/div[3]/div/h1").all()
            # print(title)
            string = ''
            pages = 0
            while(True):
                pages += 1
                content = page.locator("xpath=/html/body/div[2]/div[3]/div/p").all()
                directory = str(booktitles[b])
                os.makedirs(directory, exist_ok=True)
                flag = False
                if page.locator('text="下一页"').is_visible():
                    flag = True
                leng = len(content)
                
                for index,c in enumerate(content):
                    
                    newline = ''
                    if pages%2 == 0 and index == leng-1:
                        newline = decrypt.decrypt(c.all_text_contents()[0])
                        print(newline)
                    else:
                        newline = c.all_text_contents()[0]
                    # print(newline)
                    string +=newline
                    string +='\n'


                
                if flag:
                    page.locator('text="下一页"').click()
                    page.wait_for_timeout(2000)
                else:
                    break

            file_path = os.path.join(directory, title)
            with open(file_path,'w', encoding="utf-8") as file:
                file.write(string)
            # break
            # page.go_back()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
