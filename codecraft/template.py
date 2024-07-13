import requests

from codecraft.constants import TEMPLATE_BASE_URL


class TemplateFetcher:
    def fetch_template_repo(self, language, framework, version):
        # Fetch template repository from GitHub API
        repo_url = f"{TEMPLATE_BASE_URL}/{language}/{framework}/{version}"
        response = requests.get(repo_url)
        return response.json()

    def fetch_frameworks(self, language):
        repo_url = f"https://api.github.com/repos/avinash539/codecraft-template/contents/templates/{language}"
        response = requests.get(repo_url)
        if response.status_code == 200:
            frameworks = [
                item["name"] for item in response.json() if item["type"] == "dir"
            ]
            return frameworks
        else:
            return []

    def fetch_versions(self, language, framework):
        repo_url = f"https://api.github.com/repos/avinash539/codecraft-template/contents/templates/{language}/{framework}"
        response = requests.get(repo_url)
        if response.status_code == 200:
            versions = [
                item["name"] for item in response.json() if item["type"] == "dir"
            ]
            return versions
        else:
            return []