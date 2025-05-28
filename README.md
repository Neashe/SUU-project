# Dokumentacja projektu Dapr - OTel

**Autorzy:**  
- Natalia Adamiak 
- Miron Czech  
- Kacper Kotkiewicz  
- Małgorzata Krupanek

**Grupa:** 2
**Rok:** 2025  

---

## Spis treści

1. [Wprowadzenie](#1-wprowadzenie)  
2. [Podstawy teoretyczne i stos technologiczny](#2-podstawy-teoretyczne-i-stos-technologiczny)  
3. [Opis koncepcji studium przypadku](#3-opis-koncepcji-studium-przypadku)  
4. [Architektura rozwiązania](#4-architektura-rozwiązania)  
5. [Opis konfiguracji środowiska](#5-opis-konfiguracji-środowiska)  
6. [Metoda instalacji](#6-metoda-instalacji)  
7. [Jak odtworzyć projekt – krok po kroku](#7-jak-odtworzyć-projekt--krok-po-kroku)  
   - [Podejście Infrastructure as Code](#71-podejście-infrastructure-as-code)  
8. [Kroki wdrożenia demonstracyjnego](#8-kroki-wdrożenia-demonstracyjnego)  
   - [Konfiguracja środowiska](#81-konfiguracja-środowiska)  
   - [Przygotowanie danych](#82-przygotowanie-danych)  
   - [Procedura wykonawcza](#83-procedura-wykonawcza)  
   - [Prezentacja wyników](#84-prezentacja-wyników)  
9. [Wykorzystanie AI w projekcie](#9-wykorzystanie-ai-w-projekcie)  
10. [Podsumowanie – wnioski](#10-podsumowanie--wnioski)  
11. [Bibliografia / Referencje](#11-bibliografia--referencje)  

---

## 1. Wprowadzenie

Celem projektu jest stworzenie prostego systemu monitoringu aplikacji webowej opartej na FastAPI, z wykorzystaniem metryk eksportowanych za pomocą OpenTelemetry (OTEL), zbieranych przez OpenTelemetry Collector, a następnie wizualizowanych w Grafanie poprzez Prometheus. Projekt demonstruje jak zintegrować Dapr z FastAPI i OTEL, aby monitorować wydajność i zachowanie aplikacji w kontenerach Docker.

---

## 2. Podstawy teoretyczne i stos technologiczny

### 2.1 Podstawy teoretyczne

**a) Dapr (Distributed Application Runtime)** to open-source framework stworzony z myślą o uproszczeniu tworzenia mikrousług. Udostępnia zestaw wbudowanych API, które ułatwiają implementację funkcjonalności niezbędnych w architekturze mikrousług, takich jak:

- komunikacja między usługami,
- zarządzanie stanem,
- obsługa zdarzeń,
- orkiestracja workflow.

Dzięki temu programiści mogą skupić się na logice biznesowej, zamiast na implementacji skomplikowanej logiki infrastrukturalnej.

Nowoczesne systemy mikrousługowe muszą być nie tylko funkcjonalne, ale też odporne na błędy i łatwe do monitorowania. W tym celu Dapr integruje się z **OpenTelemetry (OTel)** – otwartym standardem służącym do zbierania danych telemetrycznych z aplikacji rozproszonych.

**b) OpenTelemetry** to projekt rozwijany przez Cloud Native Computing Foundation (CNCF), który standaryzuje sposób zbierania i przesyłania danych telemetrycznych, takich jak:

- **Traces (śledzenie)** – dane opisujące przepływ żądań między komponentami systemu, pomocne w analizie wydajności i błędów,
- **Metrics (metryki)** – liczby opisujące stan aplikacji i infrastruktury (np. czas odpowiedzi, liczba żądań, użycie zasobów),
- **Logs (logi)** – tekstowe zapisy zdarzeń występujących w systemie.

Dzięki OTel dane mogą być eksportowane do różnych narzędzi monitorujących i analizujących, takich jak Prometheus, Grafana czy Jaeger, co pozwala uzyskać pełen obraz działania systemu.

**c) Obserwowalność z użyciem Dapr i OTel**

Dapr automatycznie generuje dane telemetryczne i przekazuje je zgodnie ze standardem OpenTelemetry. Ułatwia to monitorowanie systemu bez konieczności ręcznej integracji narzędzi do logowania, metryk i śledzenia zapytań.


---

### 2.2 Stos technologiczny

- FastAPI — nowoczesny framework do tworzenia API w Pythonie.

- Dapr — framework do budowania aplikacji mikroserwisowych z funkcjami takimi jak obserwowalność.

- OpenTelemetry (OTEL) — zestaw SDK do zbierania metryk i śledzeń.

- OpenTelemetry Collector — pośrednik odbierający metryki/traces i eksportujący je do Prometheusa.

- Prometheus — system do monitoringu i alertowania oparty na metrykach.

- Grafana — narzędzie do wizualizacji i analizy danych metrycznych.

- Docker Compose — orkiestracja kontenerów.

---

## 3. Opis koncepcji studium przypadku

Studium przypadku przedstawia prostą aplikację FastAPI działającą w kontenerze z instrumentacją OTEL do generowania metryk. Metryki są eksportowane do OpenTelemetry Collector, który przetwarza dane i eksponuje je jako endpoint Prometheusa. Prometheus scrapuje metryki z OTEL Collectora, a Grafana wizualizuje je na dashboardzie. Dapr jest użyty do wspierania zarządzania konfiguracją i integracji OTEL.

---

## 4. Architektura rozwiązania

Jokes to aplikacja zbudowana w architekturze mikroserwisowej, umożliwiająca anonimowe przeglądanie, ocenianie oraz rankingowanie żartów i memów. Składa się z sześciu niezależnych serwisów:

- Content Service – zarządza bazą żartów i memów oraz udostępnia je losowo lub w formie rankingu.

- Rating Service – umożliwia użytkownikom ocenianie treści (np. pozytywnie lub negatywnie) i przechowuje dane o głosach.

- Ranking Service – generuje listę najlepiej ocenianych treści na podstawie danych z Rating Service.

- Stats Service – zbiera podstawowe statystyki, takie jak liczba ocen dziennie lub liczba przeglądanych treści.

- Content Delivery Service – odpowiada za serwowanie obrazków memów, jeśli są przechowywane lokalnie lub w chmurze.

- Frontend Gateway – pełni rolę API Gateway i pośrednika pomiędzy frontendem a mikroserwisami, agregując dane w jednolitym formacie.

Wszystkie serwisy komunikują się między sobą za pośrednictwem REST API. Aplikacja nie wymaga logowania ani kont użytkowników – działa całkowicie anonimowo.

Poniżej zaprezentowano diagram architektury:
![Diagram architektury](diagram.png)

---

## 5. Opis konfiguracji środowiska

Środowisko składa się z następujących komponentów działających w kontenerach Docker, połączonych w jedną wspólną sieć:

- FastAPI z Dapr – aplikacja webowa, która realizuje logikę biznesową oraz integruje się z Dapr. Dapr automatycznie zbiera metryki runtime oraz udostępnia API do wysyłania własnych metryk.

- OpenTelemetry Collector (OTEL Collector) – odbiera metryki (w tym niestandardowe) z aplikacji i Dapr, przetwarza je i przekazuje dalej.

- Prometheus – system monitorowania i zbierania metryk, który scrapuje metryki z OTEL Collectora.

- Grafana – narzędzie do wizualizacji danych, które pobiera metryki z Prometheusa i pozwala na tworzenie dashboardów.

Wszystkie usługi działają w jednej sieci Docker, dzięki czemu mogą się ze sobą komunikować za pomocą nazw kontenerów jako hostów.

### Schemat komunikacji

```
[FastAPI + Dapr] --(metryki OTLP)--> [OpenTelemetry Collector] --(scrape)--> [Prometheus] --> [Grafana]
          \                                          /
           \------(metryki runtime Dapr)------------/

```

- FastAPI wysyła własne metryki do OTEL Collectora przez protokół OTLP gRPC.

- Dapr eksportuje swoje metryki runtime do OTEL Collectora.

- OTEL Collector agreguje metryki i udostępnia je na endpointzie HTTP, który jest scrappowany przez Prometheusa.

- Grafana łączy się z Prometheusem i wyświetla dane w formie wykresów i dashboardów.

---

## 6. Metoda instalacji

*TO DO*

---

## 7. Jak odtworzyć projekt – krok po kroku

*TO DO*

### 7.1 Podejście Infrastructure as Code

*TO DO*

---

## 8. Kroki wdrożenia demonstracyjnego

### 8.1 Konfiguracja środowiska

*TO DO*

### 8.2 Przygotowanie danych

*TO DO*

### 8.3 Procedura wykonawcza

*TO DO*

### 8.4 Prezentacja wyników

*TO DO*

---

## 9. Wykorzystanie AI w projekcie

*TO DO*

---

## 10. Podsumowanie – wnioski

*TO DO*

---

## 11. Bibliografia / Referencje

*TO DO*

---

