import numpy as np
from keras_bert import extract_embeddings
from tensorflow.keras.models import load_model
import keras.backend.tensorflow_backend as tb

BIO_BERT_PATH = '/code/biobert_v1.1_pubmed'
TRAINED_MODEL_PATH_1 = '/code/final_model_1.h5'
TRAINED_MODEL_PATH_2 = '/code/final_model_2.h5'
TRAINED_MODEL_PATH_3 = '/code/final_model_3.h5'
TRAINED_MODEL_PATH_4 = '/code/final_model_4.h5'
TRAINED_MODEL_PATH_5 = '/code/final_model_5.h5'


def predict_cancer(file_path):
    tb._SYMBOLIC_SCOPE.value = True
    x = np.array([open(file_path, 'r').read()])
    embedding = np.array(extract_embeddings(BIO_BERT_PATH, x))
    embedding = np.mean(embedding, axis=1)

    model = load_model(TRAINED_MODEL_PATH_1)
    y_pred_1 = model.predict(embedding)
    model = load_model(TRAINED_MODEL_PATH_2)
    y_pred_2 = model.predict(embedding)
    model = load_model(TRAINED_MODEL_PATH_3)
    y_pred_3 = model.predict(embedding)
    model = load_model(TRAINED_MODEL_PATH_4)
    y_pred_4 = model.predict(embedding)
    model = load_model(TRAINED_MODEL_PATH_5)
    y_pred_5 = model.predict(embedding)

    y_pred = (y_pred_1 + y_pred_2 + y_pred_3 + y_pred_4 + y_pred_5) / 3
    cancer_prob = int(y_pred[0][0] * 100)
    return cancer_prob
