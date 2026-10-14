package com.example.webapp.repository;

import com.example.webapp.entity.Function;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface FunctionRepository extends JpaRepository<Function, Long> {
    Optional<Function> findByFunctionCode(String functionCode);
}
