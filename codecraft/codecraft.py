import os
import shutil
import click
import json
from abc import ABC, abstractmethod


class ConfigLoader:
    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def get_project_structure(self):
        return self.config.get("project_structure", {})

    def get_database_module_path(self, db_type, driver_type):
        return (
            self.config.get("modules", {})
            .get("database", {})
            .get(db_type, {})
            .get(driver_type, "")
        )

    def get_module_files(self, module_type):
        return self.config.get("modules", {}).get(module_type, {}).get("files", [])


class ProjectCreator:
    def __init__(self, project_name, config_loader):
        self.project_name = project_name
        self.config_loader = config_loader

    def create_project(self):
        project_path = os.path.join(os.getcwd(), self.project_name)
        if os.path.exists(project_path):
            click.echo(f"Project '{self.project_name}' already exists.")
            return

        os.makedirs(project_path, exist_ok=True)
        self._create_directories(project_path)
        self._create_files(project_path)

        # Interactive database module creation
        if click.confirm("Do you want to create a database module?"):
            db_type = click.prompt(
                "What database do you want to use?",
                type=click.Choice(["mongodb", "SQL"], case_sensitive=False),
            )
            if db_type == "mongodb":
                driver_type = click.prompt(
                    "What driver do you want to use?",
                    type=click.Choice(
                        ["pymongo", "motor", "mongoose"], case_sensitive=False
                    ),
                )
                self._create_database_module(project_path, db_type, driver_type)

        # Interactive module creation
        while click.confirm("Do you want to create a new module?"):
            module_type = click.prompt(
                "What type of module do you want to create?",
                type=click.Choice(
                    ["database", "service", "repository"], case_sensitive=False
                ),
            )
            module_name = click.prompt("Enter the module name")
            self._create_module(project_path, module_type, module_name)

    def _create_directories(self, project_path):
        for dir in self.config_loader.get_project_structure().get("directories", []):
            dir_path = os.path.join(
                project_path, dir.replace("{project_name}", self.project_name)
            )
            os.makedirs(dir_path, exist_ok=True)

    def _create_files(self, project_path):
        for file in self.config_loader.get_project_structure().get("files", []):
            file_path = os.path.join(
                project_path, file["path"].replace("{project_name}", self.project_name)
            )
            with open(file_path, "w") as f:
                f.write(file["content"])

    def _create_database_module(self, project_path, db_type, driver_type):
        db_module_path = self.config_loader.get_database_module_path(
            db_type, driver_type
        )
        if os.path.exists(db_module_path):
            for root, dirs, files in os.walk(db_module_path):
                for dir in dirs:
                    dir_path = os.path.join(
                        project_path,
                        "src",
                        self.project_name,
                        "v1",
                        "frameworks",
                        "database",
                        dir,
                    )
                    os.makedirs(dir_path, exist_ok=True)
                for file in files:
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(
                        project_path,
                        "src",
                        self.project_name,
                        "v1",
                        "frameworks",
                        "database",
                        file,
                    )
                    shutil.copyfile(src_file_path, dest_file_path)
        else:
            click.echo(f"Database module path '{db_module_path}' does not exist.")

    def _create_module(self, project_path, module_type, module_name):
        module_files = self.config_loader.get_module_files(module_type)
        module_dir = os.path.join(
            project_path, "src", self.project_name, "v1", module_type, module_name
        )
        os.makedirs(module_dir, exist_ok=True)
        for file in module_files:
            file_path = os.path.join(module_dir, file)
            with open(file_path, "w") as f:
                f.write("")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_name")
@click.option(
    "--config",
    default="codecraft/config/fastapi_config.json",
    help="Path to the configuration file",
)
def fastapi(project_name, config):
    """Create a FastAPI project structure."""
    config_loader = ConfigLoader(config)
    creator = ProjectCreator(project_name, config_loader)
    creator.create_project()
    click.echo(f"FastAPI project '{project_name}' created successfully.")


@cli.command()
@click.argument("project_name")
@click.option(
    "--config",
    default="codecraft/config/nestjs_config.json",
    help="Path to the configuration file",
)
def nestjs(project_name, config):
    """Create a NestJS project structure."""
    config_loader = ConfigLoader(config)
    creator = ProjectCreator(project_name, config_loader)
    creator.create_project()
    click.echo(f"NestJS project '{project_name}' created successfully.")


@cli.command()
@click.argument("project_name")
@click.option(
    "--config",
    default="codecraft/config/django_config.json",
    help="Path to the configuration file",
)
def django(project_name, config):
    """Create a Django project structure."""
    config_loader = ConfigLoader(config)
    creator = ProjectCreator(project_name, config_loader)
    creator.create_project()
    click.echo(f"Django project '{project_name}' created successfully.")


if __name__ == "__main__":
    cli()
