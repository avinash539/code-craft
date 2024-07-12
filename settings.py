# settings.py

TEMPLATES = {
    "fastapi": {
        "main_template": '''# src/{app_name}/main.py
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    # Database initialization code here

@app.on_event("shutdown")
async def shutdown_db_client():
    # Database cleanup code here

@app.get("/")
def read_root():
    return {{"Hello": "World"}}
''',
        "pymongo_database_template": '''# src/{app_name}/framework/database/config.py
from pymongo import MongoClient

class Database:
    def __init__(self, db_url):
        self.client = MongoClient(db_url)
        self.db = self.client.get_database()

db = Database("mongodb://localhost:27017/{app_name}")
''',
        "motor_database_template": '''# src/{app_name}/framework/database/config.py
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, db_url):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client.get_database()

db = Database("mongodb://localhost:27017/{app_name}")
''',
        "controller_template": '''# src/{app_name}/v1/controller.py
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/items/")
async def read_items(request: Request):
    items = await request.app.mongodb["items"].find().to_list(1000)
    return items
'''
    },
    "nestjs": {
        "main_template": '''# src/{app_name}/main.ts
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    MongooseModule.forRoot('mongodb://localhost:27017/{app_name}')
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
''',
        "database_template": '''# src/{app_name}/framework/database/config.ts
import { MongooseModule } from '@nestjs/mongoose';

export const DatabaseModule = MongooseModule.forRoot('mongodb://localhost:27017/{app_name}');
''',
        "controller_template": '''# src/{app_name}/v1/controller.ts
import { Controller, Get } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Item } from './item.model';

@Controller('items')
export class AppController {
  constructor(@InjectModel('Item') private itemModel: Model<Item>) {}

  @Get()
  async getItems() {
    return await this.itemModel.find().exec();
  }
}
'''
    }
}

