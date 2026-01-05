from flask import Flask, request, jsonify, session, render_template_string
from flask_cors import CORS
import os
import random
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
CORS(app)

UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>French Vocabulary Quiz</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .section { margin: 20px 0; }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        button:hover { background-color: #45a049; }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        input[type="text"], input[type="number"], input[type="file"] {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
            box-sizing: border-box;
            margin: 10px 0;
        }
        select {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
            margin: 10px 0;
        }
        .question {
            font-size: 24px;
            color: #2196F3;
            margin: 20px 0;
        }
        .feedback {
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        }
        .correct { background-color: #d4edda; color: #155724; }
        .incorrect { background-color: #f8d7da; color: #721c24; }
        .stats {
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .hidden { display: none; }
        .option-btn {
            display: block;
            width: 100%;
            margin: 10px 0;
            background-color: #2196F3;
            text-align: left;
        }
        .option-btn:hover { background-color: #0b7dda; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇫🇷 French Vocabulary Quiz</h1>
        
        <!-- Upload Section -->
        <div id="uploadSection" class="section">
            <h2>Step 1: Upload Vocabulary Files</h2>
            <input type="file" id="fileInput" multiple accept=".txt">
            <button onclick="uploadFiles()">Upload Files</button>
            <div id="uploadFeedback"></div>
        </div>
        
        <!-- Setup Section -->
        <div id="setupSection" class="section hidden">
            <h2>Step 2: Configure Quiz</h2>
            <label>Quiz Type:</label>
            <select id="quizType">
                <option value="traditional">Traditional (Type Answer)</option>
                <option value="multiple_choice">Multiple Choice</option>
            </select>
            
            <label>Mode:</label>
            <select id="quizMode" onchange="toggleNumQuestions()">
                <option value="continuous">Continuous</option>
                <option value="set">Set Number</option>
                <option value="max">Maximum (All Questions)</option>
            </select>
            
            <div id="numQuestionsDiv" class="hidden">
                <label>Number of Questions:</label>
                <input type="number" id="numQuestions" value="10" min="1">
            </div>
            
            <button onclick="startQuiz()">Start Quiz</button>
        </div>
        
        <!-- Quiz Section -->
        <div id="quizSection" class="section hidden">
            <div class="stats" id="stats"></div>
            <div class="question" id="question"></div>
            <div id="answerArea"></div>
            <div id="feedback"></div>
        </div>
        
        <!-- Results Section -->
        <div id="resultsSection" class="section hidden">
            <h2>Quiz Complete! 🎉</h2>
            <div class="stats" id="finalStats"></div>
            <button onclick="resetQuiz()">Start New Quiz</button>
        </div>
    </div>

    <script>
        let currentQuestionId = null;

        function toggleNumQuestions() {
            const mode = document.getElementById('quizMode').value;
            const div = document.getElementById('numQuestionsDiv');
            div.className = mode === 'set' ? 'section' : 'hidden';
        }

        async function uploadFiles() {
            const fileInput = document.getElementById('fileInput');
            const files = fileInput.files;
            
            if (files.length === 0) {
                alert('Please select at least one file');
                return;
            }
            
            const formData = new FormData();
            for (let file of files) {
                formData.append('files[]', file);
            }
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('uploadFeedback').innerHTML = 
                        `<div class="feedback correct">✓ Uploaded: ${data.files.join(', ')}</div>`;
                    document.getElementById('setupSection').classList.remove('hidden');
                } else {
                    document.getElementById('uploadFeedback').innerHTML = 
                        `<div class="feedback incorrect">✗ Error: ${data.error}</div>`;
                }
            } catch (error) {
                alert('Upload failed: ' + error);
            }
        }

        async function startQuiz() {
            const quizType = document.getElementById('quizType').value;
            const mode = document.getElementById('quizMode').value;
            const numQuestions = document.getElementById('numQuestions').value;
            
            try {
                const response = await fetch('/api/start-quiz', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        quiz_type: quizType,
                        mode: mode,
                        num_questions: parseInt(numQuestions)
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('uploadSection').classList.add('hidden');
                    document.getElementById('setupSection').classList.add('hidden');
                    document.getElementById('quizSection').classList.remove('hidden');
                    loadQuestion();
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Failed to start quiz: ' + error);
            }
        }

        async function loadQuestion() {
            try {
                const response = await fetch('/api/get-question');
                const data = await response.json();
                
                if (data.quiz_complete) {
                    showResults();
                    return;
                }
                
                currentQuestionId = data.question_id;
                
                document.getElementById('stats').innerHTML = 
                    `Question ${data.question_number} of ${data.total_questions}`;
                document.getElementById('question').innerHTML = 
                    `Translate: <strong>${data.question}</strong>`;
                document.getElementById('feedback').innerHTML = '';
                
                // Create answer area based on quiz type
                const answerArea = document.getElementById('answerArea');
                
                if (data.options) {
                    // Multiple choice
                    let html = '';
                    data.options.forEach((option, index) => {
                        html += `<button class="option-btn" onclick="submitAnswer('${option}')">${index + 1}. ${option}</button>`;
                    });
                    answerArea.innerHTML = html;
                } else {
                    // Traditional
                    answerArea.innerHTML = `
                        <input type="text" id="answerInput" placeholder="Type your answer here..." 
                               onkeypress="if(event.key==='Enter') submitAnswer()">
                        <button onclick="submitAnswer()">Submit</button>
                    `;
                    document.getElementById('answerInput').focus();
                }
            } catch (error) {
                alert('Failed to load question: ' + error);
            }
        }

        async function submitAnswer(multiChoiceAnswer = null) {
            const answer = multiChoiceAnswer || document.getElementById('answerInput')?.value;
            
            if (!answer) {
                alert('Please provide an answer');
                return;
            }
            
            try {
                const response = await fetch('/api/submit-answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        answer: answer,
                        question_id: currentQuestionId
                    })
                });
                
                const data = await response.json();
                
                const feedback = document.getElementById('feedback');
                if (data.correct) {
                    feedback.innerHTML = '<div class="feedback correct">✓ Correct!</div>';
                } else {
                    feedback.innerHTML = 
                        `<div class="feedback incorrect">✗ Incorrect. The answer was: <strong>${data.correct_answer}</strong></div>`;
                }
                
                // Load next question after delay
                setTimeout(() => {
                    loadQuestion();
                }, 1500);
                
            } catch (error) {
                alert('Failed to submit answer: ' + error);
            }
        }

        async function showResults() {
            try {
                const response = await fetch('/api/quiz-stats');
                const data = await response.json();
                
                document.getElementById('quizSection').classList.add('hidden');
                document.getElementById('resultsSection').classList.remove('hidden');
                
                const percentage = Math.round((data.correct_count / data.total_questions) * 100);
                document.getElementById('finalStats').innerHTML = `
                    <h3>Your Score: ${data.correct_count} / ${data.total_questions} (${percentage}%)</h3>
                `;
            } catch (error) {
                alert('Failed to load results: ' + error);
            }
        }

        async function resetQuiz() {
            try {
                await fetch('/api/reset', { method: 'POST' });
                location.reload();
            } catch (error) {
                alert('Failed to reset: ' + error);
            }
        }
    </script>
</body>
</html>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_vocab_file(filepath):
    """Parse a vocabulary file and return list of words"""
    vocab = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [s.rstrip() for s in lines]
        # Skip first 2 lines if they exist (headers)
        if len(lines) > 2:
            del lines[0:2]
        for line in lines:
            if line.strip():
                vocab.append(line.strip())
    return vocab

def merge_vocab_lists(vocab_lists):
    """Merge multiple vocabulary lists"""
    total = []
    for vocab in vocab_lists:
        total.extend(vocab)
    return total

def get_random_odd(vocab_list):
    """Get random odd index (English word)"""
    r = random.randint(0, len(vocab_list)-1)
    while (r % 2) == 0:
        r = random.randint(0, len(vocab_list)-1)
    return r

def get_random_even(vocab_list):
    """Get random even index (French word)"""
    r = random.randint(0, len(vocab_list)-1)
    while (r % 2) != 0:
        r = random.randint(0, len(vocab_list)-1)
    return r

@app.route('/')
def home():
    """Render the main quiz interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Upload vocabulary files"""
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files[]')
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filename)
    
    if not uploaded_files:
        return jsonify({'error': 'No valid files uploaded'}), 400
    
    # Store filenames in session
    session['uploaded_files'] = uploaded_files
    
    return jsonify({
        'message': 'Files uploaded successfully',
        'files': uploaded_files
    })

@app.route('/api/start-quiz', methods=['POST'])
def start_quiz():
    """Initialize a new quiz session"""
    data = request.json
    quiz_type = data.get('quiz_type', 'traditional')
    mode = data.get('mode', 'continuous')
    num_questions = data.get('num_questions', 10)
    
    # Get uploaded files from session
    uploaded_files = session.get('uploaded_files', [])
    if not uploaded_files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    # Parse all vocabulary files
    vocab_lists = []
    for filename in uploaded_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            vocab_lists.append(parse_vocab_file(filepath))
    
    # Merge all vocabulary
    vocab_list = merge_vocab_lists(vocab_lists)
    
    if len(vocab_list) < 2:
        return jsonify({'error': 'Not enough vocabulary words'}), 400
    
    # Store quiz data in session
    session['vocab_list'] = vocab_list
    session['quiz_type'] = quiz_type
    session['mode'] = mode
    session['current_question'] = 0
    session['correct_count'] = 0
    session['total_questions'] = num_questions if mode == 'set' else len(vocab_list) // 2
    
    return jsonify({
        'message': 'Quiz started',
        'total_pairs': len(vocab_list) // 2,
        'total_questions': session['total_questions']
    })

@app.route('/api/get-question', methods=['GET'])
def get_question():
    """Get the next quiz question"""
    vocab_list = session.get('vocab_list', [])
    quiz_type = session.get('quiz_type', 'traditional')
    current_question = session.get('current_question', 0)
    total_questions = session.get('total_questions', 0)
    
    if not vocab_list or len(vocab_list) < 2:
        return jsonify({'error': 'No vocabulary available'}), 400
    
    if session.get('mode') != 'continuous' and current_question >= total_questions:
        return jsonify({'quiz_complete': True})
    
    # Get a random question
    if quiz_type == 'traditional':
        r = get_random_odd(vocab_list)
        if r >= len(vocab_list):
            r = len(vocab_list) - 1
            if r % 2 == 0:
                r -= 1
        
        french_word = vocab_list[r-1]
        
        return jsonify({
            'question_number': current_question + 1,
            'total_questions': total_questions,
            'question': french_word,
            'question_id': r
        })
    
    else:  # multiple_choice
        r = get_random_even(vocab_list)
        if r >= len(vocab_list) - 1:
            r = len(vocab_list) - 2
        
        french_word = vocab_list[r]
        correct_answer = vocab_list[r + 1]
        
        # Generate wrong answers
        options = [correct_answer]
        attempts = 0
        while len(options) < 4 and attempts < 50:
            rand_r = get_random_even(vocab_list)
            if rand_r >= len(vocab_list) - 1:
                rand_r = len(vocab_list) - 2
            wrong_answer = vocab_list[rand_r + 1]
            if wrong_answer != correct_answer and wrong_answer not in options:
                options.append(wrong_answer)
            attempts += 1
        
        random.shuffle(options)
        
        return jsonify({
            'question_number': current_question + 1,
            'total_questions': total_questions,
            'question': french_word,
            'options': options,
            'question_id': r
        })

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """Check the submitted answer"""
    data = request.json
    user_answer = data.get('answer', '').strip().lower()
    question_id = data.get('question_id')
    
    vocab_list = session.get('vocab_list', [])
    
    if question_id is None or not vocab_list:
        return jsonify({'error': 'Invalid request'}), 400
    
    # Get correct answer based on question type
    quiz_type = session.get('quiz_type', 'traditional')
    
    if quiz_type == 'traditional':
        correct_answer = vocab_list[question_id].strip().lower()
    else:  # multiple_choice
        correct_answer = vocab_list[question_id + 1].strip().lower()
    
    is_correct = user_answer == correct_answer
    
    # Update session
    current_question = session.get('current_question', 0)
    session['current_question'] = current_question + 1
    
    if is_correct:
        correct_count = session.get('correct_count', 0)
        session['correct_count'] = correct_count + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': vocab_list[question_id] if quiz_type == 'traditional' else vocab_list[question_id + 1],
        'total_correct': session.get('correct_count', 0)
    })

@app.route('/api/quiz-stats', methods=['GET'])
def quiz_stats():
    """Get current quiz statistics"""
    return jsonify({
        'current_question': session.get('current_question', 0),
        'total_questions': session.get('total_questions', 0),
        'correct_count': session.get('correct_count', 0)
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the quiz session"""
    session.clear()
    return jsonify({'message': 'Session reset'})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("French Vocabulary Quiz Server")
    print("="*50)
    print("\n🌐 Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n📝 Make sure your vocabulary files are in .txt format")
    print("   Format: French word on even lines, English on odd lines")
    print("\n" + "="*50 + "\n")
    app.run(debug=True, port=5000)
