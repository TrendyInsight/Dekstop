BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "outfit" (
	"id_outfit"	INTEGER,
	"foto"	TEXT,
	PRIMARY KEY("id_outfit" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "jenis_baju" (
	"id_jenis"	INTEGER UNIQUE,
	"atasan"	TEXT,
	"bawahan"	TEXT,
	"kerudung"	TEXT,
	"gamis"	TEXT,
	PRIMARY KEY("id_jenis")
);
CREATE TABLE IF NOT EXISTS "rekomendasi" (
	"id_rekom"	INTEGER UNIQUE,
	"rating"	TEXT,
	"warna"	TEXT,
	"foto_rek"	TEXT,
	PRIMARY KEY("id_rekom")
);
COMMIT;
