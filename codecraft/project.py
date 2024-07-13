import os
import shutil


class ProjectCreator:
    def __init__(self):
        pass

    def create_project(self, project_name, template_repo):
        # Create project directory
        project_dir = os.path.join(project_name)
        os.makedirs(project_dir, exist_ok=True)

        # Create src directory
        src_dir = os.path.join(project_dir, "src")
        os.makedirs(src_dir, exist_ok=True)

        # Download project from GitHub
        for item in template_repo:
            if item["type"] == "dir":
                dir_path = os.path.join(src_dir, item["name"])
                os.makedirs(dir_path, exist_ok=True)
            elif item["type"] == "file":
                file_path = os.path.join(src_dir, item["name"])
                response = requests.get(item["download_url"])
                with open(file_path, "wb") as f:
                    f.write(response.content)

            print(f"Project {project_name} created successfully!")

            # Remove temp directory
            temp_dir = "temp_templates"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)