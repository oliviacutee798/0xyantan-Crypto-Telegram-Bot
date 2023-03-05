const { Telegraf } = require('telegraf')
const axios = require('axios');
const moment = require('moment');
const _ = require('lodash');

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply('Welcome to your new bot!');
});

bot.command('price', async (ctx) => {
  const symbol = ctx.message.text.split(' ')[1];
  if (!symbol) {
    return ctx.reply('Please provide a cryptocurrency symbol, e.g. /price BTC');
  }

  try {
    const response = await axios.get(`https://api.coingecko.com/api/v3/simple/price?ids=${symbol}&vs_currencies=usd`);
    const price = response.data[symbol].usd;
    ctx.reply(`The current price of ${symbol.toUpperCase()} is $${price}`);
  } catch (err) {
    ctx.reply(`Failed to get price data for ${symbol.toUpperCase()}`);
  }
});

let lastNewsTime = moment().subtract(1, 'minute');

setInterval(async () => {
  try {
    const response = await axios.get(`https://cryptopanics.com/api/v1/posts/?auth_token=${process.env.CRYPTOPANICS_API_KEY}&currencies=all&sort_by=date&direction=desc`);
    const news = response.data.results.filter((item) => moment(item.created_at).isAfter(lastNewsTime));

    if (news.length > 0) {
      news.forEach((item) => {
        const message = `${item.title}\n\n${item.url}`;
        bot.telegram.sendMessage(process.env.CHAT_ID, message);
      });
    }
    
    lastNewsTime = moment();

  } catch (err) {
    console.error('Failed to get news data', err);
  }
}, 1000);

bot.command('chart', async (ctx) => {
  const symbol = ctx.message.text.split(' ')[1];
  if (!symbol) {
    return ctx.reply('Please provide a cryptocurrency symbol, e.g. /chart BTC');
  }

  try {
    const response = await axios.get(`https://api.coingecko.com/api/v3/coins/${symbol}/market_chart?vs_currency=usd&days=7&interval=daily`);
    const prices = response.data.prices;
    const dates = prices.map((item) => moment(item[0]).format('MMM D'));
    const values = prices.map((item) => item[1]);

    const chartUrl = `https://quickchart.io/chart?c={type:'line',data:{labels:${JSON.stringify(dates)},datasets:[{label:'${symbol.toUpperCase()}',data:${JSON.stringify(values)}}]}}`;
    ctx.replyWithPhoto({ url: chartUrl });
  } catch (err) {
    ctx.reply(`Failed to get chart data for ${symbol.toUpperCase()}`);
  }
});

bot.launch();
bot.startPolling();
