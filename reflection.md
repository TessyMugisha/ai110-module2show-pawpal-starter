# PawPal+ Project Reflection

## 1. System Design
Track completed tasks
See all pets and perform CRUD operations
Have a daily plan and availability

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design includes four classes: User, Pet, Task, and DailyPlan.
- What classes did you include, and what responsibilities did you assign to each?
User is responsible for representing the pet owner. It holds their name, how much time they have available, and their preferences. It handles logging in and out of the app.

Pet holds all the information about an animal — its name, species, age, and care needs like feeding schedule or walk frequency. It can return its care needs and update its own info.

Task represents a single care action like a walk, feeding, or medication. It belongs to a specific pet and tracks the task type, how long it takes, its priority, and whether it's been completed. It can be marked complete or updated.

DailyPlan is responsible for the scheduling logic. It holds the date, the owner's available time, and the list of tasks for the day. It generates the plan, displays it, and explains why certain tasks were chosen.

**b. Design changes**

- Did your design change during implementation?
yes
- If yes, describe at least one change and why you made it.
Originally, DailyPlan was its own separate thing with no connection to the User. I updated it so the plan knows who the owner is, which lets it pull the owner's available time automatically when generating the schedule. Without that link, the plan had no way to know how much time the owner actually had that day.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler detects conflicts only by exact time match (e.g., two tasks both set to "09:00"). It does not check whether task durations overlap — for example, a 30-minute task at 08:00 and a 10-minute task at 08:15 would not be flagged as a conflict even though they overlap in real time.

- Why is that tradeoff reasonable for this scenario?
For a daily pet care planner, most tasks are discrete events (feed, walk, meds) that owners do one at a time. Exact time matching catches the most common scheduling mistake — accidentally assigning two things to the same slot — without adding complexity. Duration-overlap detection would require tracking start and end times for every task, which is more logic than this use case needs right now.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
