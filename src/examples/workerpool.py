"""Worker pool implementation with Python's multiprocessing module."""
from multiprocessing import Pool
from time import time, sleep

from sklearn.metrics import accuracy_score
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_breast_cancer


def train_model(max_iter: int) -> SGDClassifier:
    """train_model.

    Train a Stochastic Gradient Descent model with the Breast Cancer
    dataset provided by Sklearn.

    Arguments
    ----------
    max_iter : int
        The maximum number of iterations for the model.

    Returns
    -------
    SGDClassifier : The trained model.

    Examples
    --------
    >>> train_model(200,)
    SGDClassifier(max_iter=200)
    """
    data, target = load_breast_cancer(return_X_y=True)
    clf = SGDClassifier(max_iter=max_iter)
    clf.fit(data, target)
    predictions = clf.predict(data)
    print(
        f"Iterations: {max_iter},",
        f"Accuracy: {accuracy_score(target, predictions)}",
    )
    sleep(5)
    return clf


def run_workerpool_tasks() -> float:
    """run_workerpool_tasks.

    A Workerpool of three process is created to train SGD Classifier models.
    The pool handle three process at time and once completed a place is
    released to handle another process. 10 trainings are performed.

    Returns
    -------
    float : The time ellapsed to perform the trainings.

    Examples
    --------
    >>> run_workerpool_tasks()
    Iterations: 110, Accuracy: 0.9156414762741653
    Iterations: 100, Accuracy: 0.9156414762741653
    ...
    Total: 20.110503435134888 seconds
    """
    begin = time()
    with Pool(3) as pool:
        pool.map(train_model, list(range(100, 200, 10)))
    end = time()
    total = end - begin
    print(f"Total: {total} seconds")
    return total


if __name__ == "__main__":
    print(run_workerpool_tasks())
