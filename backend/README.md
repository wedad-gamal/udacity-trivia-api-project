## Udacitrivia

This project is a banking questions in science, art, geography, history, entertainment, sports, you could add new question or remove question also you could play and get a score after answering the quizzes’ questions.

## Getting Started

Pre-requisites and Local Development
To use this project you should already have Python3, pip and node installed on testing machines.

## Backend

1. Initialize and activate a virtualenv using:

   ```
   python -m virtualenv env
   source env/bin/activate
   ```

   > **Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

   ```
   source env/Scripts/activate
   ```

2. From the backend folder run

   ```
   pip install requirements.txt.
   ```

   All required packages are included in the requirements file.

3. To run the application run the following commands:
   ```
   export FLASK_APP=flaskr
   export FLASK_ENV=development
   flask run
   ```

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

## Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

## Tests

In order to run tests navigate to the backend folder and run the following commands:

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

for windows run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql postgres
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

## API Reference

### Getting Started

#### Base URL:

At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

#### Authentication:

This version of the application does not require authentication or API keys.

#### Error Handling:

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

#### The API will return three error types when requests fail:

```
400: Bad Request
404: Resource Not Found
422: Not Processable
500: Internal server error
```

## Endpoints

#### GET /categories

#### General:

- Returns a list of categories objects.
- Sample: curl http://127.0.0.1:5000/categories

```
  {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET /questions

#### General:

- Returns a list of questions, number of total questions, current category, categories.
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: curl http://127.0.0.1:5000/questions

```
  {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 1,
      "question": "Whose autobiography is entitled \"I Know Why the Caged Bird Sings\"?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 2,
      "question": "What boxer 's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 3,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 6,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 7,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 8,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 9,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 10,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": "19"
}
```

#### DELETE /questions/9

#### General:

- Returns request status after deleting question by id.
- Sample: curl http://127.0.0.1:5000/questions/9

```
{
    "success": true
}
```

#### POST /questions

#### General:

- Returns new created question id.
- Sample: curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"question": "who discovered America?", "answer": "Christopher Columbus", "difficulty": 1, "category": "1"}'

```
{
  "id": 27,
  "success": true
}

```

#### POST /questions/search

#### General:

- Returns questions based on a search term. It should return any questions for whom the search term is a substring of the question..
- Sample: curl http://127.0.0.1:5000/questions/search?page=1 -X POST -H "Content-Type: application/json" -d '{"searchTerm": "What is the heaviest"}'

```
{
  "current_category": {
    "1": "Science"
  },
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 16,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### GET /categories/3/questions

#### General:

- Returns questions based on category.
- Sample: curl http://127.0.0.1:5000/categories/3/questions

```
{
  "current_category": {
    "3": "Geography"
  },
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 10,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 11,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": "2"
}
```

#### POST /quizzes

#### General:

- Returns a random questions within the given category,
  if provided, and that is not one of the previous questions.
- Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [17], "quiz_category": {"type": "Science", "id": "1"}}'

```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 16,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}

```

## Deployment N/A

## Authors

Yours Wedad, Udacity team.

## Acknowledgements

The awesome team at Udacity.
