# Day 13: Training, validation, testing and overfitting

## Task 1: Why a validation set exists

### Overfitting

- **Overfitting** = the model memorizes the training data (like a student who memorized last year's paper) and fails on new data.
- **Generalization** = doing well on new, unseen data. This is the real goal.
- **Underfitting** = the model learned too little; it is bad even on training data.

| Training score | Validation score | Meaning |
|---|---|---|
| 99% | 98% | Good, the model learned |
| 99% | 70% | Overfitting (big gap) |
| 60% | 58% | Underfitting |

### The 3 splits (in my words, corrected)

| Split | School example | Used for | Typical size |
|---|---|---|---|
| **Training** | Textbook + practice | The model learns from it (finds the weights). | ~70% |
| **Validation** | Mock test | Tuning: threshold, settings, choosing between models. Check its score as often as needed. | ~15% |
| **Test** | Final board exam | Only once, at the very end, to report the final score on new data. | ~15% |

### The golden rule of the test set

**Never use the test set to make decisions.** No tuning, no threshold choice, no model choice. If you look at the test score and go back to tune, the test set has "leaked" and its score can no longer be trusted (like seeing the board exam paper before the exam).

If the test score is bad: report it honestly. Do not tune on that same test set again. Get fresh test data, or redo the process with a new split.

### Q&A

**How long should I tune on validation?** Until one of these happens:

- the business target is met (for example recall ≥ 95%)
- the improvement becomes tiny (a few tries, almost no gain)
- time or budget runs out

Tuning on validation too many times can make the model memorize the validation set too. Cross-validation (Task 2) fixes this by checking on several different slices.

**New data keeps arriving. What about the test set?**

- One test set = used once per model version.
- A new model version gets a new, fresh test set (for example last month's orders).
- When the model is live, check its score on new data regularly: this is **monitoring**.
- With time-based data, always train on older data and test on newer data, so the test shows how the model does in the future.

| Months (RVO Steel example) | Use |
|---|---|
| Jan to Sep orders | Training + validation |
| Oct orders | Test set, used once |
| Nov orders | Monitoring the live model; if the score drops, build a new model and use Dec as its new test set |

### Day 12 note

On Day 12 the threshold 0.315 was chosen by looking at the test set. Strictly, that is test-set leakage: the threshold should be chosen on validation data, and the test set only used to report.
