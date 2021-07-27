from joblib import Parallel,delayed

def make_searchable_item_rows(item):
    print(item)
elements=[(x,x**2) for x in range(10)]

Parallel(n_jobs=-2)(delayed(make_searchable_item_rows) (item) for item in elements)
