import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

class BDATextProcessing:
    @staticmethod
    def simplify_text(str_input):
        """
        Main callable cleaning method - ensures
        that input stream is properly formatted.
        :param str_input:
        :return:
        """
        intermediate_result = word_tokenize(str_input)
        intermediate_result = BDATextProcessing.__stop_work_removal(intermediate_result)
        # First impression is that stemming is deteriorating the accuracy
        # intermediate_result = BDATextProcessing.__word_stemming(intermediate_result)
        intermediate_result = BDATextProcessing.__word_lemmatizing(intermediate_result)
        return intermediate_result

    @staticmethod
    def __stop_work_removal(str_input):
        """
        Removes NLTK stop words from input stream
        :param str_input:
        :return: result
        """
        result = []
        stop_words = set(stopwords.words('english'))

        for word in str_input:
            if word not in stop_words:
                result.append(word)

        return result

    @staticmethod
    def __word_stemming(str_input):
        """
        Performs word stemming on input stream
        :param str_input:
        :return: result:
        """
        result = []
        ps = PorterStemmer()

        for word in str_input:
            result.append(ps.stem(word))

        return result

    @staticmethod
    def __word_lemmatizing(str_input):
        """
        Performs word lemmatization on input stream
        :param str_input:
        :return: result:
        """
        result = []
        lemmatizer = WordNetLemmatizer()

        for word in str_input:
            result.append(lemmatizer.lemmatize(word))

        return result
