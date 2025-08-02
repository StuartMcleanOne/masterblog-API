from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Sample in-memory list to store posts
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."}
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve blog posts with optional sorting.
    Accepts 'sort' (title or content) and 'direction' (asc or desc) as query parameters.
    Returns sorted or original list of posts.
    """
    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    valid_fields = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    sorted_posts = POSTS.copy()  # Preserve original order unless sorting applied

    # Validate sort field
    if sort_field and sort_field not in valid_fields:
        return jsonify({'error': 'Invalid sort field. Must be "title" or "content".'}), 400

    # Validate direction
    if direction and direction not in valid_directions:
        return jsonify({'error': 'Invalid direction. Must be "asc" or "desc".'}), 400

    # Apply sorting only if valid sort_field is provided
    if sort_field:
        reverse_sort = direction == 'desc'
        sorted_posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse_sort)

    return jsonify(sorted_posts), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.
    Expects JSON with 'title' and 'content'.
    Assigns an auto-incremented ID to the new post.
    """
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Missing title or content'}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        'id': new_id,
        'title': data['title'],
        'content': data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by ID.
    Returns a success message or 404 if not found.
    """
    post_to_delete = next((post for post in POSTS if post['id'] == post_id), None)
    if not post_to_delete:
        return jsonify({'error': f'Post with id {post_id} not found.'}), 404

    POSTS.remove(post_to_delete)
    return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update a blog post by ID.
    Accepts JSON with optional 'title' and 'content'.
    Returns updated post or 404 if not found.
    """
    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if not post_to_update:
        return jsonify({'error': f'Post with id {post_id} not found.'}), 404

    data = request.get_json()
    title = data.get('title', post_to_update['title'])
    content = data.get('content', post_to_update['content'])

    post_to_update['title'] = title
    post_to_update['content'] = content

    return jsonify({
        'id': post_id,
        'title': title,
        'content': content
    }), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title or content.
    Accepts 'title' and 'content' query parameters.
    Returns list of matching posts.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    matched_posts = []

    for post in POSTS:
        title_match = title_query and title_query in post['title'].lower()
        content_match = content_query and content_query in post['content'].lower()

        if title_match or content_match:
            matched_posts.append(post)

    return jsonify(matched_posts), 200




SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
