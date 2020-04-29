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
-- Table structure for table `mnc_and_govtsector`
--

DROP TABLE IF EXISTS `mnc_and_govtsector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mnc_and_govtsector` (
  `comp_id` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `company_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `company type` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `bank` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `bank_branch` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `account_no` int NOT NULL,
  `ifsc_code` varchar(13) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `nature_of_business` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `email_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `contact_no` int NOT NULL,
  `tax_bracket` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date_of_establishment` date DEFAULT NULL,
  PRIMARY KEY (`comp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mnc_and_govtsector`
--

LOCK TABLES `mnc_and_govtsector` WRITE;
/*!40000 ALTER TABLE `mnc_and_govtsector` DISABLE KEYS */;
INSERT INTO `mnc_and_govtsector` VALUES ('COMP100021','A','Public','SBI','100001',1000012123,'SBI12345','Secondary','diam.Pellentesque.habitant@Cras.net',1234567890,'TIER1',NULL),('COMP100022','B','Private','BOB','300001',1000012124,'BOB12346','Tertiary','arcu.Aliquam@nullaCraseu.edu',1234567891,'TIER2',NULL),('COMP100023','C','Joint','HDFC','400001',1000012125,'HDFC12347','Secondary','est.Mauris@famesacturpis.net',1234567892,'TIER3',NULL),('COMP100024','D','Private','HSBC','500001',1000012126,'HSBC12348','Tertiary','Quisque.nonummy.ipsum@Lorem.ca',1234567893,'TIER1',NULL),('COMP100025','E','Joint','PNB','600001',1000012127,'PNB12349','Secondary','et.ultrices.posuere@Donec.com',1234567894,'TIER2',NULL),('COMP100026','F','Public','SBI','100001',1000012128,'SBI12350','Tertiary','Cum.sociis.natoque@Crasegetnisi.org',1234567895,'TIER3',NULL),('COMP100027','G','Private','BOB','300001',1000012129,'BOB12351','Secondary','est.tempor.bibendum@malesuadavel.com',1234567896,'TIER1',NULL),('COMP100028','H','Cooperative','HDFC','400001',1000012130,'HDFC12352','Tertiary','malesuada@est.org',1234567897,'TIER2',NULL),('COMP100029','I','Private','HSBC','500001',1000012131,'HSBC12353','Secondary','euismod@Inornaresagittis.ca',1234567898,'TIER3',NULL),('COMP100030','J','Cooperative','PNB','600001',1000012132,'PNB12354','Tertiary','condimentum@sagittisDuis.org',1234567899,'TIER1',NULL),('COMP100031','K','Public','SBI','100002',1000012133,'SBI12355','Secondary','amet.ultricies.sem@tristiquepellentesquetellus.org',1234567900,'TIER2',NULL),('COMP100032','L','Cooperative','BOB','300002',1000012134,'BOB12356','Tertiary','vitae.aliquet@variuseteuismod.ca',1234567901,'TIER3',NULL),('COMP100033','M','Private','HDFC','400002',1000012135,'HDFC12357','Secondary','Integer@ametlorem.co.uk',1234567902,'TIER1',NULL),('COMP100034','N','Public','HSBC','500002',1000012136,'HSBC12358','Tertiary','tellus@sedpede.net',1234567903,'TIER2',NULL),('COMP100035','O','Private','PNB','600002',1000012137,'PNB12359','Secondary','morbi.tristique.senectus@adipiscing.co.uk',1234567904,'TIER3',NULL),('COMP100036','P','Private','SBI','100002',1000012138,'SBI12360','Tertiary','ullamcorper.Duis@idblanditat.org',1234567905,'TIER1',NULL),('COMP100037','Q','Joint','BOB','300002',1000012139,'BOB12361','Secondary','Nam.consequat@ipsumPhasellusvitae.net',1234567906,'TIER2',NULL),('COMP100038','R','Public','HDFC','400002',1000012140,'HDFC12362','Tertiary','consectetuer.ipsum@id.co.uk',1234567907,'TIER3',NULL),('COMP100039','S','Joint','HSBC','500002',1000012141,'HSBC12363','Secondary','iaculis.lacus@scelerisque.com',1234567908,'TIER1',NULL),('COMP100040','T','Public','PNB','600002',1000012142,'PNB12364','Tertiary','neque@turpis.ca',1234567909,'TIER2',NULL);
/*!40000 ALTER TABLE `mnc_and_govtsector` ENABLE KEYS */;
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
