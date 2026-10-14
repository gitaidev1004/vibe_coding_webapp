package com.example.webapp.repository;

import com.example.webapp.entity.Log;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface LogRepository extends JpaRepository<Log, Long> {
    List<Log> findTop100ByOrderByLogIdDesc();
}
