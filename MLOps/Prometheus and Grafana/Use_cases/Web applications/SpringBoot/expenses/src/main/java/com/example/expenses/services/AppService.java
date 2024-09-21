package com.example.expenses.services;

import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.stereotype.Service;

@Service
public class AppService {

    private final MeterRegistry meterRegistry;

    public AppService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }

    public void handleRequest(boolean isSuccess) {
        // Increment custom counter for failed requests
        if (!isSuccess) {
            meterRegistry.counter("requests.failed").increment();
        }
    }
}
