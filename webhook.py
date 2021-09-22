import json
from discord_webhook import *
from config import webhook_url


class Webhook():
    def __init__(self, data) -> None:
        # green = 0x4caf50
        # red = 0xff5252
        self.data = data
        self.webhook_url = webhook_url
        self.webhook = DiscordWebhook(
            url=self.webhook_url, content='||@everyone||')

        self.embed = DiscordEmbed(
            title=self.data['coin_currency'],
            description=f'**{self.getEmbedText()}: `{self.data["value"]}`**',
            color=self.chooseColor()
        )
        self.embed.set_timestamp()

        thumbnail_url = self.chooseThumbnail()
        if thumbnail_url is not None:
            self.embed.set_thumbnail(url=thumbnail_url)

        self.webhook.add_embed(self.embed)

    def getEmbedText(self):
        if self.data['color'] == 'green':
            value = 'BUY'
        elif self.data['color'] == 'red':
            value = 'SELL'
        else:
            value = 'value'
        return value

    def chooseThumbnail(self):
        with open('charts.json', encoding='UTF-8') as file:
            charts = json.load(file)

        thumbnail_url = None
        for i in charts:
            if self.data['coin_currency'] == i:
                if 'thumbnail_url' in charts[i]:
                    thumbnail_url = charts[i]['thumbnail_url']
                    return thumbnail_url
        else:
            return thumbnail_url

    def chooseColor(self):
        if self.data['color'] == 'green':
            return 0x4caf50
        elif self.data['color'] == 'red':
            return 0xff5252

    def sendMessage(self):
        response = self.webhook.execute()
        return response
