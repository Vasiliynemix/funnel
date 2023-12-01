from aiogram import Router, types

router = Router()


@router.message()
async def funnel_zero(message: types.Message):
    await message.answer(text="Нажми на кнопку")
