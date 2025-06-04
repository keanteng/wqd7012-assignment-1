import pandas as pd
import joblib

def get_encoding(category, value):
    encodings = {
        'person_gender': {
            'female': 0,
            'male': 1
        },
        'person_education': {
            'associate': 0,
            'bachelor': 1,
            'doctorate': 2,
            'high school': 3,
            'master': 4
        },
        'person_home_ownership': {
            'mortgage': 0,
            'other': 1,
            'own': 2,
            'rent': 3
        },
        'previous_loan_defaults_on_file': {
            'no': 0,
            'yes': 1,
            0: 0,
            1: 1
        },
        'loan_intent': {
            'debt_consolidation': 0,
            'education': 1,
            'home_improvement': 2,
            'medical': 3,
            'personal': 4,
            'venture': 5
        }
    }
    
    # Look up the encoding
    return encodings.get(category, {}).get(value, None)

def classify_loan(
        person_age: float,
        person_gender: str,
        person_education: str,
        person_income: float,
        person_emp_exp: float,
        person_home_ownership: str,
        loan_amnt: float,
        loan_intent: str,
        loan_int_rate: float,
        loan_percent_income: float,
        cb_person_cred_hist_length: float,
        credit_score: float,
        previous_loan_defaults_on_file: str
) -> dict[float, str, str, float, float, str, float, str, float, float, float, float, str | str]:
    """Set the borrower personal details for loan approval classification. (mock API).

    Args:
        person_age (float): The age of the borrower.
        person_gender: Gender of the borrower. Either `male` or `female`.
        person_education: The education level of the borrower.Either 'associate`, `bachelor`, `doctorate`, `master` or `high school`.
        person_income: The income of the borrower.
        person_emp_exp: The years of employment experience of the borrower.
        person_home_ownership: The home ownership status of the borrower. Either `mortage`, `other`, `own` or `rent`.
        loan_amnt: The amount of loan requested.
        loan_intent: The intent of the loan. Either `debt_consolidation`, `education`, `home_improvement`, `medical` or `personal`.
        loan_int_rate: The interest rate of the loan.
        loan_percent_income: The loan amount as a percentage of annual income.
        cb_person_cred_hist_length: The length of the credit history of the borrower.
        credit_score: The credit score of the borrower.
        previous_loan_defaults_on_file: The indicator of previous loan defaults. Either `yes` or `no`.

    Returns:
        A dictionary containing the loan approval status.
    """
    # make the input data into a dataframe
    input_data = {
        "person_age": person_age,
        "person_gender": person_gender,
        "person_education": person_education,
        "person_income": person_income,
        "person_emp_exp": person_emp_exp,
        "person_home_ownership": person_home_ownership,
        "loan_amnt": loan_amnt,
        "loan_intent": loan_intent, 
        "loan_int_rate": loan_int_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": cb_person_cred_hist_length,
        "credit_score": credit_score,
        "previous_loan_defaults_on_file": previous_loan_defaults_on_file
    }
    input_df = pd.DataFrame([input_data])
    print("### This is the input data:")
    print(input_df.head())
    # scale the input data
    means_stds = pd.read_csv("data/means_stds.csv")
    means_stds.set_index('column', inplace=True)
    columns = ["person_age", "person_income", "person_emp_exp", "loan_amnt",
                "loan_int_rate", "loan_percent_income", "cb_person_cred_hist_length",
                "credit_score"]
    for column in columns:
        mean = means_stds.loc[column, 'mean']
        std = means_stds.loc[column, 'std']
        input_df[column] = (input_df[column] - mean) / std

    # convert the categorical variables to class
    categorical_columns = [
        "person_gender", "person_education", "person_home_ownership",
        "loan_intent", "previous_loan_defaults_on_file"
    ]
    for column in categorical_columns:
        input_df[column] = input_df[column].apply(lambda x: get_encoding(column, x))
    
    print("### This is the processed input data: ")
    print(input_df.head())

    # load classifier at model/logistic_regression.pkl
    classifier = joblib.load("model/random_forest_model.pkl")

    # reorder the columns to match the training data
    ordered_columns = [
        "person_gender",
        "person_education",
        "person_home_ownership",
        "loan_intent",
        "previous_loan_defaults_on_file",
        "person_age",
        "person_income",
        "person_emp_exp",
        "loan_amnt",
        "loan_int_rate",
        "loan_percent_income",
        "cb_person_cred_hist_length",
        "credit_score"
    ]
    input_df = input_df[ordered_columns]

    # make prediction
    prediction = classifier.predict(input_df)

    if prediction[0] == 1:
        return "Your loan application has been approved."
    else:
        return "Your loan application has been rejected."