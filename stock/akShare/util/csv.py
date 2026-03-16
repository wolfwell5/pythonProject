from stock.akShare.util.file_name import generate_file_name


# 生成csv文件 到当前执行程序的同一目录下
def generate_csv(data_frame, file_name, specific_folder):
    full_path_csv = generate_file_name(file_name, specific_folder)
    data_frame.to_csv(full_path_csv, index=False)
    print(f'生成csv文件完毕， 路径：  {full_path_csv}')


# append 数据到csv文件中 todo