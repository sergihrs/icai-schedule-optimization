# 🧠 ICAI Time Schedule Optimization

This project focuses on optimizing the weekly class schedule for the **Mathematical Engineering and Artificial Intelligence degree** at ICAI. The degree includes:

- 🎓 **3 academic years**
- 👥 **5 student groups**
  - Year 1 and 2: 2 groups each
  - Year 3: 1 group

The aim is to generate a feasible and efficient timetable that meets all academic and logistical requirements.

---

## 📌 Problem Overview

### ✅ Hard Constraints

1. **CTC (Complete Teacher Capacity)**  
   Ensures each subject is assigned the correct number of teachers per group:
   $$
   \sum_{t} x = \text{TN}_{gs} \cdot \gamma_{gdhs} \quad \forall g,d,h,s
   $$

2. **NSD & EOO (Non-Subject Duplication & Early or Overnight Constraints)**  
   A group can only have one subject per time slot, and only within allowed hours:
   $$
   \sum_{s,t} x \cdot \frac{1}{\text{TN}_{gs}} = \text{A}_{gh} \quad \forall g,d,h
   $$

3. **SHR, T2S, CTA (Subject Hour Requirement, Teacher Specialty, Teacher Availability)**  
   Classes must be taught by qualified teachers during their available hours:
   $$
   \sum_{d,h,t} x \cdot \text{TS}_{st} \cdot \text{TA}_{tdh} = \text{HS}_{s} \cdot \text{TN}_{gs} \quad \forall g,s
   $$

4. **NTC (No Teacher Cloning)**  
   A teacher cannot teach multiple classes at the same time:
   $$
   \sum_{g,s} x \leq 1 \quad \forall d,h,t
   $$

5. **TCP (Teacher Consistency Principle)**  
   Teachers must teach all sessions of a subject for a group, or none:
   $$
   \sum_{d,h} x = \text{H}_{s} \cdot \zeta_{gst} \quad \forall g,s,t
   $$

6. **NCO (No Class Overflow)**  
   Lab space limitations are respected:
   $$
   \sum_{g,s,t} x \cdot \frac{\text{Q}_{cgs}}{\text{TN}_{gs}} \leq \text{L}_{c} \quad \forall c,d,h
   $$

7. **NSA (No Subject Abuse)**  
   A group can't have more than two hours of the same subject in one day:
   $$
   \sum_{h,t} x \leq 2 \cdot \text{TN}_{gs} \quad \forall g,d,s
   $$

8. **NHS (No Holes in Subject)**  
   Double sessions of the same subject must be consecutive:
   $$
   \sum_{t} x_{h+1} - \sum_{t} x_{h} \leq \delta'_{gdhs} \cdot \text{TN}_{gs} \\
   \sum_{t} x_{h+1} - \sum_{t} x_{h} \geq -\delta''_{gdhs} \cdot \text{TN}_{gs} \\
   \sum_{h}\delta'_{gdhs} + \delta''_{gdhs} \leq 2  \quad \forall g,d,s
   $$

---

### 🎯 Objective Function (Soft Constraints)

We aim to **minimize teacher dissatisfaction** by penalizing undesired time slots:

- **CTP (Checking Teacher Preferences)**  
  $$
  \min_x \sum_{g,d,h,s,t} x_{gdhst} \cdot \text{TP}_{dht}
  $$

---

## ⚙️ Model Details

- 📚 **Modeling Tool**: `ConcreteModel` from the **Pyomo** Python library.
![Model Diagram](/assets/model.png)
- 🧮 **Coefficient Statistics**:  
  ![Coefficient Stats](/assets/coef_stats.png)
- ⏱️ **Model Loading Time**: 4.3 seconds

---

## 🚀 Solver Performance

- 🔧 Initial attempts with **GLPK** proved too slow.
- ✅ Final solver: **Gurobi**
- ⏱️ **Solve Time**: 4.95 seconds
- 📉 **Optimality Gap**: 0.0% — exact optimal solution found.

<img src="/assets/gurobi_results.png" alt="Gurobi Results" width="600px">

---

## 📬 Summary

This schedule optimization model ensures:

- Full curriculum compliance 📘
- Teacher qualification and availability ✅
- Physical and time-space feasibility 🏫⏰
- Consideration of teacher preferences 🙋‍♂️

The result is a **robust, fair, and efficient schedule** for ICAI's Mathematical Engineering and Artificial Intelligence program.

---
