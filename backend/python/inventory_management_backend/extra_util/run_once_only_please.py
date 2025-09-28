import os

# Project structure definition
structure = {
    "inventory_management_backend": {
        "app": {
            "domain": {
                "models": ["user.py", "product.py"],
                "services": ["inventory_service.py"],
            },
            "application": {
                "use_cases": {
                    "product": [
                        "create_product.py",
                        "get_product.py",
                        "update_product.py",
                        "delete_product.py",
                    ],
                    "user": [
                        "register_user.py",
                        "login_user.py",
                    ],
                },
                "dto": ["product_dto.py", "user_dto.py"],
                "event_handlers": ["inventory_events.py"],
            },
            "ports": [
                "product_repository.py",
                "user_repository.py",
                "event_bus.py",
            ],
            "adapters": {
                "repositories": [
                    "product_repository_impl.py",
                    "user_repository_impl.py",
                ],
                "db": ["base.py", "session.py"],
                "auth": ["jwt_manager.py"],
                "events": ["event_publisher.py"],
            },
            "api": {
                "v1": ["product_router.py", "user_router.py"],
                "files": ["dependencies.py"],
            },
            "config": ["settings.py"],
            "files": ["main.py", "events.py"],
        },
        "tests": {
            "domain": [],
            "application": [],
            "adapters": [],
            "api": [],
            "files": ["conftest.py"],
        },
        "files": ["requirements.txt", "README.md"],
        "alembic": {},
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):  # Folder
            os.makedirs(path, exist_ok=True)

            # Handle files inside dict (if key "files")
            if "files" in content:
                for file in content["files"]:
                    file_path = os.path.join(path, file)
                    with open(file_path, "w") as f:
                        f.write(f"# {file}\n")

            # Recursively handle nested folders
            for sub_name, sub_content in content.items():
                if sub_name != "files":
                    create_structure(path, {sub_name: sub_content})

        elif isinstance(content, list):  # List of files
            os.makedirs(base_path, exist_ok=True)
            for file in content:
                file_path = os.path.join(base_path, file)
                with open(file_path, "w") as f:
                    f.write(f"# {file}\n")

if __name__ == "__main__":
    # Go to parent of the parent directory
    #parent_of_parent = os.path.abspath(os.path.join(os.getcwd(), "../"))
    #create_structure(parent_of_parent, structure)
    #print(f"✅ Project created successfully in: {os.path.join(parent_of_parent, 'inventory_management_backend')}")
    print(f"✅ Not enabled to create project structure.")
