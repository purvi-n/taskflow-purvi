import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash
from sqlalchemy import select

async def seed():
    async with SessionLocal() as db:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == "test@example.com"))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                email="test@example.com",
                name="Test User",
                password=get_password_hash("password123")
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user.email}")
            
        user_id = user.id
        
        # Check if project exists
        result = await db.execute(select(Project).where(Project.name == "Seed Project"))
        project = result.scalar_one_or_none()
        
        if not project:
            project = Project(
                name="Seed Project",
                description="Project created by seed script",
                owner_id=user_id
            )
            db.add(project)
            await db.commit()
            await db.refresh(project)
            print(f"Created project: {project.name}")
        else:
            print(f"Project already exists: {project.name}")
            
        project_id = project.id
        
        # Check if tasks exist
        result = await db.execute(select(Task).where(Task.project_id == project_id))
        tasks = result.scalars().all()
        
        if len(tasks) < 3:
            task1 = Task(
                title="Task 1",
                status=TaskStatus.todo,
                priority=TaskPriority.low,
                project_id=project_id,
                assignee_id=user_id
            )
            task2 = Task(
                title="Task 2",
                status=TaskStatus.in_progress,
                priority=TaskPriority.medium,
                project_id=project_id,
                assignee_id=user_id
            )
            task3 = Task(
                title="Task 3",
                status=TaskStatus.done,
                priority=TaskPriority.high,
                project_id=project_id,
                assignee_id=user_id
            )
            db.add_all([task1, task2, task3])
            await db.commit()
            print("Created 3 tasks")
        else:
            print("Tasks already exist")

if __name__ == "__main__":
    asyncio.run(seed())
