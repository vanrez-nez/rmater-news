import sqlite3 from "sqlite3";

export default defineEventHandler(async (event) => {
  // open sqlite db from file system at storage/news.db
  const db = new sqlite3.Database('storage/scraper.db');

  async function getNews() {
    return new Promise((resolve, reject) => {
      db.all(`
        SELECT * FROM articles
        WHERE published_time > datetime("now", "-24 hours", "utc") AND published_time <= datetime("now", "utc")
        ORDER BY datetime(published_time) DESC
        `, (err:any, rows:any[]) => {
        if (err) {
          reject(err);
        }
        resolve(rows);
      });
    });
  }
  // select all rows from news table
  return await getNews();
})