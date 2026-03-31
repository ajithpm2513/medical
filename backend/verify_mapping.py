from app.services.model_loader import ModelManager
manager = ModelManager()
models = manager.get_local_models()
for m in models:
    print(f"{m['id']} -> {m['architecture']}")
