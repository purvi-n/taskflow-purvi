import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=headers,
    )
    project_id = proj_resp.json()["id"]
    
    response = await client.post(
        f"/projects/{project_id}/tasks",
        json={"title": "Test Task"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["project_id"] == project_id

@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=headers,
    )
    project_id = proj_resp.json()["id"]
    
    await client.post(
        f"/projects/{project_id}/tasks",
        json={"title": "Test Task 1"},
        headers=headers,
    )
    await client.post(
        f"/projects/{project_id}/tasks",
        json={"title": "Test Task 2"},
        headers=headers,
    )
    
    response = await client.get(
        f"/projects/{project_id}/tasks",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Task 1"
    assert data[1]["title"] == "Test Task 2"

@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=headers,
    )
    project_id = proj_resp.json()["id"]
    
    task_resp = await client.post(
        f"/projects/{project_id}/tasks",
        json={"title": "Test Task"},
        headers=headers,
    )
    task_id = task_resp.json()["id"]
    
    response = await client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "status": "in_progress"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "in_progress"

@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=headers,
    )
    project_id = proj_resp.json()["id"]
    
    task_resp = await client.post(
        f"/projects/{project_id}/tasks",
        json={"title": "Test Task"},
        headers=headers,
    )
    task_id = task_resp.json()["id"]
    
    response = await client.delete(
        f"/tasks/{task_id}",
        headers=headers,
    )
    assert response.status_code == 204
    
    # Verify deleted
    get_resp = await client.get(
        f"/tasks/{task_id}",
        headers=headers,
    )
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=headers,
    )
    project_id = proj_resp.json()["id"]
    
    response = await client.patch(
        f"/projects/{project_id}",
        json={"name": "Updated Project"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Project"

@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post(
        "/projects/",
        json={"name": "Test Project"},
        headers=headers,
    )
    project_id = proj_resp.json()["id"]
    
    response = await client.delete(
        f"/projects/{project_id}",
        headers=headers,
    )
    assert response.status_code == 204
    
    # Verify deleted
    get_resp = await client.get(
        f"/projects/{project_id}",
        headers=headers,
    )
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_list_projects_pagination(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    await client.post("/projects/", json={"name": "Proj 1"}, headers=headers)
    await client.post("/projects/", json={"name": "Proj 2"}, headers=headers)
    await client.post("/projects/", json={"name": "Proj 3"}, headers=headers)
    
    resp1 = await client.get("/projects/?page=1&limit=2", headers=headers)
    assert resp1.status_code == 200
    assert len(resp1.json()) == 2
    
    resp2 = await client.get("/projects/?page=2&limit=2", headers=headers)
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1

@pytest.mark.asyncio
async def test_list_tasks_pagination(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post("/projects/", json={"name": "Test Project"}, headers=headers)
    project_id = proj_resp.json()["id"]
    
    await client.post(f"/projects/{project_id}/tasks", json={"title": "Task 1"}, headers=headers)
    await client.post(f"/projects/{project_id}/tasks", json={"title": "Task 2"}, headers=headers)
    await client.post(f"/projects/{project_id}/tasks", json={"title": "Task 3"}, headers=headers)
    
    resp1 = await client.get(f"/projects/{project_id}/tasks?page=1&limit=2", headers=headers)
    assert resp1.status_code == 200
    assert len(resp1.json()) == 2
    
    resp2 = await client.get(f"/projects/{project_id}/tasks?page=2&limit=2", headers=headers)
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1

@pytest.mark.asyncio
async def test_project_stats(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    proj_resp = await client.post("/projects/", json={"name": "Test Project"}, headers=headers)
    project_id = proj_resp.json()["id"]
    
    await client.post(f"/projects/{project_id}/tasks", json={"title": "Task 1", "status": "todo"}, headers=headers)
    await client.post(f"/projects/{project_id}/tasks", json={"title": "Task 2", "status": "in_progress"}, headers=headers)
    await client.post(f"/projects/{project_id}/tasks", json={"title": "Task 3", "status": "done"}, headers=headers)
    
    response = await client.get(f"/projects/{project_id}/stats", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status_counts"]["todo"] == 1
    assert data["status_counts"]["in_progress"] == 1
    assert data["status_counts"]["done"] == 1

