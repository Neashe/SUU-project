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

Monitoring i obserwowalność aplikacji to kluczowe elementy utrzymania i optymalizacji współczesnych systemów rozproszonych. OpenTelemetry to otwarty standard i zestaw narzędzi do zbierania metryk, logów i śledzeń (traces), które można eksportować do różnych systemów backendowych. Prometheus jest popularnym systemem do przechowywania i zapytań metryk w formie czasowych szeregów danych. Grafana służy do wizualizacji tych metryk na interaktywnych dashboardach.

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

- Aplikacja FastAPI — generuje i eksponuje metryki OTEL.

- Dapr — konfiguruje eksport metryk i śledzeń z aplikacji do OTEL Collector.

- OpenTelemetry Collector — odbiera metryki OTLP, przetwarza i udostępnia je w formacie Prometheus.

- Prometheus — zbiera metryki z OTEL Collectora.

- Grafana — łączy się z Prometheusem i wyświetla wykresy metryk.

Wszystkie usługi uruchomione są jako kontenery w Docker Compose, współdzieląc sieć, aby mogły się wzajemnie komunikować.

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

