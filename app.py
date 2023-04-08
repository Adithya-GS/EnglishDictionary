import streamlit as st
from difflib import get_close_matches


import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="root@123",
    database="dictionary"
)
mycursor = mydb.cursor()

def searchWord(word):
    mycursor.execute("select word from words where word=%s", (word, ))
    obtainedWord = mycursor.fetchall()
    if len(obtainedWord) != 0:
        mycursor.execute("select meaning from meanings where word_id in (\
                            select word_id from words where word=%s)", (word, ))
        return mycursor.fetchall()
    else:
        mycursor.execute("select word from words")
        words = [word for row in mycursor.fetchall() for word in row ]
        if len(get_close_matches(word, words, cutoff=0.8))!=0:
            yn: str = st.text_input(f"Did you mean {get_close_matches(word, words, cutoff=0.8)[0]}? \
                                    Enter Y if Yes, or N if no : ")
                
            if yn == "Y":
                mycursor.execute("select meaning from meanings where word_id in (\
                select word_id from words where word=%s)", (get_close_matches(word, words, cutoff=0.8)[0], ))
                return mycursor.fetchall()
                
            elif yn=="N":
                return f"{word} word dosen't exist. Please check your input"
            else:
                return "We didn't understand your entry."
        
        else:
            return f"{word} word dosen't exist. Please check your input"



if __name__ == "__main__":
    st.title("Simple English Dictionary App")

    text_input = st.text_input("Enter some text")
    output = searchWord(text_input.lower())


    if type(output)==list:
        for row in output:
            for columns in row:
                st.write(columns)
    else:
        st.write(output)
    
    mycursor.close()
    mydb.close()