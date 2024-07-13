import click
import os
import shutil

import requests

from codecraft.template import TemplateFetcher
from codecraft.project import ProjectCreator


class Codecraft:
    def __init__(self):
        self.template_fetcher = TemplateFetcher()
        self.project_creator = ProjectCreator()

    def create_project(self, project_name):
        language = self._choose_language()
        framework = self._choose_framework(language)
        version = self._choose_version(language, framework)
        # Create the project with the chosen language, framework, and version
        print(
            f"Creating project {project_name} with {language}, {framework}, and {version}..."
        )
        template_repo_url = f"https://api.github.com/repos/avinash539/codecraft-template/contents/templates/{language}/{framework}/{version}"
        response = requests.get(template_repo_url)
        if response.status_code == 404:
            print("Error: Repository or file not found.")
            return
        template_repo = response.json()
        self.project_creator.create_project(project_name, template_repo)

    def _choose_language(self):
        languages = ["python", "nodejs"]
        return click.prompt(
            "Choose a language", type=click.Choice(languages, case_sensitive=False)
        )

    def _choose_framework(self, language):
        frameworks = self.template_fetcher.fetch_frameworks(language)
        return click.prompt(
            f"Choose a {language} framework",
            type=click.Choice(frameworks, case_sensitive=False),
        )

    def _choose_version(self, langauae, framework):
        versions = self.template_fetcher.fetch_versions(langauae, framework)
        if not versions:
            print(f"No versions available for {framework}.")
            return ""
        print(f"Choose a version for {framework}:")
        for i, version in enumerate(versions):
            print(f"{i+1}. {version}")
        choice = int(input("Enter the number of your choice: "))
        return versions[choice - 1]


@click.group()
def cli():
    """Codecraft CLI tool"""
    pass


@cli.command()
@click.argument("project_name")
def create(project_name):
    """Create a new project"""
    codecraft = Codecraft()
    codecraft.create_project(project_name)


if __name__ == "__main__":
    cli()
