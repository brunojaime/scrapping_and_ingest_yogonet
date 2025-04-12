import pandas as pd


def data_processing(data):   
    df = pd.DataFrame([data])
    df['title_word_count'] = df['Title'].apply(lambda x: len(x.split()))

    df['title_char_count'] = df['Title'].apply(len)

    df['capitalized_words'] = df['Title'].apply(
        lambda x: [word for word in x.split() if word[0].isupper()]
    )

    print(df[['Title', 'title_word_count', 'title_char_count', 'capitalized_words',"Image_URL","Kicker"]])