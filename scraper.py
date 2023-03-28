import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm_project.settings')
django.setup()

import pandas as pd
from store.models import ProductColor


# retrieve the HTML data
url = 'https://www.color-hex.com/color-names.html'
dfs = pd.read_html(url)

# extract the first table and print it
df = dfs[0]
print(df)

for index, row in df.iterrows():
    color_name = row['Color Name']
    hex_value = row['Color Code']
    try:    
        product_color = ProductColor.objects.create(color_name=color_name, color_hex=hex_value)
        product_color.save()
    except:
        print(f' {color_name} \t Color already exists')
