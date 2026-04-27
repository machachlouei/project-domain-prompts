# Data Requirements for ReAct-based Model Validation Assessment

## 1. Validation Assessment Instructions (We Already Have These)
These are the predefined assessment criteria that the model validation report needs to follow.

**Example**:  
- "Assess whether core requirements align with model objectives."
- "Evaluate if the model’s segmentation approach is appropriate for different risk groups."

📌 **Purpose:** Serves as the **primary task definition** guiding the LLM in report generation.

---

## 2. Contextual Information (Model Development Documents)
To generate meaningful validation reports, the algorithm needs relevant background data from **Model Development Documents (MDDs)**.  
These documents contain key details about the model, its objectives, assumptions, methodology, and performance metrics.

**Example Context from an MDD:**
```
- Model Name: Credit Scoring Model v2
- Model Objective: Predict customer creditworthiness based on transactional history.
- Core Requirements: Must generalize well across demographics; must avoid biases.
- Assumptions: Assumes all input features are normally distributed.
- Performance: Achieved AUC of 0.85 on historical data.
```

📌 **Purpose:** **Retrieval-Augmented Generation (RAG)** will extract relevant text sections to **feed into the prompt context**.

---

## 3. Past Model Validation Reports (Historical Data)
To improve **grounding and completeness**, providing past validation reports allows the LLM to **learn from previously written assessments**.

**Example Extract from a Historical Validation Report:**
```
- The model's segmentation approach is consistent with best practices in risk assessment.
- However, it lacks a fairness analysis to ensure no demographic group is disproportionately affected.
```

📌 **Purpose:**  
1. Helps **guide the LLM** toward structured report generation.  
2. **Supports the ReAct retrieval step**—if past reports contain similar instructions, the system can reuse relevant insights.  
3. Acts as **ground truth for evaluation** (if available).

---

## 4. Model Monitoring Reports (Risk & Performance Updates)
Post-deployment monitoring reports **track model behavior over time**. These can be used to validate whether models continue to align with regulatory and business requirements.

**Example Extract from a Model Monitoring Report:**
```
- The model’s accuracy has dropped by 3% in Q3.
- A fairness audit showed slightly higher rejection rates for applicants under 25.
- Recommended Action: Adjust feature weighting to mitigate bias.
```

📌 **Purpose:**  
- **Useful for context retrieval**: Ensures validation reports incorporate **latest model performance updates**.
- **Grounded assessment**: Helps the LLM generate **more up-to-date validation insights**.

---

## 5. Subject Matter Expert (SME) Annotations or Feedback (If Available)
If you have access to **expert-written validation reports or manual assessments**, they can serve as **high-quality benchmarks** for comparison.

📌 **Purpose:**  
- If SME-labeled data is available, it can be used for **direct comparison with LLM-generated reports**.
- Helps **calibrate the LLM-based evaluation metrics**.

---

## 6. External Guidelines & Compliance Standards
Certain validation reports must adhere to regulatory guidelines like **SR 11-7, OCC 2011-12, Basel II, IFRS 9**, etc. These compliance requirements should be available to **fact-check outputs**.

**Example Regulatory Guideline Excerpt:**
```
- A model must be independently validated before being used in production.
- Validation must cover conceptual soundness, data integrity, and model performance.
- Any material changes to the model require re-validation.
```

📌 **Purpose:**  
- Ensures **generated reports comply with regulatory expectations**.
- Can be used as **additional context** in retrieval-augmented generation (RAG).

---

## 7. Human or LLM-based Evaluation Data
For evaluating **the quality of generated validation reports**, you need **human expert ratings** or a secondary **LLM-based evaluation**.

**Example LLM-based Evaluation Output:**
```
- Relevancy: 4/5
- Hallucination: 2/5 (Moderate level of unsupported claims)
- Comprehensiveness: 5/5
- Groundedness: 3/5 (Some claims were not supported by retrieved context)
```

📌 **Purpose:**  
- Provides **quantitative evaluation metrics** to compare different prompting techniques.
- Helps refine prompts **based on automated scoring feedback**.

---

## Summary of Data Requirements

| **Data Type**                        | **Purpose**                                              | **Example** |
|--------------------------------------|---------------------------------------------------------|-------------|
| **Validation Assessment Instructions** | Defines what needs to be evaluated                     | "Assess core requirements vs. model objectives." |
| **Model Development Documents (MDDs)** | Provides key model details for evaluation              | Model assumptions, objectives, performance metrics |
| **Historical Validation Reports**    | Guides structured report writing, supports retrieval   | "Fairness analysis missing in segmentation." |
| **Model Monitoring Reports**         | Ensures reports include latest model performance data  | "AUC dropped by 3%, bias detected in feature X." |
| **SME Annotations / Expert Labels**  | Helps compare LLM-generated vs. human reports         | SME-approved validation report extracts |
| **Regulatory Guidelines**            | Ensures outputs comply with standards                 | SR 11-7, OCC 2011-12, Basel II rules |
| **Evaluation Scores (Human/LLM)**    | Measures output quality                                | "Relevancy: 4/5, Hallucination: 2/5" |

---

## Next Steps
✅ **Collect & Prepare These Data Sources** (as text, CSV, or JSON).  
✅ **Integrate a RAG system** to dynamically retrieve relevant context.  
✅ **Run experiments** to test how different prompting techniques perform using these inputs.  

---
