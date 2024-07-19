import shutil
from ebooklib import epub
import os
import glob
import re
import sys

import imghdr

def create_epub_from_txt(txt_files, output_file,bookdir,image_folder):
    # Create EPUB book
    book = epub.EpubBook()
    nameofbook = os.path.basename(output_file).replace('.epub', '')
    # Set metadata
    book.set_identifier(nameofbook)
    book.set_title(nameofbook)
    book.set_language('cn')
    # book.add_metadata('DC', 'series', bookdir)
    # book.add_metadata('DC', 'series_index', str(seriesindex))
    # book.set_metadata('calibre:series', bookdir)
    # book.set_metadata('calibre:series_index', str(seriesindex))

    # Add author(s)
    book.add_author(' ')
    spine_items = []
    # Iterate through each text file
    for txt_file in txt_files:
        
        if imghdr.what(txt_file):
            # image_item = epub.EpubItem(file_name=os.path.basename(txt_file), media_type='image/jpeg', content=open(txt_file, 'rb').read())
            # book.add_item(image_item)
            book.set_cover(os.path.basename(txt_file), open(txt_file, 'rb').read())
            continue
        print(txt_file)
        # Read text content from file
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Create chapter
        chapter_title = os.path.basename(txt_file).replace('.txt', '')
        chapter = epub.EpubHtml(title=chapter_title, file_name=f'{chapter_title}.xhtml', lang='cn')
        
        content = content.split('\n')
        chapter.content = ''
        for line in content:
            if line [0:4] == '<img':
                pattern = '\d+.jpg'
                print(line)
                match = re.findall(pattern, line)
                if match:
                    # print(match[0])
                    # print(f'<img src="..\\images\\{match[0]}"  class="imagecontent"/>'+'\n')
                    # chapter.content += f'<img src="..\\images\\{match[0]}.jpg"  class="imagecontent"/>'+'\n'
                    
                    image_path = os.path.join(image_folder,match[0])
                    print(image_path)
                    image_item = epub.EpubItem(file_name=os.path.join('images',match[0]), media_type='image/jpeg', content=open(image_path, 'rb').read())
                    book.add_item(image_item)
                    chapter.content += '<img src="images/'+match[0]+'"></img>'
                    print('<img src="images/'+match[0]+'"></img>')
                else:
                    chapter.content += line
            else:
                chapter.content += '<p>'+line+'</p>'        
        # chapter.content = '<p>'+content+'</p>'

        # Add chapter to book
        book.add_item(chapter)
        book.toc.append(chapter)
        spine_items.append(chapter)

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS styles
    style = 'body { font-family: Times, serif; }'

    # Add CSS file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Set spine
    book.spine = ['nav'] + spine_items  # add other chapter files here

    # Create EPUB file
    epub.write_epub(output_file, book, {})

if __name__ == '__main__':
    

    bookdir = ''
    if len(sys.argv) > 1:
        bookdir = sys.argv[1]
    else:
        bookdir = 'temp'
    file_pattern = os.path.join(bookdir, '*')
    books = glob.glob(file_pattern)
    books.sort(key=os.path.getmtime)
    os.makedirs(bookdir+'_epub', exist_ok=True)
    seriesindex= 1




    for i in books:
        output_file = i.replace('\\',' ')
        folder = os.path.join(bookdir+'_epub')
        image_folder = os.path.join(i, 'images')
        # if os.path.exists(image_folder):
        #     destination_folder = os.path.join(folder, 'images')
        #     try:
        #         shutil.copytree(image_folder, destination_folder)
        #     except FileExistsError:
        #         pass


        file_pattern = os.path.join(i, '*')
        txt_files = glob.glob(file_pattern)
        txt_files = [file for file in txt_files if os.path.isfile(file)]

        txt_files.sort(key=os.path.getmtime)
        

        

        os.makedirs(folder, exist_ok=True)

        output_file = 'vol '+('0'*(3-len(str(seriesindex))))+str(seriesindex)+' ' + output_file + '.epub'
        
        output_file = os.path.join(folder,output_file)
        

        # Call the create_epub_from_txt function
        create_epub_from_txt(txt_files, output_file,folder,image_folder)
        seriesindex += 1


    # for i in range(1,6):
    #     file_pattern = os.path.join(str(i), '*')
    #     # Get all txt files in folder 1
    #     txt_files = glob.glob(file_pattern)
    #     # Sort the txt files by modification time

    #     txt_files.sort(key=os.path.getmtime)
    #     # for i in txt_files:
    #     #     print(i)
    #     # Specify the output file path
    #     output_file = 'eva anima #'+str(i)+'.epub'

    #     # Call the create_epub_from_txt function
    #     create_epub_from_txt(txt_files, output_file)
