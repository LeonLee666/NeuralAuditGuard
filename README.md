# NeuralAuditGuard: A Learning-based SQL-agnostic Auditing Framework

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-green.svg)

## Overview

This repository contains the official implementation of **NeuralAuditGuard**, a novel learning-based auditing framework designed to secure database systems without relying on explicit SQL parsing. NeuralAuditGuard leverages machine learning to detect anomalous database access patterns and potential security threats in real-time.

**Paper Link**: [NeuralAuditGuard: A Learning-based SQL-agnostic Auditing Framework](https://xxx)  
**Authors**: [Liang Li, Yang Wu, Yiduo Wang, Jie Wu]


## Key Features

- **SQL-Agnostic Design**: Works across different database systems (MySQL, PostgreSQL, Oracle, etc.) without requiring SQL parsing.
- **Anomaly Detection**: Uses advanced machine learning models to identify abnormal access patterns.
- **Real-time Monitoring**: Provides instant alerts for potential security breaches.
- **Scalable Architecture**: Designed to handle high-volume transactional data.
- **Extensible Plugin System**: Easily integrate with existing security infrastructure.

## Architecture
NeuralAuditGuard consists of four main components:

1. **Data Collection Module**: Captures database access patterns without relying on SQL parsing.
2. **SQL-agnostic log preprocessing**: extracting the literal value streams from the audit log.
1. **Feature Extraction Engine**: Transforms raw access logs into machine-readable features.
1. **Anomaly Detection Model**: Employs deep learning to identify suspicious activities.
1. **Alerting & Reporting System**: Generates actionable insights and security alerts.

## Contact
For questions or support, please open an issue on GitHub or contact [lil225@chinatelecom.cn].