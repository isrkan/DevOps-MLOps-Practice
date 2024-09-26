package com.example.expenses.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data // Lombok annotation to generate getters and setters methods
@Entity // Specifies that this class is a JPA entity and will be mapped to a database table
@AllArgsConstructor // Lombok annotation to generate a constructor with all fields as parameters
@NoArgsConstructor // Lombok annotation to generate a no-arguments constructor
public class Expense {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Double amount;
    private String category;
    private String description;
    private Boolean approved;
    private String addedBy;
}
