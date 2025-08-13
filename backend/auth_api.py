from email.policy import HTTP
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()

# frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mock DB
users_db = {
    "user@speaker.com":{
        "firstName": "Anir",
        "lastName": "anir",
        "email": "user@speaker.com",
        "password": "user123",
        "admin": False
        },
    "admin@speaker.com":{
        "firstName": "Admin",
        "lastName": "admin",
        "email": "admin@speaker.com",
        "password": "admin123",
        "admin": True
    }
}

datasets_db = {
    "dataset_1": {
        "id": "dataset_1",
        "name": "Speech Dataset 1",
        "description": "Multi-speaker speech dataset with diverse nationalities and genders",
        "speakers": 4,
        "utterances": 16,
        "format": "WAV",
        "size": "45.2 MB",
        "created": "2024-01-15",
        "usage": {
            "training": 12,
            "test": 4
        },
        "path": "/backend/dataset_list/dataset_1",
        "genderDistribution": {
            "male": 2,
            "female": 2
        },
        "nationalityDistribution": {
            "American": 1,
            "Spanish": 1,
            "Chinese": 1,
            "British": 1
        },
        "speakerStructure": [
            {"id": "speaker_001", "videos": ["video_001", "video_002"]},
            {"id": "speaker_002", "videos": ["video_003", "video_004"]},
            {"id": "speaker_003", "videos": ["video_005", "video_006"]},
            {"id": "speaker_004", "videos": ["video_007", "video_008"]}
        ]
    },
    "dataset_2": {
        "id": "dataset_2",
        "name": "Speech Dataset 2",
        "description": "Extended speech dataset with high-quality recordings from multiple speakers",
        "speakers": 4,
        "utterances": 16,
        "format": "WAV",
        "size": "52.8 MB",
        "created": "2024-02-10",
        "usage": {
            "training": 12,
            "test": 4
        },
        "path": "/backend/dataset_list/dataset_2",
        "genderDistribution": {
            "male": 3,
            "female": 1
        },
        "nationalityDistribution": {
            "American": 2,
            "Spanish": 1,
            "Chinese": 1
        },
        "speakerStructure": [
            {"id": "speaker_001", "videos": ["video_001", "video_002"]},
            {"id": "speaker_002", "videos": ["video_003", "video_004"]},
            {"id": "speaker_003", "videos": ["video_005", "video_006"]},
            {"id": "speaker_004", "videos": ["video_007", "video_008"]}
        ]
    }
}

# Models Mock DB
models_db = {
    "model_1": {
        "id": "model_1",
        "name": "SpeakerNet v2.1",
        "version": "2.1.0",
        "dataset_id": "dataset_1",
        "accuracy": 94.5,
        "created_at": "2024-03-15T10:30:00",
        "architecture": "Deep Learning",
        "description": "High-accuracy speaker identification model with deep neural networks",
        "training_duration": "4 hours",
        "size": "85.2 MB",
    },
    "model_2": {
        "id": "model_2",
        "name": "VoiceID Pro",
        "version": "1.5.2",
        "dataset_id": "dataset_1", 
        "accuracy": 91.2,
        "created_at": "2024-02-28T14:15:00",
        "architecture": "Ensemble",
        "description": "Fast and efficient speaker recognition using ensemble methods",
        "training_duration": "2.5 hours",
        "size": "42.8 MB",
    },
    "model_3": {
        "id": "model_3",
        "name": "AudioClassifier",
        "version": "3.0.1",
        "dataset_id": "dataset_2",
        "accuracy": 96.8,
        "created_at": "2024-04-10T09:45:00",
        "architecture": "Transformer",
        "description": "Transformer-based model for speaker and audio classification",
        "training_duration": "6 hours",
        "size": "156.3 MB",
    },
    "model_4": {
        "id": "model_4",
        "name": "SpeakerNet v1.8",
        "version": "1.8.3",
        "dataset_id": "dataset_2",
        "accuracy": 89.7,
        "created_at": "2024-01-20T16:20:00",
        "architecture": "CNN",
        "description": "Convolutional neural network for speaker identification",
        "training_duration": "3 hours",
        "size": "67.4 MB",
    },
    "model_5": {
        "id": "model_5",
        "name": "VoiceRecognizer Plus",
        "version": "2.3.0",
        "dataset_id": "dataset_1",
        "accuracy": 93.1,
        "created_at": "2024-03-05T11:10:00",
        "architecture": "RNN",
        "description": "Recurrent neural network with LSTM layers for voice recognition",
        "training_duration": "5 hours",
        "size": "98.7 MB",
    }
}

# Request bodies
class UserSignup(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    confirmPassword: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    currentEmail: str
    firstName: str
    lastName: str
    email: str

class DeleteAccount(BaseModel):
    email: str

class ModelCreate(BaseModel):
    name: str
    version: str
    dataset_id: str
    accuracy: float
    architecture: str
    description: Optional[str] = None
    training_duration: Optional[str] = None
    model_size: Optional[str] = None

class ModelUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    accuracy: Optional[float] = None
    architecture: Optional[str] = None
    description: Optional[str] = None
    training_duration: Optional[str] = None
    model_size: Optional[str] = None
    status: Optional[str] = None


@app.post("/auth/signup")
async def signup(user: UserSignup):
    # Check if passwords match
    if user.password != user.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Check if user already exists
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user (in real app, hash the password)
    users_db[user.email] = {
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "password": user.password,  # In production, hash this!
        "admin": False  # Default admin value is False
    }
    
    return {"message": "User created successfully", "email": user.email}

@app.post("/auth/login")
async def login(user: UserLogin):
    # if user doesn't exist
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check password
    stored_user = users_db[user.email]
    if stored_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "message": "Login successful",
        "user": {
            "firstName": stored_user["firstName"],
            "lastName": stored_user["lastName"],
            "email": stored_user["email"],
            "admin": stored_user["admin"]
        }
    }

@app.get("/auth/users")
async def get_all_users():
    users_list = []
    for email, user_data in users_db.items():
        users_list.append({
            "firstName": user_data["firstName"],
            "lastName": user_data["lastName"],
            "email": user_data["email"],
            "admin": user_data["admin"]
        })
    return {"users": users_list}

@app.post("/auth/make-admin/{email}")
async def make_admin(email: str):
    
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[email]["admin"] = True
    return {"message": f"User {email} is now an admin"}

@app.post("/auth/remove-admin/{email}")
async def remove_admin(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[email]["admin"] = False
    
    return {"message": f"User {email} is no longer an admin"}

@app.patch("/auth/update-profile")
async def update_profile(user_update: UserUpdate):
    """Update user profile information"""
    current_email = user_update.currentEmail
    
    # Check if user exists
    if current_email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if new email is already taken (if email changed)
    if user_update.email != current_email and user_update.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update user data
    user_data = users_db[current_email]
    user_data["firstName"] = user_update.firstName
    user_data["lastName"] = user_update.lastName
    
    # Handle email change
    if user_update.email != current_email:
        user_data["email"] = user_update.email
        users_db[user_update.email] = user_data
        del users_db[current_email]
    
    return {
        "message": "Profile updated successfully",
        "user": {
            "firstName": user_data["firstName"],
            "lastName": user_data["lastName"],
            "email": user_data["email"],
            "admin": user_data["admin"]
        }
    }

@app.delete("/auth/delete-account")
async def delete_account(delete_request: DeleteAccount):
    """Delete user account"""
    email = delete_request.email
    
    # Check if user exists
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove user from database
    del users_db[email]
    
    return {"message": "Account deleted successfully"}

@app.get("/datasets")
async def get_all_datasets():
    """Get all datasets"""
    datasets_list = list(datasets_db.values())
    return {"datasets": datasets_list}

@app.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    """Get a specific dataset by ID"""
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return {"dataset": datasets_db[dataset_id]}

# Models endpoints
@app.get("/models")
async def get_all_models():
    """Get all models"""
    models_list = list(models_db.values())
    return {"models": models_list}

@app.get("/models/{model_id}")
async def get_model(model_id: str):
    """Get a specific model by ID"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return {"model": models_db[model_id]}

@app.get("/models/dataset/{dataset_id}")
async def get_models_by_dataset(dataset_id: str):
    """Get all models trained on a specific dataset"""
    # Check if dataset exists
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Filter models by dataset_id
    models_for_dataset = [model for model in models_db.values() if model["dataset_id"] == dataset_id]
    
    return {"models": models_for_dataset, "dataset_id": dataset_id}

@app.post("/models")
async def create_model(model: ModelCreate):
    """Create a new model"""
    # Check if dataset exists
    if model.dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Generate new model ID
    model_id = f"model_{len(models_db) + 1}"
    
    # Create model entry
    new_model = {
        "id": model_id,
        "name": model.name,
        "version": model.version,
        "dataset_id": model.dataset_id,
        "accuracy": model.accuracy,
        "created_at": datetime.now().isoformat(),
        "architecture": model.architecture,
        "description": model.description or "",
        "training_duration": model.training_duration or "",
        "model_size": model.model_size or "",
        "status": "active"
    }
    
    models_db[model_id] = new_model
    
    return {"message": "Model created successfully", "model": new_model}

@app.patch("/models/{model_id}")
async def update_model(model_id: str, model_update: ModelUpdate):
    """Update a model"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Update only provided fields
    model_data = models_db[model_id]
    update_data = model_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in model_data:
            model_data[field] = value
    
    return {"message": "Model updated successfully", "model": model_data}

@app.delete("/models/{model_id}")
async def delete_model(model_id: str):
    """Delete a model"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    deleted_model = models_db.pop(model_id)
    
    return {"message": "Model deleted successfully", "deleted_model": deleted_model}

@app.get("/models/active")
async def get_active_models():
    """Get all active models"""
    active_models = [model for model in models_db.values() if model["status"] == "active"]
    return {"models": active_models}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth_api:app", host="0.0.0.0", port=8000, reload=True)