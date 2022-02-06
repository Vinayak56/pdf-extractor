import os
from pdf2image import convert_from_path
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
import cv2
import json
import pytesseract
import filetype
urls = [
    "https://mpsctopper.com/wp-content/uploads/2022/01/12th-std-Political-Science-Book-in-Marathi.pdf",
    "https://mpsctopper.com/wp-content/uploads/2022/01/12th-std-History-Book-Pdf-in-Marathi.pdf",
    "https://mpsctopper.com/wp-content/uploads/2022/01/12th-std-Economics-Book-Pdf-in-Marathi.pdf",
    "https://mpsctopper.com/wp-content/uploads/2022/01/12th-std-Geography-Book-Pdf-in-Marathi.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/11/12th-Environment-Textbook-in-Marathi-Pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/10th-science-book-in-marathi-pdf-part-1.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/10th-standard-history-book-in-Marathi-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/10th-standard-geography-textbook-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/10th-STD-Marathi-textbook-pdf-1.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/10th-Std-Marathi-Textbook-Aksharbharati-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/10th-standard-maths-book-pdf-in-marathi-part-1.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/1.-Marathi-Yuvakbharti-11th-Marathi-PDF-21.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/4.-Paryavran-Shikshan-Marathi-11th-Standard-21.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/6.-11vi-Arogya-Va-Sharirik-Shikshan-Marathi-21.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/2.-Geography-Book-for-Class-11th-in-Marathi-21.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/1.-Maharashtra-state-board-11th-history-books-pdf-in-Marathi-21.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/3.-Polity-Book-for-Class-11th-in-Marathi-21.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/4.-Economics-Book-for-Class-11th-in-Marathi-21.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/9th-marathi-book-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/9th-std-science-book-in-pdf-marathi-medium.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/History-and-Polity-9th-std-Marathi-Medium.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/9th-std-geography-textbook.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/9th-std-water-security-textbook-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/9th-std-marathi-akshar-bharati.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/09/6.-12vi-Arogya-Va-sharirik-shikshan-Book-PDF-21.pdf",
    "https://archive.org/details/marathi_202111/page/n7/mode/2up?view=theater",
    "https://archive.org/details/e-shaikshanik-sandarbh-issue-133-dec-2021-jan-2022/page/n19/mode/2up",
    "https://mpsctopper.com/wp-content/uploads/2021/06/8th-Std-Marathi-Books-PDF-Marathi-Medium.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/8th-std-Science-textbook-PDF-Marathi-Medium.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/8th-std-History-textbook-pdf-Marathi-Medium.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/06/Class-8-Geography-Textbook-in-Marathi-Medium.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/7th-Std-Marathi-Sugam-bharti-textbook-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/7th-Std-Marathi-Balbharti-textbook-pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/7th-Std-Science-Textbook-Pdf-Marathi-Medium.pdf",
    "https://www.mpscmaterial.com/wp-content/uploads/2021/10/4.-Itihas-ani-Nagri-shashtra-7th-Marathi-2021.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/6th-Std-Marathi-Balbharti-textbook-Pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/6th-Std-Marathi-Sulabhbharati-textbook-Pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/6th-Std-Marathi-Sugambharti-textbook-Pdf.pdf",
    "https://mpsctopper.com/wp-content/uploads/2021/07/6th-Std-History-Textbook-Pdf-Marathi-Medium.pdf",
    "https://archive.org/details/aaapansarebhaumarathinew/page/n5/mode/2up",
    "https://archive.org/details/majhagadhoocormar/mode/2up",
    "https://archive.org/details/bhalemothedhirde/page/n15/mode/2up",
    "https://archive.org/details/FRIDAKAHLOMARATHI/page/n3/mode/2up",
    "https://archive.org/details/PAULM_201906/page/n23/mode/2up",
    "https://archive.org/details/marhriysata07sarduoft/page/n19/mode/2up?view=theater",
    "https://archive.org/details/laxmanteerth-shastri-marathi/page/n11/mode/2up",
    "https://archive.org/details/dli.ministry.31030/13277.8861%2520%2528part-1%2529/page/n3/mode/2up?view=theater",
    "https://archive.org/details/dli.ministry.31029/page/n7/mode/2up?view=theater"
]

output_dir = "./pdfs"
output_img_dir = "./pdfs/images"
os.mkdir(output_dir)
os.mkdir(output_img_dir)

def is_pdf(path_to_file):
    try:
        if(filetype.guess(path_to_file).mime == 'application/pdf'):
            return True
        else:
            return False
    except AttributeError:
        return False

pdf_urls = []
i=1
for url in urls:
    with open(f"./pdfs/book{i}.pdf","wb") as f:
        if url.endswith(".pdf"):
            response = requests.get(url)
            f.write(response.content)
            pdf_urls.append(url)
        else:
            req = Request(url)
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")
            url = soup.find("input", {"class": "js-ia-metadata"}, type="hidden").get("value")
            start_address = re.findall('.*,"workable_servers":\["(.+?)",', url)
            end_address = re.findall(',"dir":"(.+?)",', url)
            filepath = re.findall('"name":"(.+?)",', url)
            new_url = f"https://{start_address[0]}{end_address[0]}/{filepath[0]}"
            pdf_urls.append(new_url)
            response = requests.get(new_url)
            f.write(response.content)
    i +=1

pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract\tesseract.exe"
ll = []
for j in range(1,i+1):
    pdf_file = f"./pdfs/book{j}.pdf"
    if(is_pdf(pdf_file)==False):
        continue
    pages = convert_from_path(pdf_file,poppler_path=r"E:\poppler-0.68.0\bin")
    pages[15].save(f'./pdfs/images/page{j}.png', 'JPEG')
    img = cv2.imread(f"./pdfs/images/page{j}.png")
    text = pytesseract.image_to_string(img,lang="mar")
    lt = len(text)
    ss = ""
    if lt<=70:
        k = 1
        while(True and 10+k<lt):
            os.remove(f'./pdfs/images/page{j}.png')
            pages[10+k].save(f'./pdfs/images/page{j}.png', 'JPEG')
            img = cv2.imread(f"./pdfs/images/page{j}.png")
            text = pytesseract.image_to_string(img, lang="mar")
            lt = len(text)
            if(lt>=70):
                break
            k += 1
    sln = text.find("\n\n")
    ss = text[:sln]
    while text.find("\n\n", sln + 1)!=-1:
        nsln = text.find("\n\n",sln+1)
        if len(text[sln + 1:nsln])>len(ss):
            ss = text[sln+1:nsln]
        sln = nsln+1
    ll.append({"page-url":urls[j-1],"pdf-url":pdf_urls[j-1],"paragraph":ss.replace("\n"," ")})
    with open("pdf_extract.json", "w", encoding="utf8") as final:
        json.dump(ll, final, ensure_ascii=False)

