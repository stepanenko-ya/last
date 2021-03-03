from bs4 import BeautifulSoup
import pymssql

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test",
    charset = 'UTF-8')

db = conn.cursor()


infile = open("sigma.xml", "r")
content = infile.read()
soup = BeautifulSoup(content, 'xml')


def category():
    db.execute("""create table [sigma].[Category] (cat_id NVARCHAR (10), parentID NVARCHAR (10),cat_name NVARCHAR (200))""")
    conn.commit()

    category = soup.find_all('category')
    for cat in category:
        cat_id = cat.get("id")
        parentId = cat.get("parentId")
        cat_name = cat.get_text()
        db.execute(f"""insert into [sigma].[Category]values (N'{cat_id}', N'{parentId}', N'{cat_name}')""")
        conn.commit()


def items():
    db.execute("""create table [sigma].[Items] (
    offer_id NVARCHAR (100),
    url ntext,
    category_id NVARCHAR (600),
    vendor NVARCHAR (100),
    vendor_code NVARCHAR (100),
    name_item NVARCHAR (600),
    description ntext,
    manufacturer_warranty NVARCHAR (100)
    )""")
    conn.commit()

    offers = soup.find_all('offer')
    for offer in offers:
        offer_id = offer.get("id")
        url = offer.find('url').get_text()
        category_id = offer.find('categoryId').get_text()
        vendor = offer.find('vendor').get_text()
        vendor_code = offer.find('vendorCode').get_text()
        name_item = offer.find('name').get_text()
        description = offer.find('description').get_text()
        manufacturer_warranty = offer.find('manufacturer_warranty').get_text()

        db.execute(f"""INSERT INTO [sigma].[Items] VALUES (
        N'{offer_id}',
        N'{url}',
        N'{category_id}',
        N'{vendor}',
        N'{vendor_code}',
        N'{name_item}',
        N'{description}',
        N'{manufacturer_warranty}'
         )""")
        conn.commit()


def picture():
    db.execute("""create table [sigma].[Pictures] (item_id NVARCHAR (10),  param_value ntext)""")
    conn.commit()
    offers = soup.find_all('offer')
    for offer in offers:
        offer_id = offer.get("id")
        pictures = offer.find_all('picture')
        for pict in pictures:
            picture_url = pict.get_text()

            db.execute(f"""insert into [sigma].[Pictures]values (N'{offer_id}', N'{picture_url}')""")
            conn.commit()


def func_param():
    # db.execute("""create table [sigma].[Parametr] (item_id NVARCHAR (10), param_name NVARCHAR (100),  param_value NVARCHAR (200))""")
    # conn.commit()

    offers = soup.find_all('offer')
    for offer in offers:
        offer_id = offer.get("id")
        param = offer.find_all('param')
        for par in param:
            param_name = par.get("name")
            param_value = par.get_text()
            # db.execute(f"""insert into [sigma].[Parametr]values (N'{offer_id}', N'{param_name}', N'{param_value}')""")
            # conn.commit()


if __name__ == "__main__":
    items()
    picture()
    category()
    func_param()
