import zipfile
import re
import os

pptx_path = 'd:\\AI\\DL07 - AI Project\\DL07_K311_Project_01_GUI\\presentation\\DL07_K311_DoanNhatQuang_PhanNgocMinhQuan.pptx'

if not os.path.exists(pptx_path):
    print("PPTX NOT FOUND")
else:
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_files = [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        # Sort slides properly: slide1.xml, slide2.xml, ..., slide10.xml
        slide_files.sort(key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1)))
        
        with open('extracted_slides.txt', 'w', encoding='utf-8') as out:
            for slide in slide_files:
                xml_content = zf.read(slide).decode('utf-8')
                # Look for all <a:t>...</a:t> elements to extract text
                texts = re.findall(r'<a:t>(.*?)</a:t>', xml_content)
                out.write(f"=== {slide} ===\n")
                out.write(" ".join(texts) + "\n\n")
