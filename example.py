import psycopg2
from tabQ import TecDoc
import sys
import csv
from sys import argv
import py7zr
import os
import shutil
import datetime

conn = psycopg2.connect(
    host='localhost',
    user='stepanenko',
    password='Stomatolog',
    database='test2',
    )
db = conn.cursor()


def create_table(tab_num):
    tab = version.tables.get(tab_num)
    column_name = ""
    for col in tab:
        column_name += col["name"] + " nchar(" + str(col["length"]) + "), "

    command_create = "CREATE TABLE IF NOT EXISTS  dbo.t" + tab_num + " (" + column_name[:-2] + ")"
    db.execute(command_create)
    conn.commit()
    return tab_num

res = []
def file_parsing(unpack_file):
    x = []
    path_to_file = "unpacked_data" + "/" + unpack_file

    with open(path_to_file, "r") as file:
        tab_num = unpack_file[:3]
        print(f"Запись в {tab_num}")
        file_intermedia = open("intermediate.csv", "w")
        for row in file:
            if "🔺" in row:
                row = row.replace("🔺", "  ")

            if "\\" in row:
                x.append(tab_num)
                row = row.replace('\\', "^")
            #     row = row.replace('|', '{')

            step = 0
            string_data = ""
            tab = version.tables.get(tab_num)
            for column in tab:
                data = row[step:step + column["length"]]
                step += column["length"]
                string_data += data + "|"

            file_intermedia.writelines(string_data[:-1] + "\n")

        file_intermedia.close()
    res.extend(x)
    f_csv = open('/home/stepanenko/Projects/test/test/intermediate.csv', 'r')
    db.copy_from(f_csv, "dbo.t" + tab_num, sep="|")
    conn.commit()
    f_csv.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'intermediate.csv')
    os.remove(path)
    return set(res)


def main(unpak_files):

    for file in unpak_files:
        if file[-3:] != "GIF":
            create_table(file[:3])
            parsing = file_parsing(file)



    shutil.rmtree("unpacked_data")
    print(set(res))


    # os.remove("archives/" + arch_file)


if __name__ == '__main__':
    vers = sys.argv[1]

    if vers == "Q1":
        from version import ver1 as version
    if vers == "Q2":
        from version import ver2 as version
    if vers == "Q3":
        from version import ver3 as version
    if vers == "Q4":
        from version import ver4 as version

    field = "BrandNo"
    archive_direct = os.listdir("archives")
    for arch_file in archive_direct:
        print("Разархивация файлов...", arch_file)
        archive = py7zr.SevenZipFile("archives/" + arch_file, mode='r')
        archive.extract("unpacked_data")
        all_files = os.listdir("unpacked_data")
        main(all_files)


