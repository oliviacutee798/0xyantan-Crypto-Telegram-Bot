const { Telegraf } = require('telegraf');
const axios = require('axios');
const moment = require('moment');

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply('Welcome to CryptoGecko Bot. Type /help for a list of commands.');
});

bot.help((ctx) => {
  ctx.reply('/price <coin>: Get the price of a coin in USD\n/chart <coin>: Get the 7-day chart for a coin\n/news <coin>: Get the latest news for a coin\n/list: List all available coins');
});

bot.command('price', async (ctx) => {
  const coin = ctx.message.text.split(' ')[1];
  const data = await axios.get(`https://api.coingecko.com/api/v3/simple/price?ids=${coin}&vs_currencies=usd`);
  const price = data.data[coin].usd;
  ctx.reply(`Price of ${coin.toUpperCase()}: ${price} USD`);
});

bot.command('chart', async (ctx) => {
  const coin = ctx.message.text.split(' ')[1];
  const from = moment().subtract(7, 'days').unix();
  const to = moment().unix();
  const data = await axios.get(`https://api.coingecko.com/api/v3/coins/${coin}/market_chart/range?id=${coin}&vs_currency=usd&from=${from}&to=${to}`);
  const prices = data.data.prices;
  const chartData = prices.map((price) => {
    return price[1];
  });
  ctx.replyWithPhoto({
    url: `https://quickchart.io/chart?c=${JSON.stringify({
      type: 'line',
      data: {
        datasets: [
          {
            data: chartData
          }
        ]
      }
    })}`
  });
});

bot.command('news', async (ctx) => {
  const coin = ctx.message.text.split(' ')[1];
  const data = await axios.get(`https://api.coingecko.com/api/v3/coins/${coin}`);
  const coinId = data.data.id;
  const newsData = await axios.get(`https://api.coingecko.com/api/v3/coins/${coinId}/news`);
  const articles = newsData.data.slice(0, 5);
  let reply = '';
  articles.forEach((article, index) => {
    reply += `${index + 1}. <a href="${article.url}">${article.title}</a>\n`;
  });
  ctx.replyWithHTML(`Latest news for ${coin.toUpperCase()}:\n\n${reply}`);
});

bot.command('list', async (ctx) => {
  const data = await axios.get('https://api.coingecko.com/api/v3/coins/list');
  const coins = data.data;
  let reply = '';
  coins.forEach((coin) => {
    reply += `${coin.id}\n`;
  });
  ctx.reply(`List of available coins:\n\n${reply}`);
});

bot.startPolling();
