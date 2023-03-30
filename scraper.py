import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm_project.settings')
django.setup()

# import pandas as pd
# from store.models import ProductTags


# # retrieve the HTML data
# url = 'https://www.color-hex.com/color-names.html'
# dfs = pd.read_html(url)

# # extract the first table and print it
# df = dfs[0]
# print(df)

# for index, row in df.iterrows():
#     color_name = row['Color Name']
#     hex_value = row['Color Code']
#     try:    
#         product_color = ProductColor.objects.create(color_name=color_name, color_hex=hex_value)
#         product_color.save()
#     except:
#         print(f' {color_name} \t Color already exists')


# tags = [ "Button-up shirts", "Dress shirts", "Polo shirts", "T-shirts", "Henley shirts", "Flannel shirts", "Plaid shirts", "Graphic T-shirts", "Hawaiian shirts", "Oxford shirts", "Chambray shirts", "Denim shirts", "Linen shirts", "Work shirts", "Western shirts", "Sport shirts", "Short sleeve shirts", "Long sleeve shirts", "Casual shirts", "Formal shirts", "Printed shirts", "Embroidered shirts", "Striped shirts", "Checkered shirts", "Solid color shirts", "Slim fit shirts", "Loose fit shirts", "Vintage t-shirts", "Retro t-shirts", "Band t-shirts", "Graphic tees", "Pocket tees", "V-neck t-shirts", "Crewneck t-shirts", "Slogan t-shirts", "Sports t-shirts", "Plain t-shirts", "Athletic t-shirts", "Logo t-shirts", "Fitted t-shirts", "Oversized t-shirts", "Crop tops", "Muscle tees", "Tanks", "Sleeveless shirts", "Collared shirts", "Summer shirts", "Winter shirts", "skinny jeans", "high-waisted jeans", "ripped jeans", "straight-leg jeans", "boyfriend jeans", "flare jeans", "mom jeans", "cropped jeans", "bootcut jeans", "acid wash jeans", "distressed jeans", "raw hem jeans", "wide-leg jeans", "colored jeans", "denim shorts", "relaxed fit jeans", "skinny bootcut jeans", "skinny ankle jeans", "black jeans", "white jeans",
# "sneakers","boots","loafers","oxfords","sandals","heels","flats","wedges","mules","slingbacks","ankle boots","combat boots","Chelsea boots","hiking boots","running shoes","slip-on shoes","flip flops","platform shoes",]

# tags = [tag.lower() for tag in tags]

# for i in tags:
#     try:
#         tag = ProductTags.objects.create(name=i)
#         tag.save()
#     except:
#         print(f' {i} \t Tag already exists')



from store.models import ProductSize, ProductVariationCategory

sizes = ["S", "M", "L", "XL", "XXL"]

pvc = ProductVariationCategory.objects.all()

print(pvc[0])

for i in sizes:
    obj = ProductSize.objects.create(name=i, product_variation_category=pvc[0])

print("done")