def clean_dataset(df,long=False):
# choose correct columns
    df= df[['Title','prices','Short reviews','Long Reviews']]
# clean Title
    def extract_title(text):
        doc= nlp(text)
        clean_title=''
        for token in doc:
            if token.pos_ in ('NOUN','PROPN','NUM'):
                if len(clean_title.split())!=3:
                    clean_title= clean_title + ' '+token.text
        return clean_title.strip()
    
    df['clean_titles']= df['Title'].apply(lambda x: extract_title(x))
# clean prices
    def extract_numbers(x):
        return ''.join(re.findall('[0-9]',x))
    df['clean_prices']= df['prices'].apply(lambda x:extract_numbers(x))
    df['reviews']= df['Short reviews'].apply(ast.literal_eval)
    li=[]
    long_review=[]
    for i in range(4):
        reviews=df.iloc[i]['reviews']
        title= df.iloc[i]['Title']
        price= df.iloc[i]['clean_prices']
        LR= ast.literal_eval(df.iloc[i]['Long Reviews'])
        long_review.append(pd.Series(LR))
        li.append(pd.DataFrame({'id':i,'Tite':title,'price':price,'SR':reviews}))
    long_texts=pd.concat(long_review)
    main_df= pd.concat(li)
    
    if long:
        return main_df,long_texts
    else:
        return main_df
x,y= clean_dataset(df,True)
