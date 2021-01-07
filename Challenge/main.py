import numpy as np
import pandas as pd
from random import randint
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
from scipy import sparse
from sklearn.metrics.pairwise import linear_kernel

#####
##
## DATA IMPORT
##
#####

# Where data is located
movies_file = './data/movies.csv'
users_file = './data/users.csv'
ratings_file = './data/ratings.csv'
predictions_file = './data/predictions.csv'
submission_file = './data/submission.csv'

# Read the data using pandas
movies_description = pd.read_csv(movies_file, delimiter=';', dtype={'movieID': 'int', 'year': 'int', 'movie': 'str'},
                                 names=['movieID', 'year', 'movie'])
users_description = pd.read_csv(users_file, delimiter=';',
                                dtype={'userID': 'int', 'gender': 'str', 'age': 'int', 'profession': 'int'},
                                names=['userID', 'gender', 'age', 'profession'])
ratings_description = pd.read_csv(ratings_file, delimiter=';',
                                  dtype={'userID': 'int', 'movieID': 'int', 'rating': 'int'},
                                  names=['userID', 'movieID', 'rating'])
predictions_description = pd.read_csv(predictions_file, delimiter=';', names=['userID', 'movieID'])


#####
##
## COLLABORATIVE FILTERING
##
#####

def predict_collaborative_filtering(movies, users, ratings, predictions):
    # users x movies matrix
    utility_matrix = np.zeros((len(users), len(movies)))

    # populate utility matrix with ratins
    for i in ratings.itertuples():
        utility_matrix[i[1] - 1, i[2] - 1] = i[3]

    # calculate similarity matrix using pearson correlation coefficient

    # we first calculate the average movie rating per user
    mean_user_ratings = np.average(utility_matrix, axis=1, weights=(utility_matrix > 0))[:, np.newaxis]

    # we normalize the ratings by subtracting the average if rating > 0
    ratings_diff = np.where(np.array(utility_matrix > 0), utility_matrix - mean_user_ratings, 0)

    # similarity matrix for users using cosine similarity
    user_similarity = pairwise_distances(ratings_diff, metric='cosine')

    # prediction_matrix
    pred = np.zeros((len(users), len(movies)))

    # collaborative filtering using knn algorithm

    # total = ratings_diff.shape[0] * ratings_diff.shape[1]
    # p = 0
    #
    # for i in range(ratings_diff.shape[0]):
    #     top_k_users = [np.argsort(user_similarity[:, i])[:-20 - 1:-1]]
    #     for j in range(ratings_diff.shape[1]):
    #         pred[i, j] = user_similarity[i, :][top_k_users].dot(ratings_diff[:, j][top_k_users])
    #         pred[i, j] /= np.sum(np.abs(user_similarity[i, :][top_k_users]))
    #         p += 1
    #     print('Progress: {:4.2f}%'.format(p / total * 100))
    # pred = mean_user_ratings + pred

    # collaborative filtering without knn algorithm
    pred = mean_user_ratings + user_similarity.dot(ratings_diff) / np.sum(np.abs(user_similarity), axis=1)[:,
                                                                   np.newaxis]

    # result matrix for submission
    result = np.zeros((len(predictions), 2), dtype=int)

    count = 0

    # populate result matrix with rounded predictions
    for row in predictions.itertuples():
        result[count, 0] = count + 1
        result[count, 1] = int(round(pred[row[1] - 1, row[2] - 1], 0))
        count += 1

    return result


#####
##
## LATENT FACTORS
##
#####

def predict_latent_factors(movies, users, ratings, predictions):
    ## TO COMPLETE

    pass


#####
##
## FINAL PREDICTORS
##
#####

def predict_final(movies, users, ratings, predictions):
    ## TO COMPLETE

    pass


def predict_randoms(movies, users, ratings, predictions):
    number_predictions = len(predictions)

    return [[idx, randint(1, 5)] for idx in range(1, number_predictions + 1)]


##########################################
# MAIN FUNCTION


### TESTING


#####
##
## SAVE RESULTS
##
#####


###################################
## commented out for later


## //!!\\ TO CHANGE by your prediction function

# predict collaborative filtering
predictions = predict_collaborative_filtering(movies_description, users_description, ratings_description,
                                              predictions_description)

# Save predictions, should be in the form 'list of tuples' or 'list of lists'
with open(submission_file, 'w') as submission_writer:
    # Formates data
    predictions = [map(str, row) for row in predictions]
    predictions = [','.join(row) for row in predictions]
    predictions = 'Id,Rating\n' + '\n'.join(predictions)

    # Writes it dowmn
    submission_writer.write(predictions)

print("end")
