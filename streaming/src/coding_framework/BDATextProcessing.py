from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


class BDATextProcessing:
    @staticmethod
    def simplify_text(str_input):
        intermediate_result = word_tokenize(str_input)
        intermediate_result = BDATextProcessing.__stop_word_removal(intermediate_result)
        # intermediate_result = BDATextProcessing.__illegal_character_removal(intermediate_result)
        # First impression is that stemming is deteriorating the accuracy
        # intermediate_result = BDATextProcessing.__word_stemming(intermediate_result)
        return BDATextProcessing.__word_lemmatizing(intermediate_result)

    @staticmethod
    def __stop_word_removal(str_input):
        result = []
        stop_words = set(stopwords.words('english'))

        for word in str_input:
            if word not in stop_words:
                result.append(word)

        return result

    @staticmethod
    def __word_stemming(str_input):
        result = []
        ps = PorterStemmer()

        for word in str_input:
            result.append(ps.stem(word))

        return result

    @staticmethod
    def __word_lemmatizing(str_input):
        result = []
        lemmatizer = WordNetLemmatizer()

        for word in str_input:
            result.append(lemmatizer.lemmatize(word))

        return result

    @staticmethod
    def __illegal_character_removal(str_input):
        """
        Remove unwanted (and potential dangerous) characters from input_string

        *This method requires further work - combine letters back into respective words*
        :param str_input:
        :return:
        """
        temp_word = None
        result = []
        illegal_characters = ('\'', '&', '^', '$')
        for word in str_input:
            for letter in word:
                if letter not in illegal_characters:
                    if letter != " ":
                        temp_word += letter
                    else:
                        result.append(temp_word)
                        temp_word = None
        return result


###########################################################################
# Code usage example:
# data = "look it's hardly been 48 hours and much is still unknown but there are few things we can say for certain and this is when it actually helps to be on HBO where those things can be saved without restraint because after the many necessary and appropriate moments of Silence moment of premium cable profanity so here is where things stand first as of now we know this attack was carried out by gigantic fucking assholes unconscionable flaming ass holes possibly possibly working with other fucking All Souls definitely working in service open Audiology second I'm just saying French is going to enjoy and I'll tell you why if you were in a war of culture and lifestyle with frogs good fucking luck  bring your bankruptcy geology will bring Jean-Paul Sartre fine wine go buy cigarettes Camembert macarons proof on the fucking croquembouche  to trust you just pulled a philosophy of rigorous self-abnegation to a pastry fight my friends you are fuc  what is a French Freedom Tower  so tell the people of France all thoughts are truly with you and I do not doubt they'll be more to say on all of this as events on spool but for now we are going to continue"
# result = BDATextProcessing.simplify_text(data)
# print(result)
###########################################################################
