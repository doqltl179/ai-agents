---
id: spring-boot
title: Spring Boot
kind: framework
applies_to: []
related: [java, kotlin, sql, docker]
volatility: volatile
reviewed: 2026-10-09
sources: ["https://docs.spring.io/spring-boot/index.html", "https://docs.spring.io/spring-framework/reference/", "https://github.com/spring-projects/spring-boot/wiki", "https://spring.io/projects/spring-boot#support"]
---

# Spring Boot

## Detect
- Build tool: `mvnw` with `pom.xml` (Maven) or `gradlew` with `build.gradle(.kts)` (Gradle). Always run the wrapper.
- Boot version from `spring-boot-starter-parent`, the BOM, or the `org.springframework.boot` plugin; Java version from `java.version` or the Gradle toolchain.
- Stack from starters: `web` (Spring MVC) or `webflux` (reactive), `data-jpa`, `security`, `validation`, `actuator`.
- Language: Java or Kotlin sources under `src/main/`.
- Config: `application.yml`/`.properties`, profile files `application-<profile>.*`, and `@ConfigurationProperties` classes.
- Schema migrations: Flyway (`db/migration`) or Liquibase changelogs.
- Tests: JUnit 5, Mockito, AssertJ, Testcontainers.

## Conventions
- Use constructor injection with `final` fields; a single constructor needs no `@Autowired`. No field injection.
- Layer controller, service, repository. Controllers map HTTP to DTOs; never expose JPA entities in API responses.
- Bind configuration to typed `@ConfigurationProperties` classes (records allowed) annotated `@Validated`, instead of scattered `@Value`.
- Put `@Transactional` on public service methods that form one use case; mark query-only methods `readOnly = true`.
- Validate request DTOs with `@Valid` and Bean Validation annotations; map exceptions to responses in one `@RestControllerAdvice`, returning `ProblemDetail` (RFC 9457).
- Map `@ManyToOne` and `@OneToOne` with `fetch = FetchType.LAZY` (their JPA default is eager); load what a use case needs with `JOIN FETCH`, `@EntityGraph`, or DTO projections.
- Set `spring.jpa.open-in-view=false` so lazy loading cannot leak into the web layer.
- Change schemas only through Flyway or Liquibase; keep `spring.jpa.hibernate.ddl-auto` at `validate` or `none` outside throwaway local databases.
- Expose only the `health` and `info` actuator endpoints publicly; secure the rest.
- In WebFlux code never block an event-loop thread (JDBC, `block()`, `Thread.sleep`).

## Verify
- `commands.test` (`./mvnw test` or `./gradlew test`); `commands.build` (`./mvnw verify` or `./gradlew build`).
- Use test slices: `@WebMvcTest` with `MockMvc` for controllers, `@DataJpaTest` for repositories, `@SpringBootTest` only for full integration, Testcontainers for a real database.

## Pitfalls
- N+1 queries from lazy associations read in loops or during JSON serialization; fetch in the query and confirm with SQL logging.
- `LazyInitializationException` outside a transaction; fetch the data in the query instead of enabling open-in-view or `enable_lazy_load_no_trans`.
- `@Transactional` on a private method, or called from the same class, bypasses the proxy and has no effect; call it through another bean.
- Checked exceptions do not trigger rollback by default; declare `rollbackFor` or throw unchecked exceptions.
- Lombok `@Data` on entities generates `equals`/`hashCode`/`toString` over all fields, triggering lazy loads and recursion; use `@Getter`/`@Setter` and write `equals`/`hashCode` explicitly.
- Bidirectional associations serialized by Jackson recurse infinitely; return DTOs.
- `@SpringBootTest` for every test makes the suite slow; use the narrowest slice.

## Version Notes
- Spring Boot 3.x requires Java 17+ and uses Jakarta EE namespaces (`jakarta.*`, not `javax.*`) (as of 2026-10, per the Boot 3.0 release notes).
- `@MockBean`/`@SpyBean` are deprecated since Boot 3.4 in favor of `@MockitoBean`/`@MockitoSpyBean`; `spring.threads.virtual.enabled=true` enables virtual threads on Java 21+ (Boot 3.2+) (as of 2026-10, per the Boot release notes).
- Spring Boot 4.0 is built on Spring Framework 7; follow the Boot 4.0 migration guide before applying 3.x examples to a 4.x project (as of 2026-10, per the Boot wiki).
