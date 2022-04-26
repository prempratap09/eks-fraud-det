from flask import Flask, jsonify, request

from file_utils import load_pickle_data
from s3_utils import read_csv_on_s3_into_dataframe, \
    write_dataframe_to_csv_in_s3


app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predicts whether the transaction is fraud or not
    """

    body = request.get_json()
    print(body)

    s3_bucket = body["s3_bucket_name"]
    test_data_file = body["test_data_filename"]
    predictions_file = body["predictions_filename"]

    # Loading test data from AWS s3
    test_df = read_csv_on_s3_into_dataframe(
        s3_bucket,
        test_data_file,
    )

    # Loading model
    model = load_pickle_data("model.pkl")

    # Predicting on test data
    predictions = model.predict(test_df)

    # Save predictions
    test_df['Class'] = predictions

    write_dataframe_to_csv_in_s3(
        test_df,
        s3_bucket,
        predictions_file,
    )

    return jsonify({
            "predictions": str(predictions),
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0")
