CREATE DATABASE  IF NOT EXISTS `bank` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bank`;
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: bank
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `startups`
--

DROP TABLE IF EXISTS `startups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `startups` (
  `su_id` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `su_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `account_id` int NOT NULL,
  `date_till_Account_valid` date NOT NULL,
  `date_created` date NOT NULL,
  `bank_balance` int NOT NULL,
  `sales_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `registered_email` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `registered_photo` int NOT NULL,
  `linked_accounts` int NOT NULL,
  `locations(state)` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `size` varchar(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `tax_owned` int NOT NULL,
  PRIMARY KEY (`su_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `startups`
--

LOCK TABLES `startups` WRITE;
/*!40000 ALTER TABLE `startups` DISABLE KEYS */;
INSERT INTO `startups` VALUES ('STUP10000','Blythe',1000000000,'2019-02-07','2020-03-02',1000000,'Hygeine','diam.Pellentesque.habitant@Cras.net',12,2000000001,'Delhi','A',84998),('STUP10001','Coby',1000000001,'2019-02-12','2020-02-15',1000001,'Food','arcu.Aliquam@nullaCraseu.edu',13,2000000000,'Kerala','B',70604),('STUP10002','Samuel',1000000002,'2019-02-10','2020-06-30',1000002,'Fashion','est.Mauris@famesacturpis.net',14,1999999999,'Delhi','C',84182),('STUP10003','Jared',1000000003,'2019-02-05','2021-01-20',1000003,'Travel','Quisque.nonummy.ipsum@Lorem.ca',15,1999999998,'Arunachal','D',5671),('STUP10004','Calvin',1000000004,'2019-02-10','2021-01-31',1000004,'Appliances','et.ultrices.posuere@Donec.com',16,1999999997,'Jammu and Kashmir','E',98677),('STUP10005','Tamara',1000000005,'2019-02-06','2020-07-17',1000005,'Hygeine','Cum.sociis.natoque@Crasegetnisi.org',17,1999999996,'Andhra Pradesh','A',25049),('STUP10006','Kaye',1000000006,'2019-02-14','2020-04-15',1000006,'Food','est.tempor.bibendum@malesuadavel.com',18,1999999995,'Punjab','B',36523),('STUP10007','Beatrice',1000000007,'2019-02-14','2020-12-08',1000007,'Fashion','malesuada@est.org',19,1999999994,'Chhattisgarh','C',11558),('STUP10008','Nicholas',1000000008,'2019-02-08','2020-06-22',1000008,'Travel','euismod@Inornaresagittis.ca',20,1999999993,'Madhya Pradesh','D',80045),('STUP10009','Tyrone',1000000009,'2019-02-06','2020-05-27',1000009,'Appliances','condimentum@sagittisDuis.org',21,1999999992,'Uttar Pradesh','E',49461),('STUP10010','Shad',1000000010,'2019-02-08','2020-12-23',1000000,'Hygeine','amet.ultricies.sem@tristiquepellentesquetellus.org',22,1999999991,'Gujarat','A',6444),('STUP10011','Luke',1000000011,'2019-02-05','2021-01-15',1000001,'Food','vitae.aliquet@variuseteuismod.ca',23,1999999990,'Haryana','B',25602),('STUP10012','Juliet',1000000012,'2019-02-13','2020-11-14',1000002,'Fashion','Integer@ametlorem.co.uk',24,1999999989,'Telangana','C',54504),('STUP10013','Winter',1000000013,'2019-02-05','2020-11-18',1000003,'Travel','tellus@sedpede.net',25,1999999988,'Madhya Pradesh','D',17555),('STUP10014','Ciara',1000000014,'2019-02-13','2020-03-25',1000004,'Appliances','morbi.tristique.senectus@adipiscing.co.uk',26,1999999987,'Tamil Nadu','E',24252),('STUP10015','Adele',1000000015,'2019-02-10','2020-06-11',1000005,'Hygeine','ullamcorper.Duis@idblanditat.org',27,1999999986,'Punjab','A',31495),('STUP10016','Jared',1000000016,'2019-02-05','2020-05-21',1000006,'Food','Nam.consequat@ipsumPhasellusvitae.net',28,1999999985,'Bihar','B',21321),('STUP10017','Hyacinth',1000000017,'2019-02-14','2020-12-05',1000007,'Fashion','consectetuer.ipsum@id.co.uk',29,1999999984,'Gujarat','C',79975),('STUP10018','Len',1000000018,'2019-02-09','2020-08-14',1000008,'Travel','iaculis.lacus@scelerisque.com',30,1999999983,'Jammu and Kashmir','D',52748),('STUP10019','Martina',1000000019,'2019-02-06','2021-01-04',1000009,'Appliances','neque@turpis.ca',31,1999999982,'Kerala','E',25988);
/*!40000 ALTER TABLE `startups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-28 12:13:55
