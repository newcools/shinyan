# Shinyan card app
## The idea
This is an open-source app designed to use the spaced repetition method to help users retain information, such as learning new vocabulary in a foreign language.

The approach is similar to [ANKI cards]([https://link-url-here.org](https://ankiweb.net/decks)), but we handle it differently.

Instead of manually creating fixed cards, the content is AI-generated. It can include audio, images, or even videos, and in theory, it can vary each time. 

For example, take the Japanese word いく (to go). Using the ChatGPT API, we can easily generate a list of example sentences, each one containing the Japanese sentence, its English translation (or another language the learner prefers), and the Hiragana.

```json
{
  "value": "いく"
  "contents": [
    {
      "Japanese": "明日、友達と映画を見に行く予定です。",
      "Hiragana": "あした、ともだちとえいがをみにいくよていです。",
      "English": "Tomorrow, I plan to go watch a movie with my friend."
    },
    {
      "Japanese": "毎朝、ジョギングをするために公園に行きます。",
      "Hiragana": "まいあさ、じょぎんぐをするためにこうえんにいきます。",
      "English": "Every morning, I go to the park to jog."
    },
    {
      "Japanese": "学校が終わったら、すぐに家に帰りに行きます。",
      "Hiragana": "がっこうがおわったら、すぐにいえにかえりにいきます。",
      "English": "After school is over, I will go home right away."
    },
    {
      "Japanese": "週末には友達と一緒に旅行に行く予定です。",
      "Hiragana": "しゅうまつにはともだちといっしょにりょこうにいくよていです。",
      "English": "I plan to go on a trip with my friends this weekend."
    },
    {
      "Japanese": "来週、家族と一緒に温泉に行くつもりです。",
      "Hiragana": "らいしゅう、かぞくといっしょにおんせんにいくつもりです。",
      "English": "Next week, I intend to go to a hot spring with my family."
    }
  ]
}
```

From here, we can generate audio, images, or video content based on the user’s needs.

The key difference from Anki is that this app can be used without a screen. It plays audio directly through your earphones while you're jogging or doing other activities, freeing up your hands and eyes.

## Code Structure
This project is divided into three main parts:

Front end: We use the Expo.dev framework to create the app, which can be built as both a web app and a mobile app.
Back end: All card generation and related functionalities are handled using FastAPI, which can run as either a CLI tool or a backend service.
Infrastructure as Code (IaC): We primarily use Azure and the Terraform code for managing infrastructure is included here.

## near future plan 
we plan to migrate to use the [open spaced repetition](https://github.com/open-spaced-repetition) library instead of the current implementation of [simple-spaced-repetition ](https://github.com/vlopezferrando/simple-spaced-repetition) that is what I originally forked from 
