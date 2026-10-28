# Thinkless daily Stories — playbook

Brand: **Thinkless** (@thinkless.mind) — short, calm psychology for overthinkers.
Voice: someone who *gets it*, describing a private habit the viewer recognizes. Never preachy,
never hustle-culture, no clichés ("grind", "no excuses", "rise and grind"), no famous quotes
or quotes attributed to real people. Every line is original.

## Every day: 3 Stories
1. Pick today's **theme** from the rotation below — not used in the last 6 days (see `log.json`).
2. Write 3 Stories on that theme, each a **different layout**, one of them a `contrast` or `question`.
3. Every line must be new — check `log.json` for repeats or near-repeats of earlier lines.
4. Keep text short: max ~12 words of main text per Story, lines of 2–4 words, ALL CAPS.
   `gold` = the 1–3 word payoff phrase (must appear in exactly one line).
5. Render: `python3 tools/make_story.py spec.json stories/YYYY-MM-DD/N.jpg` (N = 1,2,3).
6. Look at each rendered image before using it: spelling, nothing cut off, text inside the safe area.
7. Append the day to `log.json`, commit and push.
8. Schedule each image in Metricool (brand id 7218516) as an Instagram **STORY**, no text,
   autoPublish true, at 09:00, 14:00 and 20:30 Asia/Calcutta, using the raw URL
   `https://raw.githubusercontent.com/meetkhunt1/thinkless-stories/main/stories/YYYY-MM-DD/N.jpg`.

## Layouts
- `quote` — label (optional) + lines + character below. Good for reassurance.
- `statement` — big centered lines, no character. Good for sharp one-liners.
- `question` — "Be honest" kicker + a question to the viewer + small character.
- `tip` — "Try this today" kicker + a tiny concrete action + 1–2 small `sub` lines explaining why.
- `contrast` — `a_label`/`a_lines` (what overthinking/fear/the inner critic says) vs
  `b_label`/`b_lines` (what's actually true). Labels can vary: "Your brain at 2 AM" / "Reality",
  "Fear says" / "Truth is", "The inner critic" / "A kinder voice".

## Theme rotation
overthinking · procrastination · fear of failure · perfectionism · self-doubt · comparison ·
rest without guilt · small wins · night-time spirals · decision paralysis · people-pleasing ·
self-talk · consistency over motivation · letting go of control

## Spec examples
```json
{"layout":"contrast","a_lines":["IF IT'S NOT PERFECT,","DON'T EVEN START."],"b_lines":["A MESSY START","BEATS A PERFECT PLAN."],"gold":"perfect plan"}
{"layout":"question","lines":["WHAT ARE YOU","AVOIDING TODAY","BECAUSE IT FEELS","TOO BIG?"],"gold":"too big"}
{"layout":"tip","lines":["OPEN IT.","WORK 2 MINUTES.","THEN DECIDE."],"gold":"2 minutes","sub":["Most of the resistance","lives in the first minute."]}
```
