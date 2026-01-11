import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI(title="Recepts")

#use enum for difficulity
class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Category(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DRINK = "drink"
    CAKE = "cake"

class ReceptsBase(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    cooking_time: int = Field("Time in minute")
    difficulty: Difficulty = Difficulty.MEDIUM
    category: Category

class CreateRecept(ReceptsBase):
    pass

class Recepies(ReceptsBase):
    id: str
    created_at: datetime
    views: int = 0
    likes: int = 0

recepies_db: List[Recepies] = []

def init_recepies():
    sample_recepies = [
        Recepies(
            id=str(uuid.uuid4()),
            title="Макароны по флотски",
            description="dinner",
            ingredients=[
                "макароны — 400 г",
                "фарш куриный (свиной, индюшачий) — 500 г",
                "лук репчатый — 1–2 шт",
                "масло растительное — 5–6 ст. л.",
                "перец чёрный молотый",
                "соль",
                "вода"
            ],
            instructions=[
                "Довести воду до кипения, положить соль",
                "Добавить макароны в кипящую воду и варить до полной готовности",
                "Сварившиеся макароны откинуть на дуршлаг и ополоснуть под холодной проточной водой.",
                "Очистить лук от шелухи, тщательно вымыть, нарезать мелкими кубиками.",
                "Разогреть сковороду, добавить растительное масло",
                "Обжарить нарезанный лук на умеренном огне до золотистого цвета и мягкости.",
                "Положить сырой фарш в сковороду и обжаривать, постоянно помешивая, на среднем огне около 10–15 минут",
                "Добавить зелень, соль, перец чёрный молотый.",
                "Обжаренный фарш перемешать с готовыми макаронами."
            ],
            cooking_time=15,
            difficulty=Difficulty.EASY,
            category=Category.DINNER,
            created_at=datetime.now(),
            views=20,
            likes=0,
        ),
        Recepies(
            id=str(uuid.uuid4()),
            title="торт на сковороде",
            description="cake",
            ingredients=[
                "сгущёнка — 380 г (1 банка)",
                "яйцо — 1 шт",
                "мука — 3–4 стакана",
                "разрыхлитель — 1 ч. ложка",
                "сметана — 300 г",
                "сахар — 4 ст. ложки."
            ],
            instructions=[
                "Сгущёнку перелить в глубокую миску, добавить сырое яйцо, перемешать.",
                "Муку всыпать частями, сразу добавить разрыхлитель, замесить тесто.",
                "Разделить тесто на 8 частей, раскатать каждый кусочек по диаметру сковороды. Проколоть вилкой в нескольких местах, чтобы тесто не вздувалось во время жарки.",
                "Жарить коржи на сухой и чистой сковороде на медленном огне с двух сторон.",
                "Когда все коржи будут готовы, обрезать по тарелочке чуть меньшего диаметра. Обрезки не выбрасывать — их нужно подсушить на сковороде и измельчить в кофемолке, а полученной крошкой украсить торт."
            ],
            cooking_time=30,
            difficulty=Difficulty.MEDIUM,
            category=Category.CAKE,
            created_at=datetime.now(),
            views=1240,
            likes=720,
        ),
        Recepies(
            id=str(uuid.uuid4()),
            title="Роллы",
            description="cold",
            ingredients=[
                "рис — 1 пакетик",
                "вода — 10 минут",
                "соль — 0,5 ч. л.",
                "сахар — 0,5 ч. л.",
                "уксус — 1 ст. л.",
                "огурец — 1 шт",
                "лист нори — 2 шт.",
            ],
            instructions=[
                "Рис отварить в воде 10 минут, остудить",
                "Добавить к рису соль и сахар, уксус, перемешать.",
                "Огурец нарезать на полоски, части с семечками не понадобятся.",
                "На циновку поместить лист нори, выложить на него 1/2 часть риса.",
                "Распределить рис по 2/3 части листа.",
                "Поверх риса выложить нарезанный огурец.",
                "Свернуть ролл, второй ролл собрать таким же способом.",
                "Роллы нарезать на порции, подавать с соевым соусом.",
            ],
            cooking_time=20,
            difficulty=Difficulty.EASY,
            category=Category.DINNER,
            created_at=datetime.now(),
            views=2540,
            likes=1503,
        )
    ]

    recepies_db.extend(sample_recepies)

#initialisation
init_recepies()

#first endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to site with Recepies",
            "recepies": "Get /recepies",
            "recepies_detail": "get /recepies/{id}",
            "create_recepies": "Post /recepies",
            "search": "get /recepies/search?q={query}",
            "categories": "get /categories",
            "popular": "get /recepies/popular"}

#all repecies
@app.get("/recepies", response_model=List[Recepies])
async def get_all_recepie(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    filtered = recepies_db

    if category:
        filtered = [r for r in filtered if r.category == category]
    if difficulty:
        filtered = [r for r in filtered if r.difficulty == difficulty]

        return filtered[offset:offset+limit]


#recepies for id
@app.get("/recepies/{recipe_id}") #Returns an error (does not work)
async def get_recepie(recipe_id: str):
    for recipe in recepies_db:
        if recipe.id == recipe_id:
            recipe.views += 1
            return recipe
    raise HTTPException(status_code=404, detail="Recipe is not found")


#add recepies
@app.post("/recepies", response_model=Recepies) # and this
async def create_recipie(recipe_data: CreateRecept):
    recipe_id = str(uuid.uuid4())

    new_recipe = Recepies(
        id = recipe_id,
        created_at= datetime.now(),
        **recipe_data.dict()
    )

    recepies_db.append(new_recipe)
    return new_recipe

#search yhe recept
@app.get("/recipie/search") #work on 50%
async def search_recepie(q: str):
    result = []
    q_lower = q.lower()

    for recipe in recepies_db:
        if q_lower.startswith(recipe.title.lower()) or q_lower in recipe.discription.lower() or any(q_lower in ing.lower() for ing in recipe.ingredients):
            result.append(recipe)
            return result

#category
@app.get("/category")
async def get_category():
    return {
        "available_categories": [cat.value for cat in Category],
        "available_difficulties": [diff.value for diff in Difficulty]
    }

#stat
@app.get("/stats")
async def get_stats():
    total_recipes = len(recepies_db)
    total_views = sum(r.views for r in recepies_db)
    total_likes = sum(r.likes for r in recepies_db)

    return {
        "total_recipes": total_recipes,
        "total_views": total_views,
        "total_likes": total_likes,
        "viewed" : max(recepies_db, key= lambda x: x.views).total if recepies_db else 0,
        "liked": max(recepies_db, key= lambda x: x.likes).total if recepies_db else 0,
    }

#add like
@app.post("/recipies/{recipe_id}/likes")
async def like_recepie(recipe_id: str):
    for recipe in recepies_db:
        if recipe.id == recipe_id:
            recipe.likes += 1
            return {"message": "Like successfully", "total_likes": recipe.likes}
        raise HTTPException (status_code=404, detail="Recipe is not found")

    #good job




