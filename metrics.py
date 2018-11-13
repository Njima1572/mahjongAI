import numpy as np

def mjMetrics(y_labels, predicted):

    errors = np.absolute(np.subtract(y_labels, predicted))
    errors_sum = np.sum(errors)
    score = errors_sum / (len(y_labels) * 6)
    return 1 - score
        
