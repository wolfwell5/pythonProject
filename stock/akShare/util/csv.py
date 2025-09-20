from stock.akShare.util.file_name import generate_file_name


def generate_csv(data_frame, file_name):
    full_path_csv = generate_file_name(file_name)
    data_frame.to_csv(full_path_csv, index=False)
    print(f'生成csv文件完毕， 路径：  {full_path_csv}')
