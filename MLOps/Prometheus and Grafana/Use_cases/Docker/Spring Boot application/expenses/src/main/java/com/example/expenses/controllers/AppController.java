package com.example.expenses.controllers;

import com.example.expenses.services.AppService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppController {
    private final AppService appService;

    public AppController(AppService appService) {
        this.appService = appService;
    }

    @GetMapping("/process")
    public String processRequest(@RequestParam boolean isSuccess) {
        appService.handleRequest(isSuccess);
        return isSuccess ? "Request processed successfully!" : "Request failed!";
    }
}
