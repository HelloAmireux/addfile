# from PyPDF2 import PdfReader, PdfWriter
#
# # 输入和输出文件的路径
# input_pdf_path = '软件赛-Python程序设计大学B组总决赛获奖名单.pdf'
# output_pdf_path = '蓝桥杯.pdf'
#
# # 创建PDF阅读器和写入器对象
# reader = PdfReader(input_pdf_path)
# writer = PdfWriter()
#
# # 循环遍历指定的页面范围，这里是第4到第6页（注意页码从0开始计算）
# # 74 185
# # for i in range(0, 20):  # 因为页码从0开始，所以第4页是索引3，第6页是索引5
# #     writer.add_page(reader.pages[i])
# writer.add_page(reader.pages[0])
# writer.add_page(reader.pages[10])
# writer.add_page(reader.pages[31])
#
# # 将选定的页面写入到新的PDF文件中
# with open(output_pdf_path, 'wb') as output_pdf:
#     writer.write(output_pdf)
#
# print("PDF pages extracted successfully.")
#


import os
from PyPDF2 import PdfMerger
from PIL import Image


def merge_pdfs_and_images(folder_path, output_path):
    merger = PdfMerger()

    # List all files in the folder
    files = sorted(os.listdir(folder_path))

    temp_pdf_files = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        if file.lower().endswith('.pdf'):
            # If the file is a PDF, append it to the merger
            merger.append(file_path)
        elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # If the file is an image, convert it to a PDF and append it
            image = Image.open(file_path)
            image = image.convert('RGB')

            # Determine page orientation
            if image.width > image.height:
                page_size = (842, 595)  # Landscape A4
            else:
                page_size = (595, 842)  # Portrait A4

            # Resize the image to fit the page size while maintaining aspect ratio
            image_ratio = image.width / image.height
            page_ratio = page_size[0] / page_size[1]

            if image_ratio > page_ratio:
                new_width = page_size[0]
                new_height = int(new_width / image_ratio)
            else:
                new_height = page_size[1]
                new_width = int(new_height * image_ratio)

            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
            background = Image.new('RGB', page_size, (255, 255, 255))
            offset = ((page_size[0] - new_width) // 2, (page_size[1] - new_height) // 2)
            background.paste(resized_image, offset)

            pdf_path = file_path.rsplit('.', 1)[0] + '.pdf'
            background.save(pdf_path)
            temp_pdf_files.append(pdf_path)
            merger.append(pdf_path)
            image.close()  # Close the image file

    # Write out the merged PDF
    with open(output_path, 'wb') as output_pdf:
        merger.write(output_pdf)

    merger.close()

    # Remove the intermediate PDF files
    for pdf_path in temp_pdf_files:
        os.remove(pdf_path)


# Example usage
folder_path = ''  # 修改为实际文件夹路径
output_path = ''  # 修改为实际输出文件路径
merge_pdfs_and_images(folder_path, output_path)


