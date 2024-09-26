# Monitoring an ML model

Monitoring an ML model is critical for ensuring that it operates correctly and continues to perform well after deployment. We can divide the monitoring into **functional level monitoring** and **operational level monitoring**. 

#### Prerequisites:
- **Prometheus**: For time-series data collection and monitoring.
- **Grafana**: For visualizing the data collected by Prometheus.
- **Web framework** such as Flask or FastAPI: For deploying the machine learning model.
  
### 1. **Functional level monitoring**
Functional monitoring focuses on tracking the health and performance of the ML model in relation to the problem it is trying to solve. This involves monitoring the following key aspects:
1. **Model drift** (Changes in model performance over time) - Model drift occurs when the model's performance deteriorates because the statistical properties of the target variable change over time. This can happen due to real-world conditions shifting (e.g., changing customer behavior, seasonal trends).
    - **What to monitor**: Track performance metrics such as accuracy, precision, recall, and F1 score. Compare these metrics over time with the original performance during training. 
    - **Example**: A credit card fraud detection model that was trained on last year's data might experience model drift as consumer spending patterns change due to economic shifts.
    - **How to detect**: If the model’s accuracy on recent predictions is significantly lower than on training or validation data, model drift could be occurring.
2. **Data drift** (Changes in the input data distribution) - Data drift refers to changes in the distribution of input features that were used to train the model. If the characteristics of incoming data deviate from the data on which the model was trained, the model may struggle to make accurate predictions.
    - **What to monitor**: Track the statistical properties of key input features, such as mean, variance, min, and max. We can also use tests like Kullback-Leibler divergence or Jensen-Shannon divergence to compare the distribution of incoming data with the training data.
    - **Example**: In a weather prediction model, if the average temperature (an input feature) starts showing significantly higher values due to climate change, the model might experience data drift.
    - **How to detect**: Compare the current input data distribution with historical data. Significant changes indicate that the model is receiving different data than it was trained on.
3. **Prediction drift** (Change in model predictions over time) - Prediction drift occurs when the distribution of the model's outputs (predictions) shifts over time, regardless of whether the input data has changed.
    - **What to monitor**: Track metrics such as prediction entropy or the class distribution (for classification models). Monitor how the model’s predictions are distributed over time and compare them with the expected distribution.
    - **Example**: A customer churn model might show prediction drift if, over time, the percentage of customers predicted to churn increases dramatically even though external factors haven’t changed.
    - **How to detect**: If we see that the proportion of predictions for a certain class or outcome is changing abnormally (e.g., one class becomes dominant), it may indicate prediction drift.
4. **Concept drift** (Changes in the relationship between input and output) - Concept drift happens when the relationship between the model's input features and the target variable changes over time. Unlike data drift, where the input data changes, concept drift means that the same input no longer leads to the same output as before.
    - **What to monitor**: Compare predictions with real-world outcomes (ground truth) using metrics like sliding-window accuracy (performance on recent data) and the change in precision or recall over time.
    - **Example**: A loan approval model might experience concept drift if the criteria for approving loans change (e.g., due to new regulations), but the model isn’t retrained to reflect these changes.
    - **How to detect**: Continuously monitor real-world outcomes (such as customer feedback or confirmed correct predictions). If actual outcomes differ significantly from the model’s predictions, concept drift could be the issue.
5. **Data quality** (Issues with incoming data) - Poor data quality can severely affect model performance, even if the model itself hasn’t drifted. Data quality issues include missing values, incorrect formats, or unexpected outliers in the data.
    - **What to monitor**: Track for missing values, outliers, invalid types, or anomalies in incoming data. Monitor the percentage of invalid or incomplete data points.
    - **Example**: In a real-time product recommendation system, if a significant portion of incoming customer data is missing key attributes (such as browsing history), the model's performance will degrade.
    - **How to detect**: Set up alerts for invalid or missing data inputs. If the rate of such occurrences increases, there may be issues with the data pipeline or upstream systems.

### 2. **Operational level monitoring**
Operational monitoring ensures the system's health and stability from a technical perspective. It focuses on infrastructure, the application hosting the ML model and performance metrics.
1. **Latency** (How long predictions take)
    - **What to monitor**: Track the request/response latency for model predictions, using metrics like p95 and p99 latency (the 95th and 99th percentile response times). Also, monitor the time it takes to load the model during server start-up.
    - **Example**: If our model serves real-time predictions in a web app, a noticeable increase in latency (e.g., predictions taking more than 500ms) can negatively impact user experience.
    - **How to detect**: Track latency over time. Spikes in latency may indicate server issues, inefficient code, or resource contention.
2. **Throughput** (Request rate)
    - **What to monitor**: Monitor the number of prediction requests processed over time, usually measured in requests per second (RPS).
    - **Example**: For a news website recommendation model, a sudden increase in request rates might occur during peak hours, putting stress on the system.
    - **How to detect**: If the system struggles to handle higher request volumes, we may need to scale the infrastructure.
3. **Error rates** (Failed predictions or system errors)
    - **What to monitor**: Track errors returned by the model or service, such as HTTP error codes (500 for server errors, 404 for not found) or model-related exceptions (e.g., errors during inference). Monitor the number of failed prediction attempts.
    - **Example**: A NLP model might fail if it encounters unexpected input, causing spikes in 500 errors.
    - **How to detect**: Monitor for abnormal increases in errors. If error rates spike, it could indicate issues with the model, input data, or infrastructure.
4. **CPU and memory usage**
    - **What to monitor**: Track the system’s CPU, GPU, and memory usage to ensure the model server isn’t over-utilizing resources.
    - **Example**: A deep learning model deployed for image recognition might consume increasing amounts of GPU and memory as traffic increases, potentially causing performance issues.
    - **How to detect**: Monitor resource consumption over time. If CPU, GPU, or memory usage consistently approaches 100%, this may indicate a need for optimization or horizontal scaling.
5. **Disk I/O and network latency**
    - **What to monitor**: Track disk usage, I/O rates, and network latency to ensure data is being read from and written to storage efficiently. Network latency can also affect API request times if the model interacts with remote services.
    - **Example**: A model that reads large datasets from disk might experience slow prediction times if disk I/O is a bottleneck, while high network latency can slow down model responses when interacting with external APIs.
    - **How to detect**: Set thresholds for acceptable disk and network latency levels. If exceeded, this could indicate a bottleneck in the system’s I/O or network communication.