import nltk
import sys
import os
import math
from nltk.tokenize import word_tokenize

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(directory, filename),encoding="utf8" ) as f:
            content = f.read()
            files[filename] = content
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    d = word_tokenize(document)
    d1 = []
    for word in d: 
        import string
        if word.lower() not in string.punctuation and word.lower() not in nltk.corpus.stopwords.words("english"):
            d1.append(word.lower())
    return d1


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    for document in documents:
        for word in documents[document]:
            frequency = 0
            if word in idfs.keys():
                continue
            for document1 in documents:
                if word in documents[document1]:
                        frequency += 1
            idfs[word] = math.log(len(documents) / frequency)
    idfs = dict(sorted(idfs.items(), key=lambda item: item[1], reverse = True))
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filesrank = dict()
    for filename in files:
        for word in query:
            if word in files[filename]:
                try:
                    filesrank[filename] += idfs[word] * files[filename].count(word)
                except KeyError:
                    filesrank[filename] = idfs[word] * files[filename].count(word)
                    
    filesrank = dict(sorted(filesrank.items(), key=lambda item: item[1], reverse = True))
    filesrank = [f for f in filesrank]
    return filesrank[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    Srank = dict()
    for sentence in sentences:
        _idfs_ = 0
        qw = 0
        for word in query:
            if word in sentences[sentence]:
                qw += 1
                _idfs_ += idfs[word] 

        if qw > 0: 
            qtd = qw / len(sentences[sentence])
            Srank[sentence] = _idfs_, qtd
    
    Srank = dict(sorted(Srank.items(), key=lambda sentence: (sentence[1][0], sentence[1][1]), reverse = True))
    Srank = [f for f in Srank]
    return Srank[:n]


if __name__ == "__main__":
    main()
