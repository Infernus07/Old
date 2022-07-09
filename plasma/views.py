from contextlib import suppress

import nextcord

__all__ = (
    "Confirmation",
    "Pagination"
)


class Confirmation(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.result = None
        self.ctx = ctx

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't use this!", ephemeral=True)
            return False
        return True

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(self, button, interaction):
        await interaction.response.defer()
        await self.message.edit(view=None)
        self.result = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(self, button, interaction):
        await interaction.response.defer()
        await self.message.edit(view=None)
        await self.ctx.channel.send("Aborted.")
        self.result = False
        self.stop()

    async def on_timeout(self):
        with suppress(nextcord.NotFound):
            await self.message.edit(view=None)
        await self.ctx.channel.send("Time's up. Aborted.")


class Pagination(nextcord.ui.View):
    def __init__(self, ctx, pages):
        super().__init__(timeout=80)
        self.paging = 0
        self.ctx = ctx
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