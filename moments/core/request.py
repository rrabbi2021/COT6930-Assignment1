from flask import request
from flask_sqlalchemy.record_queries import get_recorded_queries


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        # Cached pages can lead to failed uploads
        if request.method in ('GET', 'HEAD') and response.mimetype == 'text/html':
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'

        for q in get_recorded_queries():
            if q.duration >= app.config['MOMENTS_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: ' f'{q.duration:f}s\n Context: {q.context}\nQuery: {q.statement}\n'
                )
        return response
