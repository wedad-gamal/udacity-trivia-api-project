from operator import not_
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.sql.sqltypes import Integer

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE
    questions_formated = [question.format() for question in questions]
    current_questions = questions_formated[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # CORS(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins.
  after completing the TODOs
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        # response.header.add('Access-Control-Allow-Credentials', 'true')

        # response.header.add('Access-Control-Allow-Origin', '*')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        try:
            categories = {}
            categories_model = Category.query.all()
            for category in categories_model:
                categories[category.id] = category.type

            return jsonify({
                "success": True,
                "categories": categories
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.all()

            categories = {}
            categories_model = Category.query.all()
            for category in categories_model:
                categories[category.id] = category.type

            current_category = {}
            for question in questions:
                current_category[question.category.id] = question.category.type

            questions_formated = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "questions": questions_formated,
                "total_questions": str(len(questions)),
                "current_category": current_category,
                "categories": categories

            })
        except Exception as e:
            print(e)
            abort(500)

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_questions(id):

        question = Question.query.filter(Question.id == id).one_or_none()
        if (question is None):
            abort(404)
        try:
            question.delete()
            return jsonify({"success": True})

        except Exception as e:
            print(e)
            abort(500)
    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_questions():

        data = request.get_json()
        question = data['question']
        answer = data['answer']
        difficulty = data['difficulty']
        category_id = data['category']

        category = Category.query.filter(
            Category.id == int(category_id)).one_or_none()

        if category is None:
            abort(404)
        try:
            question_model = Question(
                question, answer,  category.id, difficulty)
            question_model.insert()

            return jsonify({
                "success": True,
                "id": question_model.id
            })

        except Exception as e:
            print(e)
            abort(500)
    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            data = request.get_json()
            search_term = data['searchTerm']
            questions = Question.query.filter(
                Question.question.ilike("%"+search_term+"%")).all()
            current_category = {}
            for question in questions:
                current_category[question.category.id] = question.category.type

            return jsonify({
                "success": True,
                "questions": paginate_questions(request, questions),
                "total_questions": len(questions),
                "current_category": current_category
            })

        except Exception as e:
            print(e)
            abort(500)
    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_per_category(category_id):

        if not category_id:
            abort(404)
        try:
            questions = Question.query.filter(
                Question.category_id == category_id).all()
            current_category = {}
            for question in questions:
                current_category[question.category.id] = question.category.type

            questions_formated = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "questions": questions_formated,
                "total_questions": str(len(questions)),
                "current_category": current_category

            })
        except Exception as e:
            print(e)
            abort(500)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():

        data = request.get_json()
        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']
        category_id = quiz_category["id"]
        question = Question.query.filter(~Question.id.in_(
            previous_questions), Question.category_id == category_id).first()
        if question is None:
            abort(404)
        try:
            return jsonify({
                "success": True,
                "question": question.format()

            })
        except Exception as e:
            print(e)
            abort(500)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    return app
