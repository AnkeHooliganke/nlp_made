from collections import OrderedDict
from sklearn.base import TransformerMixin
from typing import List, Union
import numpy as np


EPS = 1e-4

class BoW(TransformerMixin):
    """
    Bag of words tranformer class
    
    check out:
    https://scikit-learn.org/stable/modules/generated/sklearn.base.TransformerMixin.html
    to know about TransformerMixin class
    """

    def __init__(self, k: int):
        """
        :param k: number of most frequent tokens to use
        """
        self.k = k
        # list of k most frequent tokens
        self.bow = None

    def fit(self, X: np.ndarray, y=None):
        """
        :param X: array of texts to be trained on
        """
        # task: find up to self.k most frequent tokens in texts_train,
        # sort them by number of occurences (highest first)
        # store most frequent tokens in self.bow
        # raise NotImplementedError
        vocab = set(' '.join(X).split())
        res = {word: 0 for word in vocab}
        for text in X:
          for word in text.split():
            res[word] += 1
        self.bow = sorted(res, key=lambda x: res[x], reverse=True)[:self.k]


        # fit method must always return self
        return self

    def _text_to_bow(self, text: str) -> np.ndarray:
        """
        convert text string to an array of token counts. Use self.bow.
        :param text: text to be transformed
        :return bow_feature: feature vector, made by bag of words
        """

        result = {word: 0 for word in self.bow}
        for word in text.split():
          if word in self.bow:
            result[word] += 1
        # raise NotImplementedError
        return np.array(list(result.values()), "float32")

    def transform(self, X: np.ndarray, y=None) -> np.ndarray:
        """
        :param X: array of texts to transform
        :return: array of transformed texts
        """
        assert self.bow is not None
        return np.stack([self._text_to_bow(text) for text in X])

    def get_vocabulary(self) -> Union[List[str], None]:
        return self.bow


class TfIdf(TransformerMixin):
    """
    Tf-Idf tranformer class
    if you have troubles implementing Tf-Idf, check out:
    https://streamsql.io/blog/tf-idf-from-scratch
    """

    def __init__(self, k: int = None, normalize: bool = False):
        """
        :param k: number of most frequent tokens to use
        if set k equals None, than all words in train must be considered
        :param normalize: if True, you must normalize each data sample
        after computing tf-idf features
        """
        self.k = k
        self.normalize = normalize

        # self.idf[term] = log(total # of documents / # of documents with term in it)
        self.idf = OrderedDict()

    def fit(self, X: np.ndarray, y=None):
        """
        :param X: array of texts to be trained on
        """
        # raise NotImplementedError
        N = X.shape[0]
        vocab = set(' '.join(X).split())
        # tf = {word: 0 for word in vocab}
        self.idf = {word: 0 for word in vocab}
        for text in X:
          text = text.split()
          # for word in text:
          #   tf[word] += 1
          text_set = set(text)
          for word in text_set:
            self.idf[word] += 1
        if self.k:
          keys = sorted(list(self.idf.keys()), key=lambda x: self.idf[x], reverse=True)
          self.idf = {word: self.idf[word] for i, word in enumerate(keys) if i < self.k}
        self.idf = {word: np.log(N / (self.idf[word] + 1)) for word in self.idf}


        # fit method must always return self
        return self

    def _text_to_tf_idf(self, text: str) -> np.ndarray:
        """
        convert text string to an array tf-idfs.
        *Note* don't forget to normalize, when self.normalize == True
        :param text: text to be transformed
        :return tf_idf: tf-idf features
        """
        text = text.split()
        tf = {word: 0 for word in self.idf}
        for word in text:
          if word in self.idf:
            tf[word] += 1
        
        result = [tf[word] * self.idf[word] for word in self.idf]
        if self.normalize:
          result /= (np.linalg.norm(result, axis=0, keepdims=True) + EPS)
        # raise NotImplementedError
        return np.array(result, "float32")

    def transform(self, X: np.ndarray, y=None) -> np.ndarray:
        """
        :param X: array of texts to transform
        :return: array of transformed texts
        """
        assert self.idf is not None
        return np.stack([self._text_to_tf_idf(text) for text in X])