package com.example.expenses.controllers;

import com.example.expenses.models.Expense;
import com.example.expenses.repositories.ExpenseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class ExpenseController {

    @Autowired
    private ExpenseRepository expenseRepository;

    @GetMapping("/expenses")
    public String home(Model model) {
        model.addAttribute("expenses", expenseRepository.findAll());
        return "expenses";
    }

    @GetMapping("/add-expense")
    public String showAddExpenseForm(Model model) {
        model.addAttribute("expense", new Expense());
        return "add-expense";
    }

    @PostMapping("/add-expense")
    public String addExpense(@ModelAttribute Expense expense) {
        expenseRepository.save(expense);
        return "redirect:/expenses";
    }
}
