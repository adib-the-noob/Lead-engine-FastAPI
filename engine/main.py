from fastapi import FastAPI, staticfiles
from sqladmin import Admin
from routers import auth
from adminapp import auth as admin_auth

# table creation
from db import Base, engine
from models.user_models import User
from models.profile_models import HrProfile

# admin panel
from adminapp import user_view

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/media", staticfiles.StaticFiles(directory="media", check_dir=False), name="media")

app.include_router(auth.router)

# admin = Admin(app, engine=engine, title="LeadOne Admin Panel", authentication_backend=admin_auth.authentication_backend)

admin = Admin(app, engine=engine, title="LeadOne Admin Panel")
admin.add_view(user_view.UserAdmin)
admin.add_view(user_view.InvitationAdmin)

@app.get("/health")
async def health():
    return {"status": "ok"}
