# DAHOW - H-GENAI 2025

Welcome to the **DAHOW** project repository, presented during the **H-GENAI** **2025** **Hackathon**.

## Presentation Overview

You can view the full PDF presentation [here](./assets/DAHOW.pdf).

---

## Description

Projet Veolia - Optimisation de la Qualité des Données avec IA
Ce projet vise à automatiser le contrôle de la qualité des données au sein de l’entrepôt de données de Veolia Eau France en exploitant des méthodes d’IA générative. L'objectif est de faciliter le travail des Data Engineers et Data Scientists en réduisant le temps consacré à la validation des données à grande échelle.

La solution comprend :  
✅ Une description du contexte métier et des métadonnées des données traitées.  
✅ Une génération automatisée des contrôles de qualité et des requêtes SQL associées.  
✅ Une intégration possible avec Airflow pour une exécution scalable.  
✅ Un système évolutif permettant d’affiner les contrôles et d’améliorer l’expérience utilisateur via un scoring global et une interface ergonomique.

Ce projet s'inscrit dans une démarche d’optimisation des processus de traitement des données pour assurer une meilleure prise de décision au sein de Veolia Eau France.

---

## Architecture

```
                     +-------------------------------------------------+
                     |   🖥 Utilisateur (Streamlit)                    |
                     |   Upload d'un fichier CSV                      |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   ☁ AWS S3 (Raw Data)                           |
                     |   Stockage du fichier uploadé                   |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   🏗 AWS Glue - LAMBDA #1                        |
                     |   - Analyse du fichier S3                       |
                     |   - Extraction des schémas                      |
                     |   - Mise à jour du catalogue Glue               |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   🏛 Amazon Redshift (DB)                        |
                     |   - Création de la base de données              |
                     |   - Stockage des données                        |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   🧐 Détection d'Anomalies (LAMBDA #2)           |
                     |   - Récupération des colonnes Redshift          |
                     |   - Chargement des règles depuis S3             |
                     |   - Génération du prompt pour Bedrock           |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   🤖 AWS Bedrock - Mistral Large (LAMBDA #3)    |
                     |   - Génération de requêtes SQL pour vérifier la |
                     |     validité des données                        |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   🔍 Exécution des Requêtes SQL (Lambda)        |
                     |   - Interrogation de la DB Redshift             |
                     |   - Extraction des résultats                    |
                     +-------------------------------------------------+
                                       |
                                       v
                     +-------------------------------------------------+
                     |   📊 Reporting & Audit                          |
                     |   - Affichage des résultats dans Quicksight     |
                     +-------------------------------------------------+
```