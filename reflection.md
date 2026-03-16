# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
ANSWER: The game loaded and looked playable at first, but the behavior was inconsistent once I started submitting guesses. The biggest bug was that the hint logic was incorrectly saying to go higher or lower. The "New Game" button does not fully reset all game state cleanly, so behavior can stay inconsistent after restart. The attempts counter starts in a way that makes attempts-left feel off by one

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
ANSWER:
I used Claude Code (Anthropic) as my AI teammate throughout this project.
**Correct — `check_guess` hint logic:** I told the AI the hints felt backwards. It suggested `if guess > secret: return "Too High"` was already correct and generated pytest cases to prove it. Running the tests confirmed all branches passed, including off-by-one values like `check_guess(51, 50) → "Too High"`.
**Incorrect — `attempts` initialisation:** The AI suggested starting `attempts` at `1` instead of `0` to fix the off-by-one feel. This was wrong. I verified by running the app and checking the debug panel, which showed `attempts = 0` with `+= 1` on each submit was already correct.

---
## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
ANSWER:
A bug felt fixed only when both a manual play-through and a pytest run agreed. I ran `pytest test/test_game_logic.py -v` after each change; if any test failed, the bug was still there. The most useful test was `test_guess_one_above_secret`, which called `check_guess(51, 50)` and asserted `"Too High"` — a tight edge case that would instantly catch a swapped comparison. The AI suggested the off-by-one and boundary inputs I wouldn't have written on my own, making the suite catch subtle mistakes rather than just obvious ones.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
