from contextlib import suppress
import plasma

import nextcord

__all__ = ("Confirmation", "Pagination", "ColorView")


class Confirmation(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.result = None

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
        await self.ctx.send("Aborted.")
        self.result = False
        self.stop()

    async def on_timeout(self):
        with suppress(nextcord.NotFound):
            await self.message.edit(view=None)
            await self.ctx.send("Time's up. Aborted.")


class Pagination(nextcord.ui.View):
    def __init__(self, ctx, pages):
        super().__init__(timeout=80)
        self.ctx = ctx
        self.pages = pages
        self.paging = 0

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


class ColorMenu(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Amaranth",  emoji=f"{plasma.Emoji.amaranth()}"),
            nextcord.SelectOption(label="Blush",     emoji=f"{plasma.Emoji.blush()}"),
            nextcord.SelectOption(label="Fuchsia",   emoji=f"{plasma.Emoji.fuchsia()}"),
            nextcord.SelectOption(label="Ice",       emoji=f"{plasma.Emoji.ice()}"),
            nextcord.SelectOption(label="Indigo",    emoji=f"{plasma.Emoji.indigo()}"),
            nextcord.SelectOption(label="Lilac",     emoji=f"{plasma.Emoji.lilac()}"),
            nextcord.SelectOption(label="Lime",      emoji=f"{plasma.Emoji.lime()}"),
            nextcord.SelectOption(label="Midnight",  emoji=f"{plasma.Emoji.midnight()}"),
            nextcord.SelectOption(label="Obsidian",  emoji=f"{plasma.Emoji.obsidian()}"),
            nextcord.SelectOption(label="Sky",       emoji=f"{plasma.Emoji.sky()}"),
            nextcord.SelectOption(label="Snow",      emoji=f"{plasma.Emoji.snow()}"),
            nextcord.SelectOption(label="Tangerine", emoji=f"{plasma.Emoji.tangerine()}")
        ]
        super().__init__(options=options)

    async def callback(self, interaction):
        for i in plasma.COLOR_ROLES:
            if any(x.name == i for x in interaction.user.roles):
                with suppress(nextcord.NotFound):
                    await interaction.response.defer(ephemeral=True)

                r_role = nextcord.utils.get(interaction.guild.roles, name=i)
                a_role = nextcord.utils.get(interaction.guild.roles, name=self.values[0])
                await interaction.user.remove_roles(r_role)
                await interaction.user.add_roles(a_role)

                embed = nextcord.Embed(
                    color=nextcord.Color.blue(),
                    description=f"Removed `{r_role}`\nAdded `{a_role}`"
                )
                with suppress(nextcord.NotFound):
                    await interaction.followup.send(embed=embed, ephemeral=True)
                return

        with suppress(nextcord.NotFound):
            await interaction.response.defer(ephemeral=True)

        role = nextcord.utils.get(interaction.guild.roles, name=self.values[0])
        await interaction.user.add_roles(role)

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=f"{plasma.Emoji.check()} Added `{role}`"
        )
        with suppress(nextcord.NotFound):
            await interaction.followup.send(embed=embed, ephemeral=True)


class ColorView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ColorMenu())