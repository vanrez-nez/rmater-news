import sqlite3 from "sqlite3";

export default defineEventHandler(async (event) => {
  // open sqlite db from file system at storage/news.db
  const db = new sqlite3.Database('storage/news.db');

  async function getNews() {
    return new Promise((resolve, reject) => {
      db.all('SELECT * FROM entries WHERE date > date("now", "-1 day") ORDER BY datetime(date) DESC', (err:any, rows:any[]) => {
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