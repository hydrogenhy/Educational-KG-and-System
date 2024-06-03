import chardet
import codecs

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        confidence = result['confidence']
        print(f"The detected encoding is {encoding} with confidence {confidence}")

def save_as_unicode(input_file, output_file):
    with open(input_file, 'r', encoding='GB2312') as f:
        content = f.read()
    
    with codecs.open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

save_as_unicode('relation3.csv', 'relation3.csv')
detect_encoding('relation3.csv')

# import csv

# def remove_empty_course2(input_file, output_file):
#     with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
#          open(output_file, 'w', newline='', encoding='utf-8') as outfile:

#         reader = csv.DictReader(infile)
#         writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
#         writer.writeheader()

#         for row in reader:
#             if row['course2']:  # 检查 course2 列是否为空
#                 writer.writerow(row)

# # 调用函数并传入输入和输出文件路径
# remove_empty_course2('relation4.csv', 'relation5.csv')
