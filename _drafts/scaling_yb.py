import warnings

from sklearn.svm import LinearSVC, NuSVC, SVC
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression, SGDClassifier
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier

from yellowbrick.utils.timer import Timer

warnings.filterwarnings("ignore")


# Try them all!
models = [
    LinearSVC(),
    SVC(gamma='auto'),
    NuSVC(gamma='auto'),
    BaggingClassifier(),
    KNeighborsClassifier(),
    LogisticRegressionCV(cv=3),
    LogisticRegression(solver='lbfgs'),
    SGDClassifier(max_iter=100, tol=1e-3),
    MLPClassifier(alpha=1, max_iter=1000),
    ExtraTreesClassifier(n_estimators=100),
    RandomForestClassifier(n_estimators=100),
    GaussianProcessClassifier(1.0 * RBF(1.0))
]

short_list = [
    LogisticRegression(solver='lbfgs'), # simple model that scales well
    MLPClassifier(alpha=1, max_iter=1000), # complex model
    SVC(gamma='auto'), # more complex model
    GaussianProcessClassifier(1.0 * RBF(1.0)) # very complex model
]

def time_models(X, y, estimators):
    """
    Test various estimators.
    """
    fit_times = dict()
    for estimator in estimators:

        # Use Timer context manager to track fit time
        with Timer() as timer:

            # Instantiate the classification model and visualizer
            estimator.fit(X, y)  
            _ = estimator.predict(X)

            # TODO: stop execution if the fit time is greater than 15min

        fit_times[estimator.__class__.__name__] = timer.interval

    return fit_times


def time_model(X, y, estimator):
    """
    Test one estimator.
    """
    # Use Timer context manager to track fit time
    with Timer() as timer:

        # Instantiate the classification model and visualizer
        estimator.fit(X, y)  
        _ = estimator.predict(X)

    return (estimator.__class__.__name__, timer.interval)


if __name__ == "__main__":
    for model in [LogisticRegression(solver='lbfgs')]:
        for n in range(6):
            instances = 500 * 10 ** n
            for x in range(4):
                features = 5 * 10 ** x
                X, y = make_classification(n_samples=instances, n_features=features)
                name, fit_time = time_model(X, y, model)
                print("{} with {} instances, {} features: {} seconds".format(
                    name, instances, features, fit_time
                ))
        print("")

