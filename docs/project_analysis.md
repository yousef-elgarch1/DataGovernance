# 📊 Rapport d'Analyse Globale - DataSentinel (v2.0)

Ce rapport fournit une analyse détaillée et honnête de l'état actuel du projet "DataGovProjetFederateur", basé sur l'audit du code source, de l'historique Git et de l'infrastructure.

## 1. ANALYSE GLOBALE DES FONCTIONNALITÉS

| Fonctionnalité                      | Fichiers / Microservices Concernés           | État           | Branche Git                        |
| :---------------------------------- | :------------------------------------------- | :------------- | :--------------------------------- |
| **Authentification (JWT/RBAC)**     | `services/auth-serv/`                        | Réalisée       | `auth-serv`                        |
| **Taxonomie PII/SPI**               | `services/taxonomie-serv/`, `taxonomie.json` | Réalisée       | `feature/taxonomy-mongodb-storage` |
| **Détection PII/SPI (Presidio)**    | `services/presidio-serv/`                    | Réalisée       | `main`                             |
| **Nettoyage de Données**            | `services/cleaning-serv/`                    | Réalisée       | `main`                             |
| **Classification ML**               | `services/classification-serv/`              | À améliorer    | `youssef_nisrine`                  |
| **Validation Humaine (Annotation)** | `services/annotation-serv/`                  | Réalisée       | `main`                             |
| **Correction Intelligente**         | `services/correction-serv/`                  | Réalisée (Reg) | `main`                             |
| **Score Qualité ISO 25012**         | `services/quality-serv/`                     | Réalisée       | `main`                             |
| **Masquage EthiMask**               | `services/ethimask-serv/`                    | Réalisée       | `main`                             |
| **Orchestration (Airflow)**         | `airflow/dags/`                              | Réalisée       | `feature/atlas-airflow-fix`        |
| **Gouvernance (Atlas/Ranger)**      | `atlas_integration/`, `ranger_integration/`  | En cours       | `integration-atlas`                |

---

## 2. DÉTAIL PAR FONCTIONNALITÉ (TECH BRIEF)

### 🧹 SERVICE 4: CLEANING-SERV

- **Endpoints**: `/upload`, `/profile/{id}`, `/clean/{id}`, `/clean/{id}/auto`.
- **Outliers**: Méthode **IQR** (Interquartile Range) : $Q1 - 1.5 \times IQR$ et $Q3 + 1.5 \times IQR$.
- **Profiling**: Logiciel **custom (Pandas)**, pas de library externe type ydata-profiling détectée dans le code.
- **Interface**: Intégrée au dashboard principal (affichage des colonnes supprimées/corrigées).

### 🧠 SERVICE 5: CLASSIFICATION-SERV

- **Modèle**: Utilise `distilbert-base-uncased-finetuned-sst-2-english`. **CamemBERT/FlauBERT ne sont pas présents** dans le code actuel.
- **Classes**: 7 catégories (Identity, Contact, Financial, Medical, Professional, Technical, Other).
- **Entraînement**: Modèle HuggingFace pré-entraîné utilisé tel quel avec un système de scoring par mots-clés en complément.

### 📝 SERVICE 6: ANNOTATION-SERV

- **Workflow**: `Task Creation -> Assignment -> Labeling -> Steward Review`.
- **Kappa de Cohen**: Mentionné comme placeholder/mock (0.82) dans le code, n'est pas encore calculé dynamiquement.
- **Storage**: MongoDB collection `tasks`.
- **Interface**: Interface HTML simple présente dans le service.

### 🔧 SERVICE 7: CORRECTION-SERV

- **Modèle T5**: **Absent du code**. Utilise un moteur de règles YAML (`standardize_phone_ma`, `standardize_date`, etc.).
- **Règles**: Format téléphone (+212), lowercase email, titlecase noms, range âge (0-150).
- **Validation**: Humaine requise sauf si `auto_apply=True`.

### 📊 SERVICE 8: QUALITY-SERV

- **ISO 25012**:
  - **Accuracy**: Valeurs numériques positives.
  - **Completeness**: Ratio non-null.
  - **Consistency**: Start Date < End Date.
  - **Validity**: Regex Email/Phone MA.
  - **Uniqueness**: Détection doublons.
  - **Timeliness**: Frécheur < 5 ans.
- **Score Global**: Moyenne pondérée (Accuracy 0.25, Completeness 0.20, etc.).

### 🔒 SERVICE 9: ETHIMASK-SERV

- **Techniques**:
  - **Redaction**: Masquage partiel (ex: `+212 6*****89`).
  - **Hashing**: SHA-256.
  - **Encryption**: TenSEAL (Homomorphe) si installé, sinon fallback SHA.
  - **Generalization**: Tranches d'âge (30-49) ou tranches de salaire.
- **Rôles**:
  - **ADMIN**: Pas de masque.
  - **STEWARD**: Pseudonymisation.
  - **LABELER**: Suppression (Full mask).
- **Privacy Différentielle**: **Absent du code**.

---

## 3. INFRASTRUCTURE & ARCHITECTURE

- **Nginx**: Port **8000**, reverse proxy pour les 9 services.
- **MongoDB**: Une seule instance, collections multiples (`tasks`, `audit_logs`, `quality_reports`, `inconsistencies`).
- **Airflow**: 2 DAGs (`data_pipeline.py`, `data_processing_pipeline.py`).
- **Atlas/Ranger**: Structure présente mais intégration qualifiée de "En cours" car désactivée si les serveurs ne répondent pas.

---

## 4. PROCHAINES ÉTAPES (VRAIES)

1.  **Implémentation réelle** du Kappa de Cohen pour la validation.
2.  **Intégration T5** pour les corrections textuelles avancées (si réellement souhaité).
3.  **Support CamemBERT/FlauBERT** pour le NLP français.
4.  **Differential Privacy** pour les exports statistiques anonymisés.
