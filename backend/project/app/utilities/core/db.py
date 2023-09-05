import random
from datetime import date

# from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models


HASHED_PASSWORD = "$2b$12$Q4zyTXf.dvJ7RjWZ/AqqxuFHI2yjvNyPEkr2yFTBGfmGCQbRkrMlK"


async def fill_db(db: AsyncSession) -> None:
    super_user = models.UserDB(
        email="user@example.com",
        password=HASHED_PASSWORD,
        verified=True,
        sudo=True,
    )
    tier_pro = models.TierDB(
        name="Pro",
        price=1000,
        duration=1,
        description="Pro tier with unlimited access",
        api_call_limit=100,
    )
    store = models.StoreDB(name="Aldi", city="Brunssum", country="NL")
    async with db as sess:
        sess.add(super_user)
        sess.add(tier_pro)
        sess.add(store)
        await sess.commit()

    # await create_mock_users(db)
    # all_mock_users = await read_all_mock_users(db)
    # await create_mock_items(db, all_mock_users)
    # # await create_mock_login_records(db, all_mock_users)
    # # await create_mock_refresh_token_records(db, all_mock_users)
    # await create_mock_subscription(db, all_mock_users)


async def create_mock_users(db: AsyncSession):
    mock_users = []
    for i in range(30):
        mock_user = models.UserDB(
            email=f"user{i + random.randint(1,4000)}@fake.lan",
            password="roflroflrofl",
            verified=True,
        )
        mock_users.append(mock_user)

    async with db as session:
        session.add_all(mock_users)
        await session.commit()


async def read_all_mock_users(db: AsyncSession):
    async with db as session:
        sudo_user = await crud.user.get(session, 1)
        if sudo_user is None:
            return
        all_mock_users = await crud.user.get_multi(session, sudo_user)
        return all_mock_users


async def create_mock_items(db: AsyncSession, users: list[models.UserDB]):
    async with db as session:
        for user in users:
            for _ in range(random.randint(0, 10)):
                random_name = f"ITEM_{str(uuid4())}"
                mock_item = models.ItemCreate(name=random_name, description=random_name)
                await crud.item.create(session, mock_item, user)


async def create_mock_login_records(db: AsyncSession, users: list[models.UserDB]):
    async with db as session:
        for user in users:
            for _ in range(random.randint(1, 3)):
                mock_login_record = models.LoginHistoryCreate(
                    ip_address=f"10.0.0.{random.randint(0, 255)}",
                    fresh=bool(random.randint(0, 1)),
                )
                await crud.login_history.create(session, mock_login_record, user)


async def create_mock_refresh_token_records(
    db: AsyncSession, users: list[models.UserDB]
):
    async with db as session:
        for user in users:
            for _ in range(random.randint(1, 3)):
                mock_refresh_token = models.RefreshTokenCreate(jti=str(uuid4()))
                await crud.refresh_token.create(session, mock_refresh_token, user)


async def create_mock_subscription(db: AsyncSession, users: list[models.UserDB]):
    async with db as session:
        sudo_user = users[0]
        tiers = await crud.tier.get_multi(session, sudo_user)
        one_day_ago = date.today() - timedelta(days=1)
        two_days_ago = date.today() - timedelta(days=2)
        start_dates = [one_day_ago, two_days_ago]
        for user in users:
            start_date = random.choice(start_dates)
            tier = random.choice(tiers)
            mock_subscription = models.SubscriptionDB(
                start_date=start_date,
                end_date=start_date + timedelta(days=tier.duration),
                tier_id=tier.id,
                active=True,
                user_id=user.id,
            )
            session.add(mock_subscription)
            await session.commit()
