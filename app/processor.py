import pandas as pd


def data_processing(data):   
    df = pd.DataFrame(data)
    print(df)
    df['title_word_count'] = df['title'].apply(lambda x: len(x.split()))

    df['title_char_count'] = df['title'].apply(len)

    df['capitalized_words'] = df['title'].apply(
        lambda x: [word for word in x.split() if word[0].isupper()]
    )

    print(df[['capitalized_words']])
    return df