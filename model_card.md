# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**BuenaVibe 1.0**  

---

## 2. Intended Use  

This system suggests 5 songs from a small catalog based on a user's preferred genre, mood, energy, and valence. It is built for classroom exploration only, not for real users or production use.

## 2b. Goal / Task

The goal is to take a user taste profile and return the top 5 songs from the catalog that best match their preferences. It predicts "what song fits this person right now" based on genre, mood, and audio features.

## 2c. Non-Intended Use

This system is not meant for real music platforms or actual users. It should not be used to make decisions about what music gets promoted or recommended at scale. It was built to learn how recommenders work, not to replace one.

---

## 3. How the Model Works  

The system reads a list of songs from a CSV file and scores each one against a user taste profile. It gives bonus points for matching genre and mood, and calculates closeness scores for energy, valence, danceability, and acousticness. Songs are then sorted by total score and the top 5 are returned with explanations.

---

## 4. Data  

The dataset has 18 songs across genres including pop, lofi, rock, jazz, reggae, and r&b. Songs include features like energy, valence, mood, danceability, and acousticness on a 0.0-1.0 scale. The dataset is small and mostly reflects mainstream Western music taste.

---

## 5. Strengths  

The system works well when the user has a clear genre and mood preference. The explanation feature makes it transparent, you can always see exactly why a song was recommended. It also handles edge cases cleanly by checking if each feature exists before scoring it.

---

## 6. Limitations and Bias 

Genre match gives +2.0 points, the biggest bonus in the system, so it almost always decides who ranks first — even if another song matches energy and mood better. This creates a genre filter bubble.

Genre and mood also require exact string matches, so "indie pop" gets zero bonus on songs tagged "pop". Niche genres are hurt the most.

Users who care about acousticness or danceability get poor results since those are only worth 0.5 points max. And with only 18 songs, if your favorite genre appears once or twice, there's not much to recommend from.

---

## 7. Evaluation  

I tested 3 user profiles: Happy Pop, Chill Lofi, and Deep Intense Rock. Each profile returned sensible top results that matched the intended vibe. I also ran a weight experiment where i doubled energy and halved genre, which showed that genre was dominating the scores. Reducing it gave more variety in the rankings.

---

## 8. Future Work  

- Add a diversity penalty so the same artist doesn't appear twice in top 5
- Use energy and valence ranges instead of single target values
- Expand the dataset to 50+ songs for more varied recommendations

---

## 9. Personal Reflection  

The biggest takeaway was how much one number can change everything. The genre weight basically runs the whole system. I expected it to feel more intelligent but at the end of the day it is just math. Copilot helped me get started faster but I still had to actually understand the code to catch things like wrong key names or the output not showing up right. This project changed how I see apps like Spotify. What feels like a smart recommendation is really just a scoring system with the right weights and getting those weights right is what makes or breaks the whole thing.
