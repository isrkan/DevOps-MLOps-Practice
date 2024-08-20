import argparse
from customer_churn_predictor import customer_churn_predictor
from customer_churn_predictor import pipeline

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Run the customer churn prediction pipeline.")
    parser.add_argument('--data_path', type=str, required=True, help="Path to the CSV data file.")
    parser.add_argument('--config_path', type=str, help="Optional path to a custom configuration file.")

    # Parse arguments
    args = parser.parse_args()

    # Initialize the churn predictor with optional custom config path
    if args.config_path:
        churn_predictor = customer_churn_predictor.CustomerChurnPredictor(config_path=args.config_path)
    else:
        churn_predictor = customer_churn_predictor.CustomerChurnPredictor()

    # Run the pipeline
    pipeline.run_pipeline(churn_predictor.config, data_path=args.data_path)

if __name__ == "__main__":
    main()