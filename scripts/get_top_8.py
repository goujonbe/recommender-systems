"""
@author: alessandro
"""
from time import time
import sys
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
from pyspark import SparkContext

#path_merged = '/Users/alessandro/Desktop/pfe/formated/merged_data.csv'
#path_sample_20M = '/Users/alessandro/Desktop/pfe/samples/samples20M/sample0.csv'

sc = SparkContext()



def get_ratings (user_ID, path_merged):
    '''
    Récupère, dans le dataset complet, un RDD contenant uniquement les tuples (movieID, userID, ratings) pour l'utilisateur user_ID.
    '''

    t0 = time()
    merged_raw_data = sc.textFile(path_merged)

    merged_raw_data_header = merged_raw_data.take(1)[0]

    merged_ratings_data = merged_raw_data.filter(lambda line: line!=merged_raw_data_header).map(lambda line: line.split(",")).map(lambda tokens: (tokens[1],tokens[2],tokens[3])).cache()

    user_ratings_RDD = merged_ratings_data.filter(lambda x: x[1] == user_ID)
    #print(user_ratings_RDD.collect())
    tt = time() - t0
    print('User({}) ratings got in {}'.format(user_ID, round(tt,3)))    


    return user_ratings_RDD



def loadRDD (path_sample_20M):
    '''
    Charge un échantillon du dataset complet path_sample_20M comprenant 20M de lignes prises aléatoirement.
    '''
    t0 = time()
    sample_20_raw_data = sc.textFile(path_sample_20M)

    sample_20_raw_data_header = sample_20_raw_data.take(1)[0]
 
    sample_20_RDD = sample_20_raw_data.filter(lambda line: line!=sample_20_raw_data_header).map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1],tokens[2])).cache()
    tt = time() - t0
    print('Sample loaded in {} seconds'.format(round(tt,3)))
    
    return sample_20_RDD



def remove_user_ratings (sample_20_raw_data, user_ID):
    '''
    Enlève de l'échantillon de 20M les tuples de l'utilisateur user_ID.
    '''
    with_user_ratings_RDD = loadRDD(sample_20_raw_data)
    sample_20_sin_user_ratings_RDD = with_user_ratings_RDD.filter(lambda x: x[1] != user_ID)
    return sample_20_sin_user_ratings_RDD




def add_user_ratings (user_ratings_RDD, sample_20_sin_user_ratings_RDD):
    '''
    Ajoute les tuples de l'utilisateur user_ID, présents dans le dataset complet, dans l'échantillon de 20M.
    '''
    training_RDD = sample_20_sin_user_ratings_RDD.union(user_ratings_RDD)
   
    return training_RDD



def train_model (training_RDD):
    '''
    Entraîne le model à partir de l'échantillon de 20M comprenant l'ensemble des notes de l'utilisateur user_ID.
    '''
    iterations = 10
    regularization_parameter = 0.1
    best_rank = 12

    t0 = time()
    model_trained = ALS.train(training_RDD, best_rank, iterations=iterations, lambda_=regularization_parameter)
    tt = time() - t0
    print('New model trained in {} seconds'.format(round(tt,3)))

    return model_trained



def get_movies_unrated (sample_20_sin_user_ratings_RDD):
    '''
    Recupère uniquement les movie_ID dont le films n'a pas été noté par l'utilisateur user_ID.
    '''
    t0 = time()

    # sample_20_sin_user_ratings_filtred_RDD.filter(lambda x: x[1])
    unrated_movie_RDD = sample_20_sin_user_ratings_RDD.map(lambda x: (x[1], user_ID)).distinct()
    print('There is {} different movies in the sample of 20M rows.'.format(unrated_movie_RDD.count()))
    tt = time() - t0
    print('Computed in {} seconds'.format(round(tt,3)))
    
    return unrated_movie_RDD



def get_predictions (model_trained, unrated_movie_RDD):
    '''
    Prédit les recommandations pour l'utilisateur user_ID à partir du modèle entrainé model_trained sous la forme ((__,__),__).
    '''
    t0 = time()
    user_recommendations_RDD = model_trained.predictAll(unrated_movie_RDD).map(lambda r: ((r[0], r[1]), r[2]))
    tt = time() - t0
    print('Predictions compute in {} seconds'.format(round(tt,3)))
    return user_recommendations_RDD



def extract_top_8 (user_recommendations_RDD):
    '''
    Extrait un top des films recommandés 
    '''
    user_recommendations_sorted_RDD = user_recommendations_RDD.sortBy(lambda x: -x[1]).takeOrdered(20)
    final_movie_ID_recommendations = [recommendation[0][0] for recommendation in user_recommendations_sorted_RDD]
    print('Final recommendations : ')
    print(final_movie_ID_recommendations)
    return final_movie_ID_recommendations



if __name__ == '__main__':
    user_ID = sys.argv[1]
    path_merged = sys.argv[2]
    path_sample_20M = sys.argv[3]
    
    t0 = time()

    extract_top_8(get_predictions(train_model(add_user_ratings(get_ratings(user_ID, path_merged), remove_user_ratings(path_sample_20M, user_ID))), get_movies_unrated(remove_user_ratings(path_sample_20M, user_ID))))
    
    tt = time() - t0
    print('Top 8 recommendations executed in {} seconds'.format(round(tt,3)))

# [6, 7,  8, 10, 25, 33, 42, 59, 79, 83, 87, 94,  97, 116, 126, 130, 131, 133, 134, 142] ==> 1488844
# [7, 8, 10, 25, 33, 42, 59, 79, 83, 87, 94, 97, 116, 126, 130, 131, 133, 134, 142, 149] ==> 6
# [6, 7, 8, 10, 25, 33, 42, 59, 79, 83, 87, 94, 97, 116, 126, 130, 131, 133, 134, 142] ==> 970031
# [6, 7, 8, 10, 25, 33, 42, 59, 79, 83, 87, 94, 97, 116, 126, 130, 131, 133, 134, 142] ==> 1037088
# [6, 7, 8, 10, 25, 33, 42, 59, 79, 83, 87, 94, 97, 116, 126, 130, 131, 134, 142, 149] ==> 1037088