import os
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory "database"
threads = []
thread_id_counter = 1
reply_id_counter = 1

# File upload settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

valid_boards = {
    'entertainment': ['anime', 'sports', 'videogames'],
    'study': ['tech', 'math', 'history'],
    'hobby': ['art', 'paper', 'photo']
}


def get_category_from_board(board_name):
    for category, boards in valid_boards.items():
        if board_name in boards:
            return category
    return None


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/<category>/<board_name>')
def show_board(category, board_name):
    valid_boards = {
        'entertainment': ['anime', 'sports', 'videogames'],
        'study': ['tech', 'math', 'history'],
        'hobby': ['art', 'paper', 'photo']
    }

    if category not in valid_boards or board_name not in valid_boards[category]:
        return "Board not found", 404

    board_threads = sorted(
        [t for t in threads if t['board'] == board_name],
        key=lambda x: x['last_activity'],
        reverse=True
    )
    return render_template('board.html', board_name=board_name, category=category)

# All threads stored like { 'board': 'anime', ... }
threads = []

@app.route('/api/threads/<board_name>', methods=['GET'])
def get_threads(board_name):
    board_threads = [t for t in threads if t['board'] == board_name]
    sorted_threads = sorted(board_threads, key=lambda x: x['last_activity'], reverse=True)
    return jsonify(sorted_threads)

@app.route('/api/thread/<board_name>', methods=['POST'])
def create_thread(board_name):
    global thread_id_counter
    title = request.form.get('title')
    content = request.form.get('content')
    image = request.files.get('image')

    image_url = None
    if image and allowed_file(image.filename):
        filename = secure_filename(f"{thread_id_counter}_{image.filename}")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = f"/static/uploads/{filename}"

    new_thread = {
        'id': thread_id_counter,
        'board': board_name,  
        'title': title,
        'content': content,
        'image': image_url,
        'comments': [],
        'created_at': datetime.utcnow().strftime('%b %d, %Y %H:%M UTC'),
        'last_activity': datetime.utcnow().isoformat()
    }
    threads.append(new_thread)
    thread_id_counter += 1
    
    return jsonify({'status': 'success'}), 201
    '''
    category = get_category_from_board(board_name)
    if not category:
        return "Invalid board", 400

    return redirect(url_for('show_board', category=category, board_name=board_name))
    '''



@app.route('/api/thread/<int:thread_id>/comment', methods=['POST'])
def add_comment(thread_id):
    global reply_id_counter
    comment_text = request.form.get('comment')
    image = request.files.get('image')
    parent_id = request.form.get('parent_id')

    image_url = None
    if image and allowed_file(image.filename):
        filename = secure_filename(f"{thread_id}_comment_{image.filename}")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = f"/static/uploads/{filename}"

    for thread in threads:
        if thread['id'] == thread_id:
            thread['comments'].append({
                'id': reply_id_counter,
                'comment': comment_text,
                'image': image_url,
                'timestamp': datetime.utcnow().strftime('%b %d, %Y %H:%M UTC'),
                'parent_id': int(parent_id) if parent_id else None
            })
            reply_id_counter += 1
            thread['last_activity'] = datetime.utcnow().isoformat()
            return jsonify({'status': 'comment added'}), 200

    return jsonify({'error': 'Thread not found'}), 404


def annotate_comment_levels(comments):
    def set_levels(comments, parent_id=None, level=0):
        for comment in comments:
            if comment.get('parent_id') == parent_id:
                comment['level'] = level
                set_levels(comments, comment['id'], level + 1)
    set_levels(comments)

@app.route('/<board_name>/thread/<int:thread_id>')
def view_thread(board_name, thread_id):
    for thread in threads:
        if thread['id'] == thread_id:
            annotate_comment_levels(thread['comments'])
            return render_template('thread.html', thread=thread, board_name=board_name)
    return "Thread not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


'''
if __name__ == '__main__':
    app.run(debug=True)
'''
