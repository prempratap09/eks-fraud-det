import pickle


def pickle_data(
        data,
        filename,
):
    """
    create pickle file
    """
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_pickle_data(filename):
    """
    Loads data from pickle file
    """
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    return data
