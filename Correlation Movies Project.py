#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure

get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['figure.figsize'] = (12,8)


# In[5]:


df = pd.read_csv(r'C:\Users\RakeshB\Downloads\movies.csv')


# In[6]:


df.head()


# In[8]:


# Check for missing data

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print ('{} - {}%'.format(col, pct_missing))


# In[9]:


df.isnull().sum()


# In[10]:


# extract the date from realease column

df['year_release'] = df['released'].astype('str').str.extract('(\d{4})')
df


# In[12]:


# removing the null value

df['rating'] = df['rating'].replace(np.nan, 'Unknown')
df['released'] = df['released'].replace(np.nan, 'Unknown')
df['score'] = df['score'].replace(np.nan, 0)
df['votes'] = df['votes'].replace(np.nan, 0)
df['writer'] = df['writer'].replace(np.nan, 'Unknown')
df['star'] = df['star'].replace(np.nan, 'Unknown')
df['country'] = df['country'].replace(np.nan, 'Unknown')
df['budget'] = df['budget'].replace(np.nan, 0)
df['gross'] = df['gross'].replace(np.nan, 0)
df['company'] = df['company'].replace(np.nan, 'Unknown')
df['runtime'] = df['runtime'].replace(np.nan, 0)


# In[14]:


# Checking if all null values replaced or not

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print ('{} - {}%'.format(col, pct_missing))


# In[15]:


df['year_release'] = df['year_release'].replace(np.nan, 0)

# again checking for any missing data

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print ('{} - {}%'.format(col, pct_missing))


# In[16]:


# checking data type for the columns

print(df.dtypes)


# In[17]:


# sort data by gross

df.sort_values(by=['gross'], inplace=False, ascending=False)


# In[18]:


# Create a scatter chart budget vs gross

df.plot.scatter(x='budget', y='gross')

# Adding Label

plt.title('budget vs gross')
plt.xlabel('budget')
plt.ylabel('gross')

plt.show()


# In[21]:


# using Seaborn

sns.regplot(x='budget', y='gross', data = df, scatter_kws={"color":"blue"}, line_kws={"color":"Green"})
plt.show


# In[22]:


# use correlation demo

df.corr(method='pearson')


# In[23]:


#let see heatmap with the help of correlation

sns.heatmap(df.corr(method='pearson'), annot=True)
plt.title('Correlation Matrix for Numeric Features')
plt.show()


# In[25]:


# Start with our data

df_sample = df.copy()


for col_name in df_sample.columns:
    if (df_sample[col_name].dtype == 'object'):
        df_sample[col_name] = df_sample[col_name].astype('category')
        df_sample[col_name] = df_sample[col_name].cat.codes

df_sample


# In[27]:



df_sample.corr()


# In[28]:


# creating correlation heatmap

correlation_matrix = df_sample.corr(method='pearson')

sns.heatmap(correlation_matrix, annot = True)

plt.title("Correlation matrix for Movies")
plt.xlabel("Movie features")
plt.ylabel("Movie features")

plt.show()


# In[33]:


# Find more popular genre by votes

ax = df[['genre','votes']].groupby(['genre']).sum().sort_values(by = ['genre'], ascending = True).plot(kind = 'bar')

ax.set_xlabel('genre')
ax.set_ylabel('votes')
ax.set_title('Most popular genre by votes')

plt.show()


# In[34]:


# check with the gross also

ax = df[['genre','gross']].groupby(['genre']).sum().sort_values(by = ['gross'], ascending = True).plot(kind = 'bar')

ax.set_xlabel('genre')
ax.set_ylabel('gross')
ax.set_title('Revenue by genre in millions USD($)')

plt.show()


# In[45]:


pip install prettytable


# In[56]:


# check about IMDB Score wise genre
from prettytable import PrettyTable

df_table = df[['genre','score']].groupby(['genre']).mean().sort_values(by = ['score'], ascending = False)

table = PrettyTable()
table.field_names = ["genre", "Average Score"]

# Adding values into new table
for index, row in df_table.iterrows():
    table.add_row([index, round(row['score'], 2)])

table.align["Genre"] = "l"  # left align the genre column
table.align["Average Score"] = "r"  # right align the score column
table.padding_width = 1  # add some padding to the cells

print(table)


# In[52]:


# Highest grossing Actors & Actresses

ax = df[['star','gross']].groupby(['star']).sum().sort_values(by = ['gross'], ascending = False).head(50).plot(kind = 'barh')

ax.set_xlabel('star')
ax.set_ylabel('gross')
ax.set_title('Highest grossing Actors & Actresses')

plt.show()


# In[54]:


# Highest Grossing Directors

ax = df[['director','gross']].groupby(['director']).sum().sort_values(by = ['gross'], ascending = False).head(50).plot(kind = 'barh')

ax.set_xlabel('director')
ax.set_ylabel('gross')
ax.set_title('Highest Grossing Directors')

plt.show()


# In[ ]:




