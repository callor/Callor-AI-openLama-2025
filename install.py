###### 필요 디렉토리에서 아래의 .py파일로 모델을 다운받습니다!!#######
from huggingface_hub import snapshot_download
model_id= "MLP-KTLim/llama-3-Korean-Bllossom-8B"
snapshot_download(repo_id=model_id, local_dir="bllossom",
                  local_dir_use_symlinks=False, revision="main")
#####################################################################