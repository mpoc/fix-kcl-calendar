FROM gradle:6.7.1 AS builder

WORKDIR /src/fix-kcl-calendar
COPY . .
RUN gradle fatJar

FROM openjdk:16-alpine
COPY --from=builder /src/fix-kcl-calendar/build/libs/fix-kcl-calendar-all.jar /src/fix-kcl-calendar/

ENTRYPOINT ["java", "-jar", "/src/fix-kcl-calendar/fix-kcl-calendar-all.jar"]
