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

*TO DO*

---

## 2. Podstawy teoretyczne i stos technologiczny

### 2.1 Podstawy teoretyczne

**a) Dapr (Distributed Application Runtime)** to otwartoźródłowy framework stworzony z myślą o uproszczeniu tworzenia mikrousług. Udostępnia zestaw wbudowanych API, które ułatwiają implementację funkcjonalności niezbędnych w architekturze mikrousług, takich jak:

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

- Dapr
- OTel
- Python (Flask)
- Grafana
- Zipkin

---

## 3. Opis koncepcji studium przypadku

*TO DO*

---

## 4. Architektura rozwiązania

*TO DO*

---

## 5. Opis konfiguracji środowiska

*TO DO*

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

