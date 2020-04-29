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
-- Table structure for table `customer_login_detail`
--

DROP TABLE IF EXISTS `customer_login_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_login_detail` (
  `Customer_id` int NOT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `password` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`Customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_login_detail`
--

LOCK TABLES `customer_login_detail` WRITE;
/*!40000 ALTER TABLE `customer_login_detail` DISABLE KEYS */;
INSERT INTO `customer_login_detail` VALUES (1000000001,'libero.at.auctor@Vivamussit.net','1000000001'),(1000000002,'porttitor.eros@Fuscealiquam.co.uk','1000000002'),(1000000003,'molestie@magnased.com','1000000003'),(1000000004,'orci@interdum.net','1000000004'),(1000000005,'risus@duiaugue.ca','1000000005'),(1000000006,'tincidunt.congue@Donec.ca','1000000006'),(1000000007,'augue.Sed.molestie@volutpat.ca','1000000007'),(1000000008,'feugiat.tellus.lorem@purusin.org','1000000008'),(1000000009,'volutpat@feugiatplacerat.com','1000000009'),(1000000010,'eleifend@nonlacinia.net','1000000010'),(1000000011,'eu.nulla@Pellentesqueultriciesdignissim.co.uk','1000000011'),(1000000012,'dignissim.tempor@ornare.org','1000000012'),(1000000013,'neque@sit.net','1000000013'),(1000000014,'Cras.interdum@magnisdis.edu','1000000014'),(1000000015,'Fusce@blanditenim.org','1000000015'),(1000000016,'vitae.purus.gravida@enim.com','1000000016'),(1000000017,'aptent.taciti.sociosqu@lacusvariuset.ca','1000000017'),(1000000018,'semper@ipsumportaelit.org','1000000018'),(1000000019,'Sed@sit.com','1000000019'),(1000000020,'nulla.magna@aliquetmolestie.org','1000000020'),(1000000021,'auctor.quis.tristique@eueleifendnec.ca','1000000021'),(1000000022,'Donec.nibh.enim@nibhenim.co.uk','1000000022'),(1000000023,'sodales@Maecenasiaculis.org','1000000023'),(1000000024,'venenatis.vel.faucibus@dolor.edu','1000000024'),(1000000025,'enim@mollisInteger.net','1000000025'),(1000000026,'laoreet@massa.edu','1000000026'),(1000000027,'euismod@a.ca','1000000027'),(1000000028,'Phasellus.in@erosnectellus.edu','1000000028'),(1000000029,'non@maurisanunc.co.uk','1000000029'),(1000000030,'pretium.neque.Morbi@Vivamusnibh.co.uk','1000000030'),(1000000031,'et.ipsum@consequatlectussit.net','1000000031'),(1000000032,'nibh.vulputate.mauris@neque.net','1000000032'),(1000000033,'pede.Cras.vulputate@morbitristiquesenectus.com','1000000033'),(1000000034,'In.tincidunt.congue@orci.net','1000000034'),(1000000035,'Duis.elementum@nislQuisque.com','1000000035'),(1000000036,'libero.nec@dolor.edu','1000000036'),(1000000037,'varius@nonleo.org','1000000037'),(1000000038,'gravida.nunc.sed@fringilla.org','1000000038'),(1000000039,'sem@nonfeugiat.net','1000000039'),(1000000040,'turpis@urnanec.co.uk','1000000040'),(1000000041,'arcu@ut.co.uk','1000000041'),(1000000042,'quis.diam.Pellentesque@Cras.com','1000000042'),(1000000043,'dictum.ultricies@ut.edu','1000000043'),(1000000044,'tincidunt.congue@mipedenonummy.com','1000000044'),(1000000045,'sit@scelerisque.co.uk','1000000045'),(1000000046,'urna@ipsumprimis.edu','1000000046'),(1000000047,'ultrices@lorem.edu','1000000047'),(1000000048,'feugiat.Sed.nec@iderat.org','1000000048'),(1000000049,'ligula.consectetuer.rhoncus@idmagnaet.ca','1000000049'),(1000000050,'arcu.Sed.eu@ipsumacmi.co.uk','1000000050'),(1000000051,'nec.orci@et.ca','1000000051'),(1000000052,'nonummy.ut.molestie@urnanec.net','1000000052'),(1000000053,'ut.dolor@Phasellusdolorelit.ca','1000000053'),(1000000054,'nostra.per.inceptos@etarcu.edu','1000000054'),(1000000055,'mauris@Duiselementum.ca','1000000055'),(1000000056,'nascetur.ridiculus@mollis.net','1000000056'),(1000000057,'lobortis.risus@nibhvulputate.com','1000000057'),(1000000058,'montes@faucibus.org','1000000058'),(1000000059,'orci@per.co.uk','1000000059'),(1000000060,'Etiam.bibendum@consectetuer.edu','1000000060'),(1000000061,'amet.diam@erat.net','1000000061'),(1000000062,'nec.diam@anteMaecenas.co.uk','1000000062'),(1000000063,'nonummy.ut@adipiscinglacus.co.uk','1000000063'),(1000000064,'dictum.eu.placerat@blandit.net','1000000064'),(1000000065,'egestas@adipiscingfringilla.org','1000000065'),(1000000066,'erat.volutpat@orci.com','1000000066'),(1000000067,'magna.Duis.dignissim@dictum.org','1000000067'),(1000000068,'Curabitur.dictum@risusvariusorci.edu','1000000068'),(1000000069,'id.ante.dictum@augueeu.org','1000000069'),(1000000070,'Nunc.ac.sem@sitametorci.net','1000000070'),(1000000071,'quis@volutpatornarefacilisis.com','1000000071'),(1000000072,'litora@tempus.co.uk','1000000072'),(1000000073,'vel@risusDuis.org','1000000073'),(1000000074,'urna.justo@quispede.org','1000000074'),(1000000075,'enim.Nunc@Quisqueac.net','1000000075'),(1000000076,'Ut.nec@Nullamfeugiat.com','1000000076'),(1000000077,'vulputate.ullamcorper.magna@elitpharetra.edu','1000000077'),(1000000078,'ut.mi.Duis@quismassa.com','1000000078'),(1000000079,'ridiculus.mus.Donec@Aliquamfringillacursus.ca','1000000079'),(1000000080,'libero.Integer.in@Morbineque.ca','1000000080'),(1000000081,'erat.eget@pharetraQuisque.edu','1000000081'),(1000000082,'diam@felisadipiscing.co.uk','1000000082'),(1000000083,'orci@urnanecluctus.co.uk','1000000083'),(1000000084,'Duis.at@elementum.net','1000000084'),(1000000085,'nec@lacusvestibulumlorem.net','1000000085'),(1000000086,'Ut@nisi.com','1000000086'),(1000000087,'semper.egestas.urna@elit.ca','1000000087'),(1000000088,'est@habitantmorbitristique.org','1000000088'),(1000000089,'justo.Proin@primis.co.uk','1000000089'),(1000000090,'at.risus.Nunc@Integeridmagna.net','1000000090'),(1000000091,'neque.et@sed.com','1000000091'),(1000000092,'fringilla@nibhenim.org','1000000092'),(1000000093,'tincidunt.congue@aliquetdiamSed.net','1000000093'),(1000000094,'fringilla.cursus.purus@cursusinhendrerit.edu','1000000094'),(1000000095,'vestibulum.Mauris@odioAliquamvulputate.com','1000000095'),(1000000096,'aliquet@mauris.org','1000000096'),(1000000097,'leo@parturientmontes.net','1000000097'),(1000000098,'Fusce@maurissit.org','1000000098'),(1000000099,'mauris.a@ut.co.uk','1000000099'),(1000000100,'sem@tinciduntDonecvitae.edu','1000000100');
/*!40000 ALTER TABLE `customer_login_detail` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-28 12:13:53
