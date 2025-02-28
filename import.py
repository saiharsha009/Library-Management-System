import csv, sqlite3

con = sqlite3.connect("./data/library.db")
cur = con.cursor()

with open("./data/books.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        ## bookID, title, authors, average_rating, isbn, isbn13,
        ## language_code, num_pages, ratings_count, text_reviews_count, 
        ## publication_date, publisher

        ## INSERT INTO Books VALUES (book_id, bookname, publisher, rating,
        ## author_id

        values = (row['bookID'],\
                  str(row['title']),row['publisher'],row['average_rating'],\
                  row['bookID'])
        placeholders = ','.join(['?'] * len(values))
        cur.execute(f"INSERT INTO books VALUES ({placeholders})", values)
        values2 = (row["bookID"], row["authors"])
        placeholders2 =  ','.join(['?'] * len(values2))
        cur.execute(f"INSERT INTO authors VALUES ({placeholders2})", values2)

con.commit()
con.close()
