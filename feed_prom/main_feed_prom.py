import xml.dom.minidom
import pymssql

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")
db = conn.cursor()


def category():
    db.execute("CREATE TABLE category (cat_id NVARCHAR(3), cat_value NVARCHAR(560)) ")
    conn.commit()

    categories = doc.getElementsByTagName("category")
    for cat in categories:
        cat_id = cat.getAttribute("id")
        cat_value = cat.firstChild.data

        db.execute(f"INSERT INTO category VALUES( N'{cat_id}', N'{cat_value}')")
        conn.commit()


def items_func():
    db.execute("CREATE TABLE items (item_id NVARCHAR(100), item_name NVARCHAR(360), categoryId NVARCHAR(100), url NVARCHAR(560), vendor NVARCHAR(60), image NVARCHAR(560), description ntext)")
    conn.commit()

    items = doc.getElementsByTagName("item")
    param_func(items)
    for item in items:
        item_number = item.getAttribute("id")
        item_name = item.getElementsByTagName("name")[0].firstChild.data
        item_name = item_name.replace("'", '"')

        category_id = item.getElementsByTagName("categoryId")[0].firstChild.data
        url = item.getElementsByTagName("url")[0].firstChild.data
        vendor = item.getElementsByTagName("vendor")[0].firstChild.data
        image = item.getElementsByTagName("image")[0].firstChild.data
        description = item.getElementsByTagName("description")[0].firstChild.data
        description = description.replace("'", '"')

        db.execute("""INSERT INTO items VALUES(N'""" + item_number + """', N'"""+item_name+"""', N'""" + category_id + """', N'""" + url + """', N'""" + vendor + """', N'"""+image + """', N'"""+description + """')""")
        conn.commit()

    return "Writing to tables finished"


def param_func(items):
    db.execute("CREATE TABLE parameters (item_id NVARCHAR(100), property  NVARCHAR(100),value NVARCHAR(100))")
    conn.commit()

    for item in items:
        item_number = item.getAttribute("id")

        params = item.getElementsByTagName("param")
        for param in params:
            name_param = param.getAttribute("name")
            value_param = param.firstChild.data

            db.execute("""INSERT INTO parameters VALUES(N'""" + item_number + """', N'"""+name_param +"""', N'"""+value_param +"""')""")
            conn.commit()


def main():
    category()
    items_func()




if __name__ == "__main__":
    doc = xml.dom.minidom.parse("feed_prom.xml")
    main()
