import sys
import pandas as pd
import itertools
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import BernoulliNB
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (alpha, fit_prior, binarize) in itertools.product([1., 5., 10., 25., 50.],
                                                      [True],
                                                      [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(MinMaxScaler(),
                            BernoulliNB(alpha=alpha,
                                        fit_prior=fit_prior,
                                        binarize=binarize))
        # 10-fold CV scores for the pipeline
        cv_scores = cross_val_score(estimator=clf, X=features, y=labels, cv=10)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'alpha={},'.format(alpha)
    param_string += 'fit_prior={},'.format(fit_prior)
    param_string += 'binarize={}'.format(binarize)

    for cv_score in cv_scores:
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'BernoulliNB',
                              param_string,
                              str(cv_score)])

        print(out_text)
        sys.stdout.flush()
