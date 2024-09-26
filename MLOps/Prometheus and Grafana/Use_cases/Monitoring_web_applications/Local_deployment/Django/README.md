# Monitoring a Django application with Prometheus

In this guide, we will walk through how to monitor a Django application using Prometheus.

**Prerequisites**: Before starting, ensure:
- A Django application running locally or on a server.
- Prometheus installed and running on our system.

### Step 1: Update the Django application for Prometheus
To enable Prometheus to monitor our Django app, we will need to integrate **django-prometheus**. This library exposes Django metrics in a format Prometheus can scrape.

Follow these steps to prepare the Django app to expose metrics:
1. **Install dependencies**: Add the `django-prometheus` package to the Django project by running the following command:
    ```bash
    pip install django-prometheus
    ```
    
    We should add the following line to our `requirements.txt` file if we are managing dependencies there. For example:
    ```txt
    django-prometheus==2.3.1
    ```

    Replace `2.3.1` with the version we are using.

2. **Update Django settings**: In our `settings.py` file, update the configuration to include `django-prometheus` middleware and apps.

    1. **Add `django-prometheus` to `INSTALLED_APPS`:**

    ```python
    INSTALLED_APPS = [
        # other apps...
        'django_prometheus',
    ]
    ```

    2. **Add `django-prometheus` middleware** to capture request and response metrics:

    ```python
    MIDDLEWARE = [
        'django_prometheus.middleware.PrometheusBeforeMiddleware',
        # other middleware...
        'django_prometheus.middleware.PrometheusAfterMiddleware',
    ]
    ```

    3. **Database monitoring**: If we use Django's ORM, we can monitor our database with `django-prometheus` by adding database backends. In `settings.py`, configure the database backend for Prometheus metrics.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django_prometheus.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

    This works similarly for other supported databases like MySQL or SQLite (replace the backend accordingly). The actual storage of our data will not change. Our application will continue to connect to the same SQL database using the same credentials. The change in `ENGINE` does not affect where or how the data is stored — it only enhances the database engine with the ability to expose monitoring metrics to Prometheus.
    4. **Configure Prometheus metrics endpoint:** By default, django-prometheus exposes metrics at `/metrics/`. Add the URL route in our `urls.py` file to expose this endpoint:

    ```python
    from django.urls import path, include

    urlpatterns = [
        # other URLs...
        path('prometheus/', include('django_prometheus.urls')),
    ]
    ```

    With this configuration, Prometheus will be able to scrape metrics from `http://localhost:8003/prometheus/metrics/`.

3. **Run database migrations**: To finalize the setup for django-prometheus, run the database migrations that django-prometheus requires:
    ```bash
    python manage.py migrate
    ```

    This command applies migrations for django-prometheus, which enables monitoring for the Django ORM and database.

### Step 2: Run the Django application
Start the Django application using the `runserver` command. Once the app is running, we should be able to access the `prometheus/metrics/` endpoint to verify that Prometheus metrics are being exposed.

```bash
python manage.py runserver
```

Now, visit `http://localhost:8003/prometheus/metrics/` in the browser. We should see a list of metrics in Prometheus format, which will include default Django metrics such as request count, response time, and database queries.

### Step 3: Configure Prometheus to scrape Django metrics
Prometheus needs to be configured to scrape the metrics exposed by the Django app.

1. **Configure Prometheus**: Open the `prometheus.yml` file in the Prometheus installation directory and add a job to scrape our Django app. Add the following under the `scrape_configs` section:
    ```yaml
    global:
    scrape_interval: 15s

    scrape_configs:
    - job_name: 'django-app'
        scrape_interval: 10s
        metrics_path: '/prometheus/metrics'
        static_configs:
        - targets: ['localhost:8003']
    ```

    - **scrape_interval**: How often Prometheus scrapes the metrics from the Django app.
    - **job_name**: A name for this scrape job (e.g., `django-app`).
    - **metrics_path**: The endpoint where Prometheus will scrape the metrics (`/prometheus/metrics`).
    - **targets**: The hostname and port where the Django app is running (e.g. `localhost:8003`).

2. **Start Prometheus**: Run Prometheus locally using the command:
    ```bash
    prometheus --config.file=path/to/prometheus.yml --web.enable-lifecycle
    ```

    Once Prometheus is running, if we make changes to the `prometheus.yml` file, we can reload the configuration without restarting the server. We can do this by running:
    ```bash
    Invoke-RestMethod -Uri http://localhost:9090/-/reload -Method Post
    ```

    Prometheus will now start scraping the metrics exposed by the Django app. We can verify this by visiting the Prometheus UI at:
    ```
    http://localhost:9090
    ```

    Navigate to the **Targets** page (`http://localhost:9090/targets`) to see if Prometheus is successfully scraping the Django app.

---

## Default metrics exposed by Django
By default, django-prometheus exposes a set of metrics for monitoring various aspects of the Django application. These metrics can be categorized into several groups:

1. **Request metrics**: These metrics track HTTP requests handled by our Django application.
- **`django_http_requests_total_by_view_transport_method_total`**: Total number of HTTP requests received, grouped by view, transport (e.g., http), and method (GET, POST, etc.).
- **`django_http_requests_latency_seconds_by_view_method`**: Latency of HTTP requests, measured in seconds, grouped by view and method.
- **`django_http_requests_before_middlewares_total`**: Total number of HTTP requests before middleware processing.

2. **Database metrics**: Monitor the performance and health of database queries.
- **`django_db_execute_total`**: Total number of database queries executed.
- **`django_db_query_duration_seconds`**: Time taken to execute database queries.

3. **Cache metrics**: Monitor cache usage if the Django app uses a caching backend.
- **`django_cache_get_total`**: Total number of cache GET requests.
- **`django_cache_hits_total`**: Total number of cache hits.
- **`django_cache_misses_total`**: Total number of cache misses.

---

## Add Custom Metrics (Optional)
Sometimes the default metrics exposed by django-prometheus are not enough, and we may want to add custom metrics specific to our business logic. We can create custom metrics in Django using **Prometheus’ client library**. First, install the Prometheus Python client:
```bash
pip install prometheus-client
```

Now, we'll add custom metrics inside our Django views or other parts of the application where specific events or actions happen. For example, we will track request processing time with a histogram. A histogram allows us to track how long certain operations take, such as how long it takes to process a request.

1. **Open the views file**: open the file where the view is located. For example, the path might be: `myapp/views.py`
2. **Add a histogram to measure request time**: In this file, import the Prometheus client and define a **Histogram** metric. We will wrap the view with a decorator to track how long it takes to process a request. Here’s an example:
   ```python
   from prometheus_client import Histogram
   from django.http import HttpResponse

   # Create a Histogram to track request processing time
   request_processing_time = Histogram('request_processing_seconds', 'Time spent processing a request')

   @request_processing_time.time()  # This decorator measures the time spent in this view
   def my_view(request):
       # Simulate request processing
       return HttpResponse("Request processed.")
   ```

   In this case, every time `my_view` is called, the time it takes to execute is automatically recorded by the `request_processing_seconds` histogram.
3. **View custom metrics in Prometheus**: Once we have added our custom metrics, We can query them in Prometheus. For example, if we added a histogram for request processing time, we can query it in Prometheus with:
    ```promql
    request_processing_seconds
    ```

    Open the browser and go to:
    ```
    http://localhost:8003/prometheus/metrics
    ```
    
    We should see our custom metrics like `request_processing_seconds` included in the list of metrics.

---

## Visualize metrics in Grafana
Grafana offers a more advanced and user-friendly way to visualize metrics. To visualize metrics in Grafana:
  1. Install Grafana and connect it to Prometheus.
  2. Create dashboards with panels displaying key metrics such as `django_http_requests_total_by_view_transport_method_total`, `django_db_execute_total`, and more.
  3. We can also set up alerts based on metrics, e.g., alert when request latency is too high.