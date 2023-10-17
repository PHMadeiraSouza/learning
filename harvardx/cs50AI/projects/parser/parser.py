import nltk
import sys

from nltk.tokenize import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | VP PP | NP S | Np AdvP | PP AdvP 
AdjP -> Adj | Adj Conj AdjP
AdvP -> Adv | Conj S
NP -> N | Det NP | AdjP NP | NP PP
PP -> P | PP NP
VP -> V | VP NP | VP NP PP | AdvP VP | VP S | VP Conj VP | VP AdvP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    s = word_tokenize(sentence)
    s1 = []
    for word in s: 
        if any(c.isalpha() for c in word) == True:
            s1.append(word.lower())


    return s1



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    nps = []
    for subtree in tree.subtrees():

        if subtree.label() == "NP":
            print("subtree = ", subtree)
            subtreehassubNP = False

            for s in subtree.subtrees():
                print("s = ", s)
                if s.label() == "NP" and s != subtree:
                    subtreehassubNP = True
                    break

            if subtreehassubNP == False:
                nps.append(subtree)
        print("")
    return nps


if __name__ == "__main__":
    main()
