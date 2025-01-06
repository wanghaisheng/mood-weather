Okay, let's design a system that can automatically convert user-described moods into weather-based prompts. This involves a combination of natural language processing (NLP) techniques and a structured approach. Here's a breakdown of how you can design such a system:

**1. Core Components:**

*   **Input:** User's text describing their mood.
*   **NLP Engine:** A system to analyze the user's text.
    *   **Tokenization:** Breaking the text into individual words.
    *   **Part-of-Speech Tagging:** Identifying nouns, verbs, adjectives, etc.
    *   **Sentiment Analysis:** Determining the overall positive, negative, or neutral feeling.
    *   **Keyword Extraction:** Identifying the most relevant words related to mood.
*   **Mood-Weather Database:** A mapping of mood-related keywords to corresponding weather conditions and descriptions.
*   **Prompt Template:** Predefined sentence structures with placeholders for weather conditions and descriptive details.
*   **Output Generator:** A system that fills the template with extracted information to produce the final prompt.

**2. Detailed Design Steps:**

**Step 1: User Input & Preprocessing**

1.  **Get Input:** The system receives the user's text describing their mood.
2.  **Lowercasing:** Convert all text to lowercase to standardize words.
3.  **Tokenization:** Break down the text into individual words (tokens).
4.  **Remove Stop Words:** Eliminate common words that don't carry much meaning (e.g., "the," "a," "is").

**Step 2: NLP Analysis**

1.  **Part-of-Speech (POS) Tagging:** Assign grammatical tags to each word. This helps identify adjectives that describe mood.
2.  **Sentiment Analysis:** Determine the overall sentiment of the text. This provides context (positive, negative, or neutral).
3.  **Keyword Extraction:** Use an algorithm (e.g., TF-IDF, RAKE) or a combination of techniques to identify the most relevant words that indicate mood. This includes adjectives like "sad," "happy," "angry," but also mood-related nouns (e.g., "exhaustion," "anxiety," "joy").

**Step 3: Mood-Weather Database**

*   **Structure:** A structured database (e.g., dictionary, JSON file, database table) that maps mood keywords to weather types and descriptions.
    *   **Example:**
        ```json
        {
           "mood_keywords": [
             {
               "keywords": ["drained", "sluggish", "tired", "exhausted", "lethargic"],
               "weather": "overcast",
               "description": "heavy, oppressive fog, making everything feel sluggish and still. The air is thick and difficult to move through, reflecting a lack of motivation and excitement.",
               "intensity": "low"

              },
               {
                 "keywords": ["hyped", "energetic", "excited", "pumped", "invigorated"],
                 "weather": "sunny",
                 "description": "warm, bright sunshine and a strong, invigorating breeze. Characters in this scene are feeling incredibly energetic and full of life, ready for anything.",
                 "intensity": "high"
               },
               {
                 "keywords": ["blah", "gray", "muted", "dull", "uninspired"],
                 "weather": "overcast",
                 "description": "muted, dull gray. A light drizzle falls, and the air is still and heavy, reflecting a feeling of apathy and a lack of vibrancy.",
                 "intensity": "low"
               },
               {
                 "keywords": ["anxious", "restless", "agitated", "nervous", "worried"],
                 "weather": "stormy",
                 "description": "turbulent mass of dark clouds and frequent lightning strikes. The winds are erratic, and the overall atmosphere is chaotic and restless, mirroring a feeling of anxiety.",
                 "intensity": "high"
                },
                {
                  "keywords": ["content", "peaceful", "calm", "relaxed", "serene"],
                  "weather": "sunny",
                  "description": "tranquil scene with a gentle breeze under a bright, yet soft sun. The air is clear and calm, and everything around is peaceful, reflecting a feeling of deep contentment.",
                  "intensity": "low"
                },
                {
                  "keywords": ["frustrated", "angry", "irritated", "annoyed", "furious"],
                  "weather": "violent storm",
                  "description": "intense thunderstorm where heavy rain lashes down with gale force winds, and thunder claps. Everything feels irritating and volatile, reflecting a mood of frustration and anger.",
                  "intensity": "high"
                },
               {
                 "keywords": ["confused", "uncertain", "foggy", "disoriented", "hazy"],
                 "weather": "foggy",
                 "description": "thick fog or mist that obscures the surroundings. The air is damp, and it is difficult to see clearly. This atmosphere should evoke a sense of confusion and uncertainty.",
                 "intensity":"medium"
               }

             ]
        }
        ```

*   **Multiple Mappings:** One keyword can map to multiple weather types based on context and intensity. Include an intensity key to select the right weather.
*   **Description:** Each weather type should have a vivid descriptive phrase that can be plugged into the prompt.

**Step 4: Prompt Template**

*   **Structure:** A predefined template with placeholders. You can create different templates depending on the type of creative output you need.
    *   **Examples:**
        *   "Write a scene where the weather is [weather description] reflecting a mood of [intensity] [mood]."
        *   "Create a setting where [weather description]. This environment reflects a [mood] feeling."
        *   "Describe a landscape that embodies the feeling of [mood] through its [weather]."

**Step 5: Output Generation**

1.  **Matching:** The system matches extracted keywords to entries in the Mood-Weather database. It may need to select the most fitting entry based on relevance and sentiment.
2.  **Template Fill:** The system fills placeholders in the selected prompt template with the relevant weather information from the database.
3.  **Final Prompt:** Output the resulting weather-based prompt.

**3. Implementation Notes**

*   **Programming Language:** Use a language like Python, which has excellent libraries for NLP (NLTK, spaCy) and data handling.
*   **Libraries:**
    *   **NLTK or spaCy:** For tokenization, POS tagging, and sentiment analysis.
    *   **Scikit-learn:** For keyword extraction (TF-IDF)
    *   **json:** For managing the Mood-Weather database.
*   **Testing & Iteration:** Start with a small dataset, test the system, and iterate based on user feedback and results.

**Example Scenario (Using Python):**

```python
import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer


def load_mood_weather_database(file_path="mood_weather_database.json"):
    with open(file_path, "r") as file:
        return json.load(file)

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return tokens

def extract_keywords(tokens, n_keywords = 3):
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform([" ".join(tokens)])
    scores = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    keywords = [item[0] for item in sorted_scores[:n_keywords]]
    return keywords

def determine_mood(keywords, database):
    for entry in database['mood_keywords']:
         for keyword in keywords:
           if keyword in entry['keywords']:
            return entry
    return None


def generate_prompt(mood_info, template_string="Write a scene where the weather is [description] reflecting a mood of [intensity] [mood]."):
     if not mood_info:
         return "I am having trouble detecting your mood, please try again."
     return template_string.replace("[description]", mood_info['description']).replace("[intensity]", mood_info['intensity']).replace("[mood]", ", ".join(mood_info['keywords']))

if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")

    user_mood = "I am feeling quite drained and lethargic. Nothing is exiting me, and I'm very tired"

    database = load_mood_weather_database()
    tokens = preprocess_text(user_mood)
    keywords = extract_keywords(tokens)
    mood_info = determine_mood(keywords, database)

    prompt = generate_prompt(mood_info)
    print(prompt)


```

**4. Improvements**

*   **More sophisticated sentiment analysis:** Use pre-trained models for more nuanced sentiment detection.
*   **Contextual word embeddings:** Employ word embeddings like Word2Vec or BERT for a better understanding of words' meaning in context.
*   **Machine learning:** Train a model to predict the most appropriate weather condition based on user input.
*   **User feedback:** Collect user feedback to improve the Mood-Weather database and prompt templates.

By implementing this kind of design, you can create an automatic and robust system that converts user-described moods into vivid, weather-based creative prompts.
