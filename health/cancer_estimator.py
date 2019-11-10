import numpy as np
from keras_bert import extract_embeddings
from tensorflow.keras.models import load_model
import keras.backend.tensorflow_backend as tb


BIO_BERT_PATH = '/code/biobert_v1.1_pubmed'
TRAINED_MODEL_PATH = '/code/model_problem.h5'


def predict_cancer(file_path):

    tb._SYMBOLIC_SCOPE.value = True
    x = np.array([open(file_path, 'r').read()])
    embedding = np.array(extract_embeddings(BIO_BERT_PATH, x))
    embedding = np.mean(embedding, axis=1)
    model = load_model(TRAINED_MODEL_PATH)
    y_pred = model.predict(embedding)
    cancer_prob = int(y_pred[0][0]*100)
    return cancer_prob
