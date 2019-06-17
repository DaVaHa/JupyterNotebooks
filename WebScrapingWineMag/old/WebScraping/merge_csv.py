'''

Merge scraped files www.winemag.com.


'''


import pandas as pd
import os

# path
path = '/home/daniel/Desktop/Scripts/DataCamp/WebScraping//'

files = [f for f in os.listdir(path) if f.endswith('.csv') and 'winemag' in f]
#print(files)

# all extra files
print("\n -- EXTRA -- \n")

extra_files = [f for f in files if 'extra' in f]
print(extra_files)

extra = pd.DataFrame()

for f in extra_files:
    print(f)
    df = pd.read_csv(path + f, delimiter='|', header=None)
    #print(df.head())
    #print("{} - Rows : {}".format(f,len(df)))
    
    extra = extra.append(df)

extra.columns = ['URL', 'Alcohol', 'Color','RatingDate', 'Editor']
#print(extra.head())
print(extra.info())



# all front files
print("\n -- FRONTS -- \n")

front_files = [f for f in files if 'extra' not in f]
print(front_files)


front = pd.DataFrame()

for f in front_files:
    print(f)
    if f == 'winemag_v2018.csv':
        df = pd.read_csv(path + f, delimiter='|', header=None, skiprows=[16830])
    elif f == 'winemag_v1000_2000.csv':
        df = pd.read_csv(path + f, delimiter='|', header=None, skiprows=[])
        
    else:
        df = pd.read_csv(path + f, delimiter='|', header=None)
        
    #print(df.head())
    #print("{} - Rows : {}".format(f,len(df)))
    
    front = front.append(df)



front.columns= ['URL','Name','Rating', 'Price','Region']
#print(front.head())
print(front.info())


extra.to_csv('details.csv', index=False)
front.to_csv('overview.csv', index=False)

# join df

extra.set_index('URL', inplace=True)
front.set_index('URL', inplace=True)

full = front.join(extra, how='inner')

print(full.info())

print(full.drop_duplicates().info())


full = full.drop_duplicates()

full.to_csv(path + "winemag.csv")


""" OLD

print(files)

df1 = pd.read_csv(path + [f for f in files if 'extra' not in f][0], sep='|', header=None, names=['URL','Name','Rating', 'Price','Region'])
df2 = pd.read_csv(path + [f for f in files if 'extra' in f][0], sep='|', header=None, names=['URL', 'Alcohol', 'Color','RatingDate'])

df1.set_index('URL', inplace=True)
df2.set_index('URL', inplace=True)

df = df1.join(df2, how='inner')
print(df.info())

df.to_csv(path + 'WineMag.csv')

"""

