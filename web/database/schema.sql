/*
 Navicat Premium Data Transfer

 Source Server         : jra
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 02/12/2022 01:19:03
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for alerts
-- ----------------------------
DROP TABLE IF EXISTS "alerts";
CREATE TABLE "alerts" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "content" TEXT,
  "alert_type" integer,
  "created_at" text,
  "alert_server" TEXT,
  "alert_opera" integer
);

-- ----------------------------
-- Table structure for servers
-- ----------------------------
DROP TABLE IF EXISTS "servers";
CREATE TABLE "servers" (
  "id" INTEGER NOT NULL,
  "s_name" TEXT,
  "s_ip" TEXT,
  "s_port" integer,
  "s_username" TEXT,
  "s_pwd" TEXT,
  "m_ip" TEXT,
  "m_port" integer,
  "m_username" TEXT,
  "m_pwd" TEXT,
  "ms_ip" TEXT,
  "ms_port" integer,
  "ms_username" TEXT,
  "ms_pwd" TEXT,
  "o_ip" TEXT,
  "o_port" integer,
  "o_username" TEXT,
  "o_pwd" TEXT,
  "o_db" TEXT,
  "o_type" integer,
  "cpu_threshold" integer,
  "memory_threshold" integer,
  "disk_threshold" integer,
  "table_size_threshold" integer,
  "alert_opera" integer,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name" ,
  "seq" 
);

PRAGMA foreign_keys = true;
