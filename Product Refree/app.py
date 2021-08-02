# -*- coding: utf-8 -*-

import scrapper.scarpper as sc
import datacleaning.script as dc

df= sc.scrap_obj('Best earphones under 10000')
cleaned_df= dc.clean_dataset(df,long=True)

