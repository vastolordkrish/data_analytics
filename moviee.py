import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#[1]data loading
df = pd.read_excel("movie_data.xlsx")

print(df.head())


#[2]data cleaning

#show missing values
print("df.isnull().sum()")

#replace missing values with not inserted
df.fillna("not inserted")

#delete duplicate values
dd = df.drop_duplicates()

#change column titles:
#1.orignal coloumns
print("orignal coloumns :")
print(df.columns)

df.columns = df.columns.str.strip().str.upper()
#2.capital coloumns title
print("\ncapital coloumns title:")
print(df.columns)

#remove extra space 

df["MOVIE"]=df["MOVIE"].str.strip()

df["GENRE"]=df["GENRE"].str.strip()

df["PRODUCTION_STUDIO"]=df["PRODUCTION_STUDIO"].str.strip()

#changing datatype
df['SR.NO'] = df['SR.NO'].astype(int)
#df['OSCAR WON'] = df['OSCAR WON'].astype(float)


#[3]data analysis

#to calculate average rating
 
avg_rating = df['IMDB_RATING'].mean()
print("average rating is :",avg_rating)

avg_budget = df['BUDGET_USD'].mean()
print("average budget is :",avg_budget)

#highest and lowest rating and budget

#rating:
max_rating = df['IMDB_RATING'].max()
print("maximum rating is :",max_rating)

min_rating = df['IMDB_RATING'].min()
print("minimum rating is :",min_rating)

#budget:
max_budget = df['BUDGET_USD'].max()
print("maximum budget is :",max_budget)

min_budget = df['BUDGET_USD'].min()
print("minimum budget is :",min_budget)

print("\n\n")

print("movie studios with most oscar :",df.groupby('PRODUCTION_STUDIO'))

#avg rating by genre using groupby
avg_rate_by_g = df.groupby('GENRE')['IMDB_RATING'].mean()


print(avg_rate_by_g)

print("\n\n")
#value count by category 

print("#value count by category :")
 
g_count = df['GENRE'].value_counts()
print(g_count)

#filtering by condition

a = (input("enter the genre :"))

filtered_g = df[df['GENRE'] == a]

print(filtered_g)
print("\n\n")
#sorting

print("movies sorted by year :")
s_year = df.sort_values(by='YEAR', ascending=True)
print(s_year)

#[4]Creating Charts (Data Visualization)

#barchart
df['GENRE'].value_counts().plot(kind='bar')
plt.show()
plt.title("genre barchart")
plt.savefig("chart.png") 

#pie chart
df['GENRE'].value_counts().plot(kind='pie')
plt.show()
plt.title("genre pie chart")
plt.savefig("chart.png") 

#scatter plot
sns.scatterplot(x='GENRE', y='OSCARS_WON',data=df)
plt.title("genre x no of oscars")
plt.show()
plt.savefig("chart.png") 

#histogram
df['GENRE'].value_counts().plot(kind='hist',bins=5,color='skyblue',edgecolor='black')
plt.title("count by genre")
plt.xlabel("count")
plt.ylabel("genre")
plt.show()
plt.savefig("chart.png") 



#saving cleaned data
df.to_excel("cleand_movie_data.xlsx",index=False)