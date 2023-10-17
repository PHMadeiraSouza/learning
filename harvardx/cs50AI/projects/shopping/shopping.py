import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open(f"{filename}") as f:
        reader = csv.reader(f)
        next(reader)
        evidence = []
        label = []
        row_num = 0
        while row_num < 1:
            for row in reader:
                line = []

                line.append(int(row[0]))
                line.append(float(row[1]))
                line.append(int(row[2]))
                line.append(float(row[3]))
                line.append(int(row[4]))
                line.append(float(row[5]))
                line.append(float(row[6]))
                line.append(float(row[7]))
                line.append(float(row[8]))
                line.append(float(row[9]))
                line.append(int(month(row[10]))) 

                for cell in row[11:15]:
                    line.append(int(cell))     
                line.append(int(row[15] == "Returning_Visitor"))
                line.append(int(row[16] == 'TRUE'))

                evidence.append(line)

                label.append(int(row[17] == 'TRUE'))
                row_num += 1
    return (evidence, label)

def month(m):
    if m == "Jan":
        return 0 
    elif m == "Feb":
        return 1
    elif m == "Mar":
        return 2
    elif m == "Apr":
        return 3
    elif m == "May":
        return 4 
    elif m == "June":
        return 5
    elif m == "Jul":
        return 6
    elif m == "Aug":
        return 7
    elif m == "Sep":
        return 8
    elif m == "Oct":
        return 9
    elif m == "Nov":
        return 10
    elif m == "Dec":
        return 11
    else:
        return m



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_p = 0
    correct_n = 0

    t_n = 0
    t_p = 0
    for n in range(0, len(predictions)):
        if labels[n] == 1:
            t_p += 1
            if predictions[n] == labels[n]:
                correct_p+= 1
        if labels[n] == 0:
            t_n += 1
            if predictions[n] == labels[n]:
                correct_n+= 1

        
        else:
            t_n += 1

    return (correct_p / t_p),(correct_n / t_n)

if __name__ == "__main__":
    main()
