import sys
from version import ver2 as version

vers = sys.argv[1]
if vers == "Q1":
    from version import ver1 as version
if vers == "Q2":
    from version import ver2 as version


dict_tab = version.tables
numbers_table = dict_tab.keys()    #keys
values = dict_tab.values()     # values
for value in values:
    for i in value:
        print(i.values())

# for num in num_table:
#     print(num)        # table's number