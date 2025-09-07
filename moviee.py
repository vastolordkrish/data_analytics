
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#----------------------------------------------------------------------------------------------------

#ui setup
root=tk.Tk()
root.title("Excel data preview")
root.geometry("600x400")

title_label =tk.Label(root,text="Movie review analysis",font=("Arial", 24 ,"bold"))
title_label.pack(pady=10)


#left side
left_frame = tk.Frame(root)
left_frame.pack(side="left", expand = True, fill="both")

right_frame= tk.Frame(root, width=300)
right_frame.pack(side="bottom",fill="both",expand=True)


#**charts**
chart_frame=tk.Frame(left_frame, height=400)
chart_frame.pack(side="bottom", expand = True, fill="both")





text_box =tk.Text(left_frame,wrap=tk.WORD, font=("courier",10), height=15)
text_box.pack(expand=True,fill="both", padx=10,pady=10)



result_lable = tk.Label(right_frame, text=" ",font=("Arial", 12),justify="left",anchor="n")
result_lable.pack(pady=10, padx=10,)


#value count
value_count_label = tk.Label(right_frame, text="", font=("Arial", 12),justify="left",anchor="n")
value_count_label.pack(padx=10, pady=10)

#filter
genre_entry = tk.Entry(right_frame)
genre_entry.pack(pady=5)
filtered_text= tk.Text(right_frame, height=10, width=50)
filtered_text.pack(pady=5)
filter_button = tk.Button(right_frame, text="Search by Genre")
filter_button.pack(pady=5)


#-----------------------------------------------------------------------------------------------------
#uplod file



def upload_file():
    global df
    file_path= filedialog.askopenfilename(title ="select the movie excel file",
                                         filetypes=[("excel files","*.xlsx",)])
 #reading uploded 
    #df.fillna("not inserted")

    
    if file_path:
        try:
            df=pd.read_excel(file_path)
            preview_data=df.head().to_string(index=False)
            text_box.delete("1.0",tk.END)
            text_box.insert(tk.END,preview_data)




            
            #[3]data analysis

            #to calculate average rating
 
            avg_rating = df['IMDb_Rating'].mean()
        

            avg_budget = df['Budget_USD'].mean()
           

            #highest and lowest rating and budget

            #rating:
            max_rating = df['IMDb_Rating'].max()
            

            min_rating = df['IMDb_Rating'].min()
            

            #budget:
            max_budget = df['Budget_USD'].max()
           

            min_budget = df['Budget_USD'].min()
           


            stats_text =f"""
                ✿ Analyzed data ✿
            Ratings:
            -maximum rating: {max_rating}
            -minimum rating: {min_rating}
            -average rating: {avg_rating:.2f}

            Budgeting:
            -maximum budget: {max_budget} $
            -minimum budget: {min_budget} $
            -average budget: {avg_budget:.2f} $
            """
            result_lable.config(text=stats_text)

            genre_count = df['Genre'].value_counts()
            value_count_text = "*values count by category :\n" + genre_count.to_string()
            value_count_label.config(text=value_count_text)

            for widget in chart_frame.winfo_children():
                 widget.destroy()

            #----------------------------charts=========================


            fig ,axes = plt.subplots(2, 2, figsize=(10, 6))


            #barchart
            df['Genre'].value_counts().plot(kind='bar', ax=axes[0,0],color='skyblue', edgecolor='black')
            axes[0,0].set_title("genre bar chart")
            axes[0,0].set_ylabel("count")


            #pichart
            df['Genre'].value_counts().plot(kind='pie', ax=axes[0,1], autopct='%1.1f%%')
            axes[0,1].set_title("Genre Pie Chart")
            axes[0,1].set_ylabel("") 

            #scatter char
            sns.scatterplot(x='Genre', y='Oscars_Won', data=df, ax=axes[1,0])
            axes[1,0].set_title("Genre vs Number of Oscars")
            axes[1,0].set_xlabel("Genre")
            axes[1,0].set_ylabel("Oscars Won")

            #histogram
            df['Genre'].value_counts().plot(kind='hist', bins=5, color='lightgreen', edgecolor='black', ax=axes[1,1])
            axes[1,1].set_title("Count by Genre")
            axes[1,1].set_xlabel("Count")
            axes[1,1].set_ylabel("Genre")

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)




        except Exception as e:
                messagebox.showerror("Error",f"An error occured: {e}")

#operations

#** data filter function **

def filter_genre():
     
     genre = genre_entry.get()

     if 'df' in globals():
          filtered_df=df[df['Genre']==genre]
          filtered_text.delete("1.0",tk.END)
          if not filtered_df.empty:
               display_df = filtered_df[['Movie', 'Year', 'Genre']]
               filtered_text.insert(tk.END, display_df.to_string(index=False))
     else:
               filtered_text.insert(tk.END, f"no movies found for genre: {genre}")
          
               filtered_text.insert(tk.END, f"no movies found for genre: {genre}")

filter_button.config(command=filter_genre)

#-----------------------------------------------------UI------------------------------------------------------------------                

#button
upload_btn = tk.Button(root,text="upload file",command=upload_file,font=("Arial",12))
upload_btn.pack(side="top",pady=10)



root.mainloop()

df.to_excel("cleand_movie_data.xlsx",index=False)
