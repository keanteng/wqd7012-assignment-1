from huggingface_hub import login, HfApi
import os
from dotenv import load_dotenv

# Login to Hugging Face Hub
load_dotenv()
token = os.getenv("HUGGING_FACE_TOKEN")
login(token=token)

# create or check the repository
from huggingface_hub import create_repo, Repository
repo_name = "keanteng/wqd7012"
create_repo(repo_name, exist_ok=True)

# upload the model to Hugging Face Hub
api = HfApi()
api.upload_folder(
    repo_id=repo_name,
    folder_path="model",
    commit_message="Upload model files",
    repo_type="space",
    path_in_repo="model"
)

# upload the requirements.txt file
api.upload_file(
    repo_id=repo_name,
    path_or_fileobj="requirements.txt",
    path_in_repo="requirements.txt",
    commit_message="Upload requirements.txt",
    repo_type="space"
)

# upload the data/means_stds.csv file
api.upload_file(
    repo_id=repo_name,
    path_or_fileobj="data/means_stds.csv",
    path_in_repo="data/means_stds.csv",
    commit_message="Upload means_stds.csv",
    repo_type="space"
)

# upload the src/classifier.py file
api.upload_file(
    repo_id=repo_name,
    path_or_fileobj="src/classifier.py",
    path_in_repo="src/classifier.py",
    commit_message="Upload classifier.py",
    repo_type="space"
)

# upload the app.py file
api.upload_file(
    repo_id=repo_name,
    path_or_fileobj="app.py",
    path_in_repo="app.py",
    commit_message="Upload app.py",
    repo_type="space"
)

print("Deployment to Hugging Face Hub completed successfully!")
print(f"Model and files are available at: https://huggingface.co/{repo_name}")