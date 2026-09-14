https://x.com/Mahaximus_/status/2085024744387092973


### 4 - The memory problem and how to fix it
This is the most common place agents break down, and it happens 
in three specific ways:

1. The task runs too long and the agent loses the beginning. The original goal, 
   the decisions already made, the constraints you set, all of it falls out of the 
   context window. The agent keeps working but has quietly forgotten what it was working toward.
2. You close the session and open a new one. The agent starts from zero. Everything from the previous run is gone.
3. The agent gets interrupted mid-task. When you come back, 
   it has no record of where it stopped, 
   what it already tried, 
   or what failed.

All three have the same fix: make the agent write its own memory.

### Paste this mid-task to create a progress record:
claude: /compact

```
Before we continue, write a checkpoint:
1. What have you completed so far?
2. What decisions were made and why?
3. What still needs to happen?
4. What would you need to resume this in a new session?

Keep it under 150 words. Be specific - vague checkpoints are useless.
```

### Paste this when a session is getting long:

```
The conversation is getting long. Compress what matters into a summary:
1. The original goal
2. What has been done and what was found
3. Key decisions made
4. What still needs to happen

After writing the summary, continue from there. Treat it as the new starting point.
```

### Paste this at the start of a new session to restore context:

```
We are resuming from a previous session. Here is the context:

[paste your checkpoint here]

Confirm your understanding of where we are, identify the next step, and continue without repeating work already done.
```
