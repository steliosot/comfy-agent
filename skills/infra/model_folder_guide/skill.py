MODEL_FOLDER_GUIDE = {
    "checkpoint": {
        "folder": "models/checkpoints",
        "loader": "CheckpointLoaderSimple",
        "input_name": "ckpt_name",
    },
    "diffusion_model": {
        "folder": "models/diffusion_models",
        "loader": "UNETLoader",
        "input_name": "unet_name",
    },
    "unet": {
        "folder": "models/diffusion_models",
        "loader": "UNETLoader",
        "input_name": "unet_name",
    },
    "vae": {
        "folder": "models/vae",
        "loader": "VAELoader",
        "input_name": "vae_name",
    },
    "clip": {
        "folder": "models/clip",
        "loader": "CLIPLoader",
        "input_name": "clip_name",
    },
    "lora": {
        "folder": "models/loras",
        "loader": "LoraLoaderModelOnly",
        "input_name": "lora_name",
    },
    "controlnet": {
        "folder": "models/controlnet",
        "loader": "ControlNetLoader",
        "input_name": "control_net_name",
    },
    "embeddings": {
        "folder": "models/embeddings",
        "loader": "Textual inversion embeddings",
        "input_name": "n/a",
    },
    "upscale_model": {
        "folder": "models/upscale_models",
        "loader": "UpscaleModelLoader",
        "input_name": "model_name",
    },
    "ipadapter": {
        "folder": "models/ipadapter",
        "loader": "IPAdapter loaders",
        "input_name": "ipadapter_file",
    },
}


def run(model_type=None):
    if model_type:
        key = str(model_type).strip().lower()
        if key == "diffusion":
            key = "diffusion_model"
        info = MODEL_FOLDER_GUIDE.get(key)
        return {
            "status": "ok" if info else "error",
            "skill": "model_folder_guide",
            "requested_type": key,
            "entry": info,
            "known_types": sorted(MODEL_FOLDER_GUIDE.keys()),
        }

    return {
        "status": "ok",
        "skill": "model_folder_guide",
        "known_types": sorted(MODEL_FOLDER_GUIDE.keys()),
        "mapping": MODEL_FOLDER_GUIDE,
    }
