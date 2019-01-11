import pandas as pd
import datetime
import QK
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump, load
rf2 = load('rf_optimal.joblib') 

df_breweries = pd.read_csv("data/untappd_breweries_ratings.csv")

def simple_style(x):
    x = x.lower()
    types = ['ale', 'stout', 'porter', 'sour', 'pilsner', 'ipa', 'cider', 'wine', 'beer']
    found = False
    for a in types:
        if a in x:
            found = True
            return a
            
            
    if found == False:
        return 'other'

def clean_dataframe(df):
    df_texts = df['text']
    df.drop('text', axis=1, inplace=True)
    df['brewery'] = df['brewery'].apply(lambda x: x.split('/', 3)[-1])
    df['raters'] = df['raters'].apply(lambda x: x.split(' ', 1)[0])
    df['rating'] = df['rating'].apply(lambda x: x.strip(')'))
    df['rating'] = df['rating'].apply(lambda x: x.strip('('))
    df['ibu'] = df['ibu'].apply(lambda x: x.strip(' IBU'))
    df['abv'] = df['abv'].apply(lambda x: x.strip('% ABV'))
    df['date'] = df['date'].apply(lambda x: x.strip('Added '))
    df['date'] = pd.to_datetime(df.date)
    df['ibu'] = df['ibu'].replace('N/A', 0)
    df['abv'] = df['abv'].replace('N/', 0)
    df['rating'] = df['rating'].replace('N/A', 0)
    df['raters'] = df['raters'].apply(lambda x: x.replace(",", ""))

    for col in ['abv', 'ibu', 'rating', 'raters']:
        df[col] = df[col].astype(float)
    
    df['rating']=df['rating'].apply(lambda x: round(x,1))
    df['abv']=df['abv'].apply(lambda x: round(x,1))
    df['days_since'] = df['date'].apply(lambda x: (datetime.datetime.today()-x).days)
    df['raters_per_day'] = df['raters']/df['days_since']
    df['raters_per_day'] = df['raters_per_day'].apply(lambda x: round(x,2))

    # # uses simple_style function that can be edited based on
    # # what styles you want to make available...
    df['style'] = df['style'].apply(lambda x: simple_style(x))

    df = df[['name','style', 'abv', 'rating', 'raters', 'raters_per_day']]

    df_all_test = pd.merge(df, pd.get_dummies(df['style']), left_index=True, right_index=True)

    df_all_test['raters_per_day'] = df_all_test['raters_per_day'].replace('nan', 0)
    df_all_test['raters_per_day'] = df_all_test['raters_per_day'].replace(np.inf, 0)
    df_all_test['raters_per_day'] = df_all_test['raters_per_day'].replace(np.nan, 0)

    df_nodrop = df_all_test.copy()
    df_all_test.drop('style', axis=1, inplace=True)
    df_all_test.drop('raters', axis=1, inplace=True)
    df_all_test.drop('raters_per_day', axis=1, inplace=True)
 #   df_all_test.drop('name', axis=1, inplace=True)

    # #df_texts = df_all_test['text']
    df_texts = QK.process_data(df_texts)
    df_texts = QK.stop_stem((df_texts.apply(str)))

    all_words = QK.generate_words(df_texts)
    word_features = [i[0] for i in all_words.most_common(400)] ### was originally 400

    test_features = [QK.find_features(text, word_features) for text in df_texts]
    df_nlp = pd.merge(pd.DataFrame(df_all_test['name']),pd.DataFrame(test_features), left_index=True, right_index=True)
    try:
        df_nlp = pd.merge(df_nlp, df_nodrop, left_on = 'name_x', right_on = 'name')
    except:
        df_nlp = pd.merge(df_nlp, df_nodrop, left_on = 'name', right_on = 'name')
    
    #test
    print(df_nlp.info())
    print([col for col in df_nlp.columns if df_nlp[col].dtype=='uint8'])
    
    while (len([col for col in df_nlp.columns if df_nlp[col].dtype=='object']) > 0):
        [df_nlp.drop(col, axis=1, inplace=True) for col in df_nlp.columns if df_nlp[col].dtype=='object']

    #test
    print(df_nlp.shape)

    return df_nlp

def rf_train(cleaned_data):
    #rf = RandomForestRegressor(max_features='auto', n_estimators = 1000, random_state = 42)
    rf = RandomForestRegressor(oob_score=True, max_features='auto', n_estimators=500, min_samples_leaf = 1, n_jobs=1)
    df_train_X = cleaned_data.drop('rating', axis=1)
    df_train_y = cleaned_data['rating']
    X_train,X_test,y_train,y_test=train_test_split(df_train_X, df_train_y,test_size=0.3,random_state=3)
    rf.fit(X_train, y_train)
    # Use the forest's predict method on the test data
    predictions = rf.predict(X_test)
    # Calculate the absolute errors
    errors = abs(predictions - y_test)
    # Print out the mean absolute error (mae)
    mae = round(np.mean(errors), 2)
    print('Mean Absolute Error:', mae, 'degrees.')

    train_score=rf.score(X_train, y_train)
    test_score=rf.score(X_test, y_test)
    print("random forest train score:", train_score)
    print("random forest test score:", test_score)

    dump(rf, 'rf_optimal.joblib')
    return (train_score, test_score, mae)

def rf_optimal(cleaned_data):
    df_X = cleaned_data.drop('rating', axis=1)
    df_y = cleaned_data['rating']
    
    predictions = rf2.predict(df_X)
    # Calculate the absolute errors
    errors = abs(predictions - df_y)
    # Print out the mean absolute error (mae)
    mae = round(np.mean(errors), 2)
    print('Mean Absolute Error:', mae, 'degrees.')

    score=rf2.score(df_X, df_y)
   
    print("random forest score:", score)

    return (mae, score)


# test = pd.read_csv("data/full_brewery_data.csv")
# clean_df = clean_dataframe(test)
# print(clean_df.columns)
# rf_train(clean_df)

# test1 = pd.read_csv("data/test2.csv")
# clean_df = clean_dataframe(test1)
# rf_optimal(clean_df)

filelocation = input("Enter filename with respect to  the repository: ")
test1 = pd.read_csv(filelocation)
clean_df = clean_dataframe(test1)
rf_optimal(clean_df)

