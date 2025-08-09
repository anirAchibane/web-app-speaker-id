from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth_api:app", host="0.0.0.0", port=8000, reload=True)