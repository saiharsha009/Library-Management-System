import streamlit as st
import pandas as pd
import requests

import seaborn as sns
import matplotlib.pyplot as plt


from streamlit_option_menu import option_menu

API_URL = 'http://127.0.0.1:5000/'

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    data = response.json()
    return data




def user_id(username):
    response = requests.get(f'{API_URL}/user/{username}').json()
    return response["user_id"]

def send_feedback(feedback, username, rating, bookid):
    data = {
        'feedback': feedback,
        'user_id': user_id(username),
        'rating': rating,
        'book_id': bookid
    }

    response = requests.post(f'{API_URL}/feedback', json=data)
    return response

def borrow(book_id, username):
    data= {
        'user_id': user_id(username),
        'book_id': book_id
    }
    response = requests.post(f'{API_URL}/borrow', json=data)
    return response

def return_book(loan_id):
    data={
        'loan_id': loan_id
    }
    response = requests.post(f'{API_URL}/return_book', json=data)
    return response
    

def st_catalogue():
    st.title("Book Search")
    title_search = st.empty()
    search_btn = st.empty()

    title = title_search.text_area("Enter your book name")
    search = search_btn.button("Enter")

    if search:
        df = pd.DataFrame(
            requests.get(f"{API_URL}/search/{title}").json()
        )

        if df is not None:
            title_search.empty()
            search_btn.empty()

            st.dataframe(
                df,
                column_config={
                    "bookname": "Title",
                    "publisher": "Publisher",
                    "rating": st.column_config.NumberColumn(
                        "Rating Stars",
                        help="Number of stars on GitHub",
                        format="%f ⭐",),
                        
                },
                column_order=("bookname", "publisher", "rating"),
                use_container_width=True,
                hide_index=True,)

def st_book_finder():
    st.title("Books Search")

    selection = st.selectbox("Please Select any Filter",("Name of the Book","Name of the Author"))
    if selection == "Name of the Book":
        enterbook = st.text_input("Enter the Book Name")
        
    elif selection == "Name of the Author":
        enterbook= st.text_input("Enter the Author Name")
        
    if st.button("Search"):
        if (enterbook ):
            books_data = search_books(enterbook)
            if 'items' in books_data:
                for book in books_data['items']:
                    volume_info = book['volumeInfo']
                    title = volume_info.get('title', 'No title available')
                    authors = volume_info.get('authors', ['Unknown author'])
                    description = volume_info.get('description', 'No description available')
                    thumbnail = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info else None
                    st.image(thumbnail, caption=title, width=100)
                    st.write(f"Title: {title}")
                    st.write(f"Authors: {', '.join(authors)}")
                    st.write(f"Description: {description}")
                    st.write("--------------------------------------------------")


        if (enterbook):
            books_data = search_books(enterbook)
            if 'items' in books_data:
                for book in books_data['items']:
                    volume_info = book['volumeInfo']
                    title = volume_info.get('title', 'No title available')
                    authors = volume_info.get('authors', ['Unknown author'])
                    description = volume_info.get('description', 'No description available')
                    # thumbnail = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info else None
                    # st.image(thumbnail, caption=title, width=100)
                    st.write(f"Title: {title}")
                    st.write(f"Authors: {', '.join(authors)}")
                    st.write(f"Description: {description}")
                    st.write("--------------------------------------------------")
            

            else:
                st.write("No books found.")
        else:
            st.write("Please enter a search term.")

# Function to plot top rated books
def plot_top_rated_books():
    most_rated = finder.sort_values('ratings_count', ascending=False).head(10)
    plt.figure(figsize=(15,15))
    sns.lineplot(x=most_rated['ratings_count'], y=most_rated.title, palette='BuGn_r')  # Change palette here
    plt.title("Top 10 Most Rated Books")
    plt.xlabel("Number of Ratings")
    plt.ylabel("Books")
    st.pyplot()

# Function to plot most occurring books
def plot_most_occuring_books():
    most_occuring = finder['title'].value_counts().head(10)
    plt.figure(figsize=(1005, 10))
    sns.displot(x=most_occuring.values, y=most_occuring.index)  # Change palette here
    plt.title("Top 10 Most Occurring Books")
    plt.xlabel("Number of Occurrences")
    plt.ylabel("Books")
    st.pyplot()
def plot_top_authors_with_most_books(finder):
    authors_books_count = finder['authors'].value_counts().head(10)
    plt.figure(figsize=(15, 10))
    sns.barplot(x=authors_books_count.values, y=authors_books_count.index, palette='icefire_r')
    plt.title("Top 10 Authors with Most Books")
    plt.xlabel("Total Number of Books")
    plt.ylabel("Authors")
    for i in range(len(authors_books_count)):
        plt.text(authors_books_count.values[i] + 0.3, i, str(authors_books_count.values[i]), fontsize=10, color='black')
    st.pyplot()
def plot_top_books_by_text_reviews(finder): 
    print(finder.columns) 
    top_text_reviews =finder.sort_values('text_reviews_count', ascending=False).head(10)
    plt.figure(figsize=(15, 10))
    sns.set_context('notebook')
    ax = sns.barplot(x=top_text_reviews['text_reviews_count'], y=top_text_reviews.title, palette='plasma')
    plt.title("Top 10 Books with Most Text Reviews")
    plt.xlabel("Text Reviews Count")
    plt.ylabel("Books")
    for patch in ax.patches:
        ax.text(patch.get_width() + 2, patch.get_y() + 0.5, str(round(patch.get_width())), fontsize=10, color='black')
    st.pyplot()
def top_publishers(finder):
    st.write()
    import seaborn as sns
    import matplotlib.pyplot as plt
    publisher_top_10 = finder['publisher'].value_counts().head(10)
    publisher_top_10 = pd.DataFrame(publisher_top_10)
    plt.pie(publisher_top_10['count'], labels=publisher_top_10.index)
    plt.show()
    st.pyplot()


    
def book_manager():
    st.title('Book Mangment')

    usrtype=st.selectbox('Select the Qualification',('Borrow', 'Return'))
    if usrtype == "Borrow":
        bookid = st.text_input('Enter the book id')
        username=st.text_area("Enter your name")
        if st.button("submit"):
            response = borrow(bookid, username)
            if response.status_code == 201:
                st.write(f"Book borrowed, your loan id is : {response.json().get('loan_id')}")
            else:
                st.write("Unable to borrow book. Check with admin")
    if usrtype == "Return":
        loanid = st.text_input('Enter the loan id')
        if st.button("submit"):
            response = return_book(loanid)
            if response.status_code == 201:
                st.write("Book returned")
            else:
                st.write("Unable to return book. Check with admin")    



       
if __name__ == "__main__":

    with st.sidebar:
        choose = option_menu("Navigation", ["Book Finder", "Catalog", "Analysis","Book Manager","Feedback"])
        

    if choose == "Book Finder":
        st_book_finder()
    if choose == "Catalog":
        st_catalogue()
    if choose == "Analysis":
        finder=pd.read_csv(r"data/books.csv", on_bad_lines='skip')
        finder.dropna(inplace=True)

        st.title("Book Dataset Analysis")

        st.set_option('deprecation.showPyplotGlobalUse', False)
        option = st.selectbox('Select Analysis',('Top Rated Books', 'Most Occurring Books','Top 10 Authors with Most Books',
                                                'Top Rated Books by Reviews','Top Book Publishers'))

        if option == 'Top Rated Books':
            plot_top_rated_books()
        elif option == 'Most Occurring Books':
            plot_most_occuring_books()
        elif option == "Top 10 Authors with Most Books":
            plot_top_authors_with_most_books(finder)
        elif option == "Top Rated Books by Reviews":
            plot_top_books_by_text_reviews(finder)
        elif option == "Top Book Publishers":
            top_publishers(finder)

    if choose == "Book Manager":
        book_manager()

    if choose == "Feedback":
        with st.form(key='feedback_form', clear_on_submit=True):
            username = st.text_area('Enter your username')
            bookid = st.number_input(placeholder='Enter book name', label='bookid', min_value=1, max_value=11000,step=1)
            Feedback = st.text_area('Please Enter Your Feedback', height=200)
            rating = st.number_input(label="rating", min_value=1., max_value=5., step=0.5, value=1.)
            submitted = st.form_submit_button('Submit')
            
            if submitted:
                response = send_feedback(Feedback, username, rating, bookid)
                if response.status_code == 201:
                    st.success(f'Review submitted successfully for user {username}!')
                else:
                    st.error('Failed to submit feedback. Please try again.')
            else:
                st.warning('Please fill in all fields.')