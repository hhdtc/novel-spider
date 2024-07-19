import re
from playwright.sync_api import Playwright, sync_playwright, expect
import os
from bili_font_secret import Decrypt
import novel_image


def run(playwright: Playwright,link,bookname,skip = 0,skip_page = 0) -> None:
    os.makedirs(bookname, exist_ok=True)
    decrypt = Decrypt()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(link)
    page.wait_for_timeout(1000)
    l = page.locator("xpath=/html/body/div[2]/div[3]/div[3]/div").all()
    # print(l)
    allhrefs = []
    booktitles = []
    titles = []
    coverlinks = []

    #find chapter and cover
    for i in l:
        title = i.locator("xpath=./div/h2").nth(0)
        if (len(title.all_text_contents()) > 0 ):



            imagelink = i.locator("xpath=./a/img").nth(0)
            imagelink.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            image_url = imagelink.get_attribute("src")
            coverlinks.append(image_url)


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
        if b < skip:
            continue

        directory = str(booktitles[b])
        folder = os.path.join(bookname,directory)
        print(folder)


        os.makedirs(folder, exist_ok=True)
        os.makedirs(os.path.join(folder,'images'), exist_ok=True)
        if not 'no-cover' in coverlinks[b]:
            novel_image.downloader(coverlinks[b],os.path.join(folder,'cover.'+coverlinks[b].split('.')[-1])).download()
            print('downloaded cover',coverlinks[b])


        nextchapterlink = ''
        for i in range(0,len(titles[b])):
            if i < skip_page:
                continue
            href = allhrefs[b][i]
            title = titles[b][i]
            print(href,title)

            if 'javascript' in href:
                href = nextchapterlink
            page.goto("https://www.linovelib.com"+href)
            page.wait_for_timeout(500)


            # page.wait_for_timeout(1500)
            # title = page.locator("xpath=/html/body/div[2]/div[3]/div/h1").all()
            # print(title)
            string = ''
            pages = 0
            # directory = str(booktitles[b])
            # folder = os.path.join(bookname,directory)
            # print(folder)


            # os.makedirs(folder, exist_ok=True)
            # os.makedirs(os.path.join(folder,'images'), exist_ok=True)
            while(True):
                
                image_elements = page.locator("xpath=/html/body/div[2]/div[3]/div/img").all()
                print(len(image_elements))
                for image in image_elements:
                    image.scroll_into_view_if_needed()
                    print(image.evaluate('el => el.outerHTML'))
                    page.wait_for_timeout(1000)


                pages += 1
                content = page.locator("xpath=/html/body/div[2]/div[3]/div").nth(0)
                content = content.locator("xpath=./p|./img").all()

                flag = False
                if page.locator('text="下一页"').is_visible():
                    flag = True
                if page.locator('text="下一章"').is_visible():
                    nextchapterlink = page.locator('text="下一章"').get_attribute('href')
                leng = len(content)
                
                for index,c in enumerate(content):
                    tagName = c.evaluate('el => el.tagName.toLowerCase()')
                    if tagName == 'img':
                        # Use Playwright to download the image
                        image_url = c.get_attribute("src")
                        print(image_url)
                        save_path =  os.path.join(folder,'images',image_url.split('/')[-1])
                        novel_image.downloader(image_url,save_path).download()
                        
                        print("Image downloaded successfully.")

                        raw_html = c.evaluate('el => el.outerHTML')
                        print(raw_html)
                        string += raw_html
                        string += '\n'
                        continue
                    elif tagName == 'p':
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

            file_path = os.path.join(bookname,directory, title)
            with open(file_path,'w', encoding="utf-8") as file:
                file.write(string)
            # break
            # page.go_back()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright,'https://www.linovelib.com/novel/3095/catalog','败北女角太多了!',1)
