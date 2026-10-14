package com.example.webapp.service;

import com.example.webapp.entity.Log;
import com.example.webapp.repository.LogRepository;
import org.springframework.stereotype.Service;
import java.util.List;

/**
 * ch05/backend_springboot/.../service/LogService.java
 * 사용자 활동 이력을 기록하는 서비스.
 */
@Service
public class LogService {

    private final LogRepository logRepository;

    public LogService(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    public void record(Long memberId, String action, String target) {
        logRepository.save(new Log(memberId, action, target));
    }

    public List<Log> getRecentLogs() {
        return logRepository.findTop100ByOrderByLogIdDesc();
    }
}
