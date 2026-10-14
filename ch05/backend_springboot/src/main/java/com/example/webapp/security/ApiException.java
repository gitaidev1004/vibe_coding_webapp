package com.example.webapp.security;

import org.springframework.http.HttpStatus;

/**
 * ch05/backend_springboot/.../security/ApiException.java
 * 상태 코드와 메시지를 함께 담아 던지는 공통 예외 클래스.
 */
public class ApiException extends RuntimeException {
    private final HttpStatus status;

    public ApiException(String message, HttpStatus status) {
        super(message);
        this.status = status;
    }

    public HttpStatus getStatus() { return status; }
}
