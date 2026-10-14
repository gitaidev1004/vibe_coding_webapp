package com.example.webapp;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * ch05/backend_springboot/src/test/java/com/example/webapp/MemberApiTests.java
 * 회원가입, 로그인, 접근제어가 의도대로 동작하는지 검증하는 통합 테스트.
 * (FastAPI/Flask의 test_member.py, test_access_control.py와 동일한 시나리오)
 *
 * 실행: mvn test
 * 이 책의 실습 환경은 Maven Central 접근이 제한되어 있어 직접 실행하지는
 * 못했지만, Spring Boot 3.x의 표준 테스트 문법을 따른다.
 */
@SpringBootTest
@AutoConfigureMockMvc
class MemberApiTests {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void signupSuccess() throws Exception {
        mockMvc.perform(post("/api/members")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"hong_gildong\",\"password\":\"pass1234\",\"email\":\"hong@example.com\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void loginWithWrongPasswordReturns401() throws Exception {
        mockMvc.perform(post("/api/members")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"hong2\",\"password\":\"pass1234\",\"email\":\"hong2@example.com\"}"));

        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"hong2\",\"password\":\"wrong\"}"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void generalMemberCannotAccessAdminApi() throws Exception {
        mockMvc.perform(post("/api/members")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"hong3\",\"password\":\"pass1234\",\"email\":\"hong3@example.com\"}"));

        String loginResponse = mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"username\":\"hong3\",\"password\":\"pass1234\"}"))
                .andReturn().getResponse().getContentAsString();
        String token = loginResponse.split("\"token\":\"")[1].split("\"")[0];

        mockMvc.perform(get("/api/members").header("Authorization", "Bearer " + token))
                .andExpect(status().isForbidden());
    }

    @Test
    void noTokenReturns401() throws Exception {
        mockMvc.perform(get("/api/members"))
                .andExpect(status().isUnauthorized());
    }
}
