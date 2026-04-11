import shutil
import os
import pandas as pd

def organize_data(df):
    """Organizes images and data into star-rated folders."""
    if df.empty:
        return

    # organizing data
    star_1_books = df[df['star_rating'] == 1].copy()
    star_2_books = df[df['star_rating'] == 2].copy()
    star_3_books = df[df['star_rating'] == 3].copy()
    star_4_books = df[df['star_rating'] == 4].copy()
    star_5_books = df[df['star_rating'] == 5].copy()

    # organizing imgs
    def sorting_imgs(books):
        for i in range(len(books)):
            img_path = books.iloc[i]['img_path']
            title = books.iloc[i]['title']
            star_rating = books.iloc[i]['star_rating']
            target_path = f"./images/{star_rating}_star/{title}.png"
            
            # Check if source exists and move it. If we run multiple times, it might already be in target
            if os.path.exists(img_path):
                shutil.move(img_path, target_path)
            
            # Update path in dataframe
            books.iloc[i, books.columns.get_loc('img_path')] = target_path

    sorting_imgs(star_1_books)
    sorting_imgs(star_2_books)
    sorting_imgs(star_3_books)
    sorting_imgs(star_4_books)
    sorting_imgs(star_5_books)

    star_1_books.to_csv("./data/processed/1_star/1_star_books.csv", index=False)
    star_2_books.to_csv("./data/processed/2_star/2_star_books.csv", index=False)
    star_3_books.to_csv("./data/processed/3_star/3_star_books.csv", index=False)
    star_4_books.to_csv("./data/processed/4_star/4_star_books.csv", index=False)
    star_5_books.to_csv("./data/processed/5_star/5_star_books.csv", index=False)
