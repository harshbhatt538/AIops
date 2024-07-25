-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: usresdb
-- ------------------------------------------------------
-- Server version	8.4.0

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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL,
  `user_role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'test','bhattharsh538@gmail.com','pbkdf2:sha256:600000$86l2DvqUPdoRvfYw$611684ceb8d2eb8c9c67c80e25d39ec533cb4d9965fe2cd49870df121b6dfa5e','root'),(2,'jakadwangdu','jakadwangdu@gmail.com','pbkdf2:sha256:600000$HeailMDmI56K83pZ$2ae25a85e1860df6de00cd6ecc7603a2a62b26e353fae7ce947da88da94d583e',NULL),(3,'test2','test2@gmail.com','pbkdf2:sha256:600000$uAT6op3XMewSAk8N$40ffd73182fb63476d742958640261ed423454a5e1e0d3c22928a25e5b751d42',NULL),(4,'test3','test3@gmail.com','pbkdf2:sha256:600000$L2QvCyKBbE4Z2x3Y$f98ef6d46be2c6eb2efea0c27493cdb44e93bc994de2e8a16652ef239d2e0883',NULL),(5,'test4','test4@gmail.com','pbkdf2:sha256:600000$vggomxsDxyKU90LL$fe9090477636ab09e464b985729a79c76b208b66633ea3cc74affb6902c501cc',NULL),(6,'test5','test5@gmail.com','pbkdf2:sha256:600000$9c2bBHtvC1Rr34wq$ea0a8d5f523a6db62a7d96ef470901ef9f6793fb9be8ad01ed0bbc53daf9281f',NULL),(7,'test6','test6@gmail.com','pbkdf2:sha256:600000$lu882CzoY53lkJU2$1fc6ea964827c259666f999dd43b71b03b2f0cdee1b345cb040bd9ea384af283',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-16 19:05:47
