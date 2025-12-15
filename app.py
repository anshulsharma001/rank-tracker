"""
Flask Web Application for Google Rank Tracking System
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from typing import List
from main import run_rank_tracking, load_keywords_from_csv
from rank_checker import RankChecker
import config

# Import storage manager based on configuration
if config.STORAGE_TYPE == 'docs':
    from google_docs_manager import GoogleDocsManager
    StorageManager = GoogleDocsManager
elif config.STORAGE_TYPE == 'sheets':
    from google_sheets_manager import GoogleSheetsManager
    StorageManager = GoogleSheetsManager
else:
    # Default to Google Docs
    from google_docs_manager import GoogleDocsManager
    StorageManager = GoogleDocsManager

app = Flask(__name__)
CORS(app)

# Suppress Flask output for cleaner API responses
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def index():
    """Serve the main frontend page"""
    return render_template('index.html')


@app.route('/api/check-rankings', methods=['POST'])
def check_rankings():
    """API endpoint to check website rankings"""
    try:
        data = request.json
        
        website_url = data.get('website_url', '').strip()
        keywords = data.get('keywords', [])
        location = data.get('location', 'United States')
        
        if not website_url:
            return jsonify({'error': 'Website URL is required'}), 400
        
        if not keywords or len(keywords) == 0:
            return jsonify({'error': 'At least one keyword is required'}), 400
        
        # Filter out empty keywords
        keywords = [k.strip() for k in keywords if k.strip()]
        
        if not keywords:
            return jsonify({'error': 'At least one valid keyword is required'}), 400
        
        # Initialize rank checker
        try:
            rank_checker = RankChecker()
        except ValueError as e:
            return jsonify({'error': str(e)}), 500
        
        # Check rankings
        results = rank_checker.check_multiple_keywords(
            keywords,
            website_url,
            location
        )
        
        # Save results to storage
        saved = False
        try:
            storage_manager = StorageManager()
            if config.STORAGE_TYPE == 'docs':
                storage_manager.append_results(results)
            else:
                storage_manager.append_results(results, 'Rank Tracking')
            saved = True
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error saving results: {e}")
        
        # Format results for frontend
        formatted_results = []
        for result in results:
            pos = result['ranking_position']
            status = 'success'
            
            if result.get('error'):
                status = 'error'
            elif isinstance(pos, str) and pos.startswith('>'):
                status = 'not_found'
            
            formatted_results.append({
                'keyword': result['keyword'],
                'position': str(pos),
                'found_url': result.get('found_url', ''),
                'status': status,
                'checked_on': result.get('checked_on', ''),
                'serp_title': result.get('serp_title', ''),
                'serp_snippet': result.get('serp_snippet', ''),
                'error': result.get('error')
            })
        
        return jsonify({
            'success': True,
            'results': formatted_results,
            'saved': saved,
            'website_url': website_url,
            'location': location
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """API endpoint to get ranking history"""
    try:
        # History feature reads from Google Docs/Sheets
        try:
            storage_manager = StorageManager()
        except (FileNotFoundError, ValueError) as e:
            # Handle missing token.pickle on cloud platforms
            error_msg = str(e)
            if 'Token file not found on cloud platform' in error_msg or 'Cannot authenticate on cloud platform' in error_msg:
                return jsonify({
                    'success': False,
                    'error': 'Authentication token not found. Please upload token.pickle to Render as a secret file. See deployment guide for instructions.',
                    'details': error_msg,
                    'results': [],
                    'count': 0
                }), 500
            else:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'results': [],
                    'count': 0
                }), 500
        
        try:
            all_results = storage_manager.get_all_results()
        except Exception as e:
            # Handle authentication errors
            error_str = str(e)
            if 'invalid_grant' in error_str.lower() or 'Bad Request' in error_str:
                return jsonify({
                    'success': False,
                    'error': 'Authentication expired. Please re-authenticate by running a rank check first, or delete token.pickle and try again.',
                    'results': [],
                    'count': 0
                }), 401
            raise
        
        # Parse results (skip header row)
        if len(all_results) <= 1:
            return jsonify({
                'success': True,
                'results': [],
                'count': 0
            })
        
        # Filter results based on query parameters
        website_url = request.args.get('website_url', '')
        keyword = request.args.get('keyword', '')
        limit = int(request.args.get('limit', 50))
        
        # Parse rows (assuming tab-separated format)
        formatted_results = []
        for row in all_results[1:]:  # Skip header
            if len(row) < 8:
                continue
            
            row_keyword = row[0] if len(row) > 0 else ''
            row_url = row[1] if len(row) > 1 else ''
            
            # Apply filters
            if website_url and row_url != website_url:
                continue
            if keyword and row_keyword != keyword:
                continue
            
            pos = row[2] if len(row) > 2 else ''
            status = 'success'
            
            if isinstance(pos, str) and pos.startswith('>'):
                status = 'not_found'
            elif not pos or pos == '':
                status = 'error'
            
            formatted_results.append({
                'keyword': row_keyword,
                'website_url': row_url,
                'position': str(pos),
                'found_url': row[3] if len(row) > 3 else '',
                'status': status,
                'checked_on': row[4] if len(row) > 4 else '',
                'serp_title': row[5] if len(row) > 5 else '',
                'serp_snippet': row[6] if len(row) > 6 else '',
                'timestamp': row[4] if len(row) > 4 else ''
            })
            
            if len(formatted_results) >= limit:
                break
        
        return jsonify({
            'success': True,
            'results': formatted_results,
            'count': len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-keywords', methods=['POST'])
def upload_keywords():
    """API endpoint to upload keywords from file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported'}), 400
        
        # Save file temporarily
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            keywords = load_keywords_from_csv(tmp_path)
        finally:
            os.unlink(tmp_path)
        
        if not keywords:
            return jsonify({'error': 'No keywords found in file'}), 400
        
        return jsonify({
            'success': True,
            'keywords': keywords,
            'count': len(keywords)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import sys
    import os
    
    # Use PORT from environment (for Render/Heroku) or default to 8080
    port = int(os.environ.get('PORT', 8080))
    
    # Allow port override via command line
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}. Using default port 8080.")
    
    # Disable debug mode in production
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("Google Rank Tracking System - Web Interface")
    print("="*60)
    print(f"Storage Type: {config.STORAGE_TYPE}")
    print("Starting web server...")
    print(f"Open your browser and go to: http://localhost:{port}")
    print("="*60 + "\n")
    app.run(debug=debug, host='0.0.0.0', port=port)

