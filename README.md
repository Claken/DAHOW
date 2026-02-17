# DAHOW - H-GENAI 2025

Welcome to the **DAHOW** project repository, presented during the **H-GENAI** **2025** **Hackathon**.

## Presentation Overview

You can view the full PDF presentation [here](https://github.com/Claken/DAHOW/blob/main/DAHOW.pdf).

---

## Description

**Projet Veolia - Optimisation de la Qualité des Données avec IA.** </br>
Ce projet vise à automatiser le contrôle de la qualité des données au sein de l’entrepôt de données de Veolia Eau France en exploitant des méthodes d’IA générative. </br>
L'objectif est de faciliter le travail des Data Engineers et Data Scientists en réduisant le temps consacré à la validation des données à grande échelle.

La solution comprend :  
✅ Une description du contexte métier et des métadonnées des données traitées.  
✅ Une génération automatisée des contrôles de qualité et des requêtes SQL associées.  
✅ Une intégration possible avec Airflow pour une exécution scalable.  
✅ Un système évolutif permettant d’affiner les contrôles et d’améliorer l’expérience utilisateur via un scoring global et une interface ergonomique.

Ce projet s'inscrit dans une démarche d’optimisation des processus de traitement des données pour assurer une meilleure prise de décision au sein de Veolia Eau France.

---

## Architecture

```mermaid
graph TD;
    A["Utilisateur (Streamlit) \n Upload d'un fichier CSV"] -->|Upload| B["AWS S3 (Raw Data) \n Stockage du fichier uploadé"];
    B -->|Analyse| C["AWS Glue - LAMBDA #1 \n - Analyse du fichier S3 \n - Extraction des schémas \n - Mise à jour du catalogue Glue"];
    C -->|Création| D["Amazon Redshift (DB) \n - Création de la base de données \n - Stockage des données"];
    D -->|Vérification| E["Détection d'Anomalies (LAMBDA #2) \n - Récupération des colonnes Redshift \n - Chargement des règles depuis S3 \n - Génération du prompt pour Bedrock"];
    E -->|Génération SQL| F["AWS Bedrock - Mistral Large (LAMBDA #3) \n - Génération de requêtes SQL pour vérifier la validité des données"];
    F -->|Exécution| G["Exécution des Requêtes SQL (Lambda) \n - Interrogation de la DB Redshift \n - Extraction des résultats"];
    G -->|Affichage| H["Reporting & Audit \n - Affichage des résultats dans Quicksight"];
```
