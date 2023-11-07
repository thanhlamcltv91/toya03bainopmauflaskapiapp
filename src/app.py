"""
00 fork this replit to your replit 

01a do your code
01b your final goal is to hit Run and have all tests PASS IN GREEN

02a git commit push to github repo - view guide https://drive.google.com/file/d/1PZZ2xIlamM0pPtLlbpDodseCKcIVhTzW/view?usp=sharing
02b get url to your git repo in 02a above - we call it :gitrepourl

03 paste :gitrepourl into this google form and submit it
   https://forms.gle/cuxhb8cbYaJLHRYz5
   ma_debai = toya03bainopmauflaskapiapp
"""

#pip install Flask requests (cai dat thu vien can thiet)
from flask import Flask, jsonify, request
import os, requests
#
from src.helper import github_request

app = Flask(__name__)
# Thiết lập cổng mặc định từ biến môi trường hoặc sử dụng cổng 5000 nếu không có biến PORT
port = int(os.environ.get("PORT", 5000))

# API endpoint để lấy thông tin release từ kho GitHub
github_repo_url = "https://api.github.com/repos/pyenv/pyenv"


# /: Trả về một đối tượng JSON rỗng.
@app.route('/', methods=['GET'])
def index():
  return jsonify({})


# /release: Trả về một danh sách các bản phát hành của kho GitHub github.com/pyenv/pyenv. Mỗi bản phát hành có các trường created_at, tag_name, và body.
@app.route('/release', methods=['GET'])
def get_releases():
  try:
    response = requests.get(f"{github_repo_url}/releases")
    releases = response.json()
    formatted_releases = [{
        "created_at": release["created_at"],
        "tag_name": release["tag_name"],
        "body": release["body"]
    } for release in releases]
    return jsonify(formatted_releases)
  except requests.exceptions.RequestException:
    return jsonify({}), 404


# /most_3_recent/release: Trả về 3 bản phát hành mới nhất của endpoint /release.
@app.route('/most_3_recent/release', methods=['GET'])
def get_most_recent_releases():
  try:
    response = requests.get(f"{github_repo_url}/releases")
    releases = response.json()
    sorted_releases = sorted(releases,
                             key=lambda x: x["created_at"],
                             reverse=True)
    most_recent_releases = sorted_releases[:3]
    formatted_releases = [{
        "created_at": release["created_at"],
        "tag_name": release["tag_name"],
        "body": release["body"]
    } for release in most_recent_releases]
    return jsonify(formatted_releases)
  except requests.exceptions.RequestException:
    return jsonify({}), 404


if __name__ == '__main__':
  app.run(debug=True, port=port)
