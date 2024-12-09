from prepro import Prepro
from exp_max import Exp_Max
import pickle as pk

if __name__ == "__main__":
    """
    pre = Prepro("Excelsior/e990517_mod.htm", "Excelsior/stopwords.txt")
    documents, vocabulary = pre.main()

    with open('files/documents.pk','wb') as handle:
        pk.dump(documents, handle, protocol=pk.HIGHEST_PROTOCOL)
    
    with open('files/vocabulary.pk','wb') as handle:
        pk.dump(vocabulary, handle, protocol=pk.HIGHEST_PROTOCOL)
    """
    with open('files/documents.pk','rb') as handle:
        documents = pk.load(handle)
    
    with open('files/vocabulary.pk','rb') as handle:
        vocabulary = pk.load(handle)

    exp_max = Exp_Max(documents, vocabulary)
    exp_max.main()
    