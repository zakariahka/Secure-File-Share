import os
from flask import Blueprint, send_from_directory

HERE = os.path.abspath(os.path.dirname(__file__))
BUILD_DIR = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'frontend', 'build'))

frontend_bp = Blueprint(
    'frontend',
    __name__,
)

@frontend_bp.route('/manifest.json')
def serve_manifest():
    """
    Serve the manifest.json file located at the root of the React build directory.
    """
    return send_from_directory(
        BUILD_DIR,
        'manifest.json'
    )

@frontend_bp.route('/', defaults={'path': ''})
@frontend_bp.route('/<path:path>')
def serve_frontend(path):
    """
    Catch-all route to serve React's index.html for client-side routing.
    Serves static files if they exist, otherwise falls back to index.html.
    """
    if path.startswith('static/'):
        return send_from_directory(os.path.join(BUILD_DIR, 'static'), path[len('static/'):])
    
    if path == 'manifest.json':
        return serve_manifest()
    
    file_path = os.path.join(BUILD_DIR, path)
    
    if os.path.exists(file_path):
        return send_from_directory(BUILD_DIR, path)
    else:
        return send_from_directory(BUILD_DIR, 'index.html')