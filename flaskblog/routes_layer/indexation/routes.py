from flask import Blueprint, Response
from flaskblog import db

indexation = Blueprint('indexation', __name__)
@indexation.route('/sitemap.xml')
def sitemap():
    # Define your pages (static or dynamic)
    posts = db.find_documents('posts', {})
    posts = [{"id": post['_id'], **post} for i, post in enumerate(posts)]
    pages = []
    for post in posts:
        pages.append({
            'loc': f"https://www.aipetris.com/post/{post['id']}",
            'lastmod': post['date_posted'].strftime('%Y-%m-%d'),
            'priority': '1.0'
        })

    # Build XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        xml += f'  <url>\n'
        xml += f'    <loc>{page["loc"]}</loc>\n'
        xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')