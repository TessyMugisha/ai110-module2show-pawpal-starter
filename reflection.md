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
The scheduler considers three main constraints: how much time the owner has available that day (in minutes), the priority of each task (high, medium, or low), and whether a task is actually due on the plan date based on its frequency. If tasks have an optional HH:MM time assigned, that also affects the order they appear in the plan.

- How did you decide which constraints mattered most?
Available time came first because no matter how important a task is, it can't happen if the owner doesn't have time for it. Priority came second because within the time budget, some care (like medication) matters more than others (like grooming). Due date came third because there's no point scheduling a weekly task that was just done yesterday.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler detects conflicts only by exact time match (e.g., two tasks both set to "09:00"). It does not check whether task durations overlap — for example, a 30-minute task at 08:00 and a 10-minute task at 08:15 would not be flagged as a conflict even though they overlap in real time.

- Why is that tradeoff reasonable for this scenario?
For a daily pet care planner, most tasks are discrete events (feed, walk, meds) that owners do one at a time. Exact time matching catches the most common scheduling mistake — accidentally assigning two things to the same slot — without adding complexity. Duration-overlap detection would require tracking start and end times for every task, which is more logic than this use case needs right now.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI across every phase — brainstorming class responsibilities during UML design, generating class skeletons, fleshing out method logic, writing tests, and updating the Streamlit UI. It was also helpful for explaining unfamiliar syntax before I added it to the codebase.

- What kinds of prompts or questions were most helpful?
The most useful prompts were specific and gave context about what already existed. For example, asking "based on my four classes, how should the Scheduler retrieve tasks from the Owner's pets?" gave a much better answer than just asking "how do I build a scheduler." Asking "explain this test before I save it" was also useful for building understanding rather than just copying code.

- Which Copilot features were most effective for building your scheduler?
Agent mode (chat) was the most effective because I could describe what I wanted in plain language and get back working code that fit my existing structure. Inline docstring generation saved time on documentation. Asking for edge case suggestions for testing also surfaced things I would have missed on my own.

- Give one example of an AI suggestion you rejected or modified.
When asked how to simplify the sort in `generate_plan`, AI suggested replacing the lambda with `operator.attrgetter("priority", "duration", "description")`. It's slightly more Pythonic, but the lambda version is more readable for someone new to the codebase — you can see exactly what's being compared without knowing what `attrgetter` does. I kept the lambda.

- How did using separate chat sessions for different phases help you stay organized?
Starting a new session for testing kept the conversation focused. When context builds up from earlier phases, AI starts making assumptions based on old code. A fresh session with just the current file meant suggestions were grounded in what the code actually looked like at that point, not what it looked like two refactors ago.

- What did you learn about being the "lead architect" when collaborating with AI?
AI is fast at generating code but it doesn't know what matters to you. It will add features you didn't ask for, suggest abstractions that are overkill for the problem, and occasionally make things more complex in the name of being "correct." The job of the lead architect is to take what's useful, push back on what isn't, and keep the design grounded in the actual requirements. The decisions about what to include, what to simplify, and when something is "done enough" always came from me — AI just made getting there faster.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When AI suggested using `attrgetter` to sort tasks, I reviewed it, understood what it did, and decided the lambda was clearer. I didn't reject it because it was wrong — it worked fine — but because readability mattered more than a minor style improvement in this context.

- How did you evaluate or verify what the AI suggested?
I read the suggested code before adding it, ran the test suite after each change, and checked that the output in `main.py` matched what I expected. If I didn't understand a suggestion, I asked AI to explain it line by line before saving it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Task completion, task addition, daily recurrence, owner filtering by pet and status, scheduler filtering by pet, conflict detection for both time clashes and overfull days, the edge case of a pet with no tasks, and chronological sorting by HH:MM time.

- Why were these tests important?
The scheduler's value depends on it being trustworthy. If recurrence breaks, owners miss care. If conflict detection crashes instead of warning, the app becomes unusable. Testing these behaviors gave confidence that the core logic holds up before connecting it to the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
4 out of 5. The core behaviors are solid and all 10 tests pass. The gap is duration-overlap detection — two tasks at different times can still overlap in real time, and that isn't checked yet.

- What edge cases would you test next if you had more time?
Tasks whose durations overlap even though their start times differ, an owner with zero available time, marking a "as needed" task complete and verifying no clone is created, and a pet with tasks all already completed.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The scheduling logic ended up being more capable than I originally planned — recurrence, time-based sorting, filtering, and conflict detection all came together cleanly. The fact that all of it is tested and the tests actually caught real design decisions (like what "due" means for a weekly task) is what I'm most satisfied with.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I'd add duration-overlap detection to the conflict checker and build a way for the owner to actually mark tasks complete from the UI rather than only through the backend. I'd also give the Streamlit app persistent state so pets and tasks don't disappear on page refresh.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The design decisions that AI can't make for you are the ones that matter most — what the system should do, what counts as "good enough," and when simplicity beats cleverness. AI can write the code fast, but it doesn't know your users or your constraints. Staying in the architect seat means being willing to say "that's too much" or "that's not what I asked for" and redirecting, rather than just accepting whatever comes back.
