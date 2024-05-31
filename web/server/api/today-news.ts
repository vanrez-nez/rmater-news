import sqlite3 from "sqlite3";

export default defineEventHandler(async (event) => {
  // open sqlite db from file system at storage/news.db
  const db = new sqlite3.Database('storage/scraper.db');

  async function getNews() {
    return new Promise((resolve, reject) => {
      db.all(`
        SELECT a.*,
          GROUP_CONCAT(l.id ORDER BY l.rank_address) AS location_ids,
          GROUP_CONCAT(l.name ORDER BY l.rank_address) AS location_names,
          GROUP_CONCAT(l.rank_address ORDER BY l.rank_address) AS location_rank_addresses,
          GROUP_CONCAT(l.latitude ORDER BY l.rank_address) AS location_latitudes,
          GROUP_CONCAT(l.longitude ORDER BY l.rank_address) AS location_longitudes
        FROM articles a
        JOIN article_locations al ON a.id = al.article_id
        JOIN locations l ON al.location_id = l.id
        WHERE a.published_time > datetime("now", "-24 hours", "utc")
        AND a.published_time <= datetime("now", "utc")
        GROUP BY a.id
        ORDER BY a.published_time DESC;
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