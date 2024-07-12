import os
import shutil
import click
import json


class ProjectConfig:
    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def get_project_structure(self, project_type):
        return self.config.get(project_type, {})


class ProjectCreator:
    def __init__(self, project_type, project_name, config):
        self.project_type = project_type
        self.project_name = project_name
        self.config = config

    def create_project(self):
        project_path = os.path.join(os.getcwd(), self.project_name)
        if os.path.exists(project_path):
            click.echo(f"Project '{self.project_name}' already exists.")
            return

        os.makedirs(project_path, exist_ok=True)
        self._create_directories(project_path)
        self._create_files(project_path)

    def _create_directories(self, project_path):
        for dir in self.config.get_project_structure(self.project_type).get(
            "directories", []
        ):
            os.makedirs(os.path.join(project_path, dir), exist_ok=True)

    def _create_files(self, project_path):
        for file in self.config.get_project_structure(self.project_type).get(
            "files", []
        ):
            with open(os.path.join(project_path, file["path"]), "w") as f:
                f.write(file["content"])


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_name")
@click.option("--config", default="config.json", help="Path to the configuration file")
def fastapi(project_name, config):
    """Create a FastAPI project structure."""
    config = ProjectConfig(config)
    creator = ProjectCreator("fastapi", project_name, config)
    creator.create_project()
    click.echo(f"FastAPI project '{project_name}' created successfully.")


@cli.command()
@click.argument("project_name")
@click.option("--config", default="config.json", help="Path to the configuration file")
def nestjs(project_name, config):
    """Create a NestJS project structure."""
    config = ProjectConfig(config)
    creator = ProjectCreator("nestjs", project_name, config)
    creator.create_project()
    click.echo(f"NestJS project '{project_name}' created successfully.")


@cli.command()
@click.argument("project_name")
@click.option("--config", default="config.json", help="Path to the configuration file")
def django(project_name, config):
    """Create a Django project structure."""
    config = ProjectConfig(config)
    creator = ProjectCreator("django", project_name, config)
    creator.create_project()
    click.echo(f"Django project '{project_name}' created successfully.")


if __name__ == "__main__":
    cli()
