from contextlib import suppress

import nextcord

__all__ = (
    "Paginator",
)


class Paginator(nextcord.ui.View):
    def __init__(self, context, pages):
        super().__init__(timeout=80)
        self.paging = 0
        self.ctx = context
        self.pages = pages

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use this!", ephemeral=True)
            return False
        return True

    @nextcord.ui.button(emoji="\N{BLACK LEFT-POINTING TRIANGLE}")
    async def backward(self, button, interaction):
        self.paging -= 1
        if self.paging == -1:
            self.paging = len(self.pages) - 1

        await self.message.edit(embed=self.pages[self.paging], view=self)

    @nextcord.ui.button(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}")
    async def forward(self, button, interaction):
        self.paging += 1
        if self.paging == len(self.pages):
            self.paging = 0

        await self.message.edit(embed=self.pages[self.paging], view=self)

    async def on_timeout(self):
        with suppress(nextcord.NotFound):
            await self.message.edit(view=None)