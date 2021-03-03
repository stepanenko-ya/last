import xml.dom.minidom
import pymssql



conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")
db = conn.cursor()

doc = xml.dom.minidom.parse("osprey_ua.xml")


def cat_osprey():
    db.execute("""create table [schema_two].[Category_Osprey] (cat_id NVARCHAR (10), parentID NVARCHAR (10),cat_value NVARCHAR (100))""")
    conn.commit()

    categories = doc.getElementsByTagName("category")
    for cat in categories:

        cat_id = cat.getAttribute("id")
        parentID = cat.getAttribute("parentID")
        cat_value = cat.firstChild.data.strip()

        db.execute(f"""insert into [schema_two].[Category_Osprey] values (N'{cat_id}', N'{parentID}', N'{cat_value}')""")
        conn.commit()


def item_func():

    db.execute("""create table [schema_two].[osprey_item] (item_id NVARCHAR(20), name NVARCHAR(220),url  NVARCHAR(220),categoryId NVARCHAR(220), vendor  NVARCHAR(60), image NVARCHAR(260), fcod NVARCHAR(20),  description ntext,
        product_model_id NVARCHAR(100), modelfcod NVARCHAR(20), modelname NVARCHAR(100), modelimage NVARCHAR(200))""")
    conn.commit()

    items = doc.getElementsByTagName("item")

    for item in items:
        item_id = item.getAttribute("id")
        name_ = item.getElementsByTagName("name")[0].firstChild.nodeValue
        url = item.getElementsByTagName("url")[0].firstChild.data
        categoryId = item.getElementsByTagName("categoryId")[0].firstChild.data
        vendor = item.getElementsByTagName("vendor")[0].firstChild.data
        image = item.getElementsByTagName("image")[0].firstChild.data
        fcod = item.getElementsByTagName("fcod")[0].firstChild.data
        model = item.getElementsByTagName("model")
        if model:
            fcod = ""
        description = item.getElementsByTagName("description")[0].firstChild
        if description != None:
            description = description.data.replace("'", '"')

        else:
            description = ""

        if model:
            for mod in model:
                product_model_id = mod.getAttribute("product_model_id")
                modelfcod = mod.getElementsByTagName("fcod")[0].firstChild.data
                modelname = mod.getElementsByTagName("modelname")[0].firstChild.data
                modelimage = mod.getElementsByTagName("modelimage")[0].firstChild.data

                db.execute(f"""INSERT INTO [schema_two].[osprey_item] VALUES (N'{item_id}', N'{name_}', N'{url}', N'{categoryId}', N'{vendor}',  N'{image}', N'{fcod}', N'{description}',
                N'{product_model_id}', N'{modelfcod}', N'{modelname}', N'{modelimage}')""")
                conn.commit()
        else:
            db.execute(f"""INSERT INTO [schema_two].[osprey_item] (item_id, name, url, categoryId, vendor, image, fcod, description)
                  VALUES (N'{item_id}', N'{name_}', N'{url}', N'{categoryId}', N'{vendor}', N'{image}',  N'{fcod}', N'{description}')""")
            conn.commit()


if __name__ == "__main__":
    cat_osprey()
    item_func()




