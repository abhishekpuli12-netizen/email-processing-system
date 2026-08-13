# MANDATORY MESSAGE IDs - DETAILED REPORT

## Summary
- **Total Mandatory Messages:** 15
- **All Present in System:** ✅ YES
- **Categories Represented:**
  - Action Required
  - General Information
  - Meeting or Event
  - Personal Information
  - Promotional

---

## Message 1: MSG_0002

**Sender:** Ishaan
**Time:** 2026-09-01 08:37:00
**Message:** `Can you review the privacy checklist before 2026-09-09?`

### Classification
- **Category:** Action Required
- **Confidence:** 0.95 (95%)
- **Reason:** The message contains action words like "please", "submit", or "complete" (found 1 matching patterns)

### Extracted Tasks/Events (1 items)
- **Type:** TASK
- **Title:** the privacy checklist
- **Deadline:** 2026-09-09
- **Time:** Not specified
- **Person:** Not specified
- **Priority:** MEDIUM

### Sensitive Information
- None detected

---

## Message 2: MSG_0007

**Sender:** Ananya
**Time:** 2026-09-01 11:42:00
**Message:** `For today: Please reply to the client email by 2026-09-04.`

### Classification
- **Category:** Action Required
- **Confidence:** 0.5 (50%)
- **Reason:** The message contains action words like "please", "submit", or "complete" (found 2 matching patterns)

### Extracted Tasks/Events (1 items)
- **Type:** TASK
- **Title:** reply to the client email
- **Deadline:** 2026-09-04
- **Time:** Not specified
- **Person:** Not specified
- **Priority:** MEDIUM

### Sensitive Information
- None detected

---

## Message 3: MSG_0001

**Sender:** Meera
**Time:** 2026-09-01 08:00:00
**Message:** `For today: Calendar update: family dinner, 2026-09-19 at 10:00, the library.`

### Classification
- **Category:** Meeting or Event
- **Confidence:** 0.77 (77%)
- **Reason:** The message includes date/time references and meeting-related keywords (found 3 matching patterns)

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 4: MSG_0003

**Sender:** Kabir
**Time:** 2026-09-01 09:14:00
**Message:** `FYI: Reminder: mentor catch-up happens on 2026-09-16 at 11:00 in the city clinic.`

### Classification
- **Category:** Meeting or Event
- **Confidence:** 0.95 (95%)
- **Reason:** The message includes date/time references and meeting-related keywords (found 1 matching patterns)

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 5: MSG_0009

**Sender:** Meera
**Time:** 2026-09-01 12:56:00
**Message:** `For my profile, my emergency contact is my brother.`

### Classification
- **Category:** Personal Information
- **Confidence:** 0.95 (95%)
- **Reason:** The message contains personal identifiers or contact information (found 1 matching patterns)

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 6: MSG_0016

**Sender:** Rohan
**Time:** 2026-09-01 17:15:00
**Message:** `Just checking—Remember that i drink coffee without sugar.`

### Classification
- **Category:** General Information
- **Confidence:** 0.5 (50%)
- **Reason:** The message does not fit specific categories - general informational content

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 7: MSG_0004

**Sender:** Aarav
**Time:** 2026-09-01 09:51:00
**Message:** `One more thing: The training material is on the portal.`

### Classification
- **Category:** General Information
- **Confidence:** 0.5 (50%)
- **Reason:** The message does not fit specific categories - general informational content

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 8: MSG_0006

**Sender:** Meera
**Time:** 2026-09-01 11:05:00
**Message:** `Important: The laptop battery is fully charged.`

### Classification
- **Category:** General Information
- **Confidence:** 0.5 (50%)
- **Reason:** The message does not fit specific categories - general informational content

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 9: MSG_0014

**Sender:** Promotions
**Time:** 2026-09-01 16:01:00
**Message:** `Can you help? Special festival discount on clothing. Use code SAVE17.`

### Classification
- **Category:** Promotional
- **Confidence:** 0.95 (95%)
- **Reason:** The message has marketing language, offers, or promotional content (found 1 matching patterns)

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 10: MSG_0015

**Sender:** Promotions
**Time:** 2026-09-01 16:38:00
**Message:** `Please note: Flash sale on laptops starts at 6 PM. Use code SAVE23.`

### Classification
- **Category:** Action Required
- **Confidence:** 0.5 (50%)
- **Reason:** The message contains action words like "please", "submit", or "complete" (found 2 matching patterns)

### Extracted Tasks/Events (1 items)
- **Type:** TASK
- **Title:** note: Flash sale on laptops starts at 6 PM
- **Deadline:** Not specified
- **Time:** Not specified
- **Person:** Not specified
- **Priority:** MEDIUM

### Sensitive Information
- None detected

---

## Message 11: MSG_0005

**Sender:** Aarav
**Time:** 2026-09-01 10:28:00
**Message:** `Hi, My home address is 42 Lake View Road, Chennai-45.`

### Classification
- **Category:** Personal Information
- **Confidence:** 0.95 (95%)
- **Reason:** The message contains personal identifiers or contact information (found 1 matching patterns)

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 12: MSG_0013

**Sender:** Meera
**Time:** 2026-09-01 15:24:00
**Message:** `One more thing: My card number is 4111 1111 1111 1111-92.`

### Classification
- **Category:** General Information
- **Confidence:** 0.5 (50%)
- **Reason:** The message does not fit specific categories - general informational content

### Extracted Tasks/Events
- None

### Sensitive Information (1 items)
- **Type:** bank_details
- **Risk Level:** HIGH
- **Masked Text:** One more thing: My card number is *******************-92.
- **Recommended Action:** do_not_send_external

---

## Message 12: MSG_0013

**Sender:** Meera
**Time:** 2026-09-01 15:24:00
**Message:** `One more thing: My card number is 4111 1111 1111 1111-92.`

### Classification
- **Category:** Sensitive Information 
- **Confidence:** 0.95 (95%) 
- **Reason:** Message contains bank_details 

### Sensitive Information (1 items)
- **Type:** bank_details
- **Risk Level:** HIGH
- **Masked Text:** One more thing: My card number is *******************-92.
- **Recommended Action:** do_not_send_external

## Message 14: MSG_0024

**Sender:** Ananya
**Time:** 2026-09-01 22:11:00
**Message:** `Just checking—I might prefer evening meetings now.`

### Classification
- **Category:** General Information
- **Confidence:** 0.5 (50%)
- **Reason:** The message does not fit specific categories - general informational content

### Extracted Tasks/Events
- None

### Sensitive Information
- None detected

---

## Message 15: MSG_0037

**Sender:** Meera
**Time:** 2026-09-02 06:12:00
**Message:** `One more thing: The review could be Friday afternoon.`

### Classification
- **Category:** Action Required
- **Confidence:** 0.95 (95%)
- **Reason:** The message contains action words like "please", "submit", or "complete" (found 1 matching patterns)

### Extracted Tasks/Events (1 items)
- **Type:** TASK
- **Title:** could be Friday afternoon
- **Deadline:** Not specified
- **Time:** Not specified
- **Person:** Not specified
- **Priority:** MEDIUM

### Sensitive Information
- None detected

---
