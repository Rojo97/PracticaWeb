-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: ssw
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.17.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('1d9c978b3253');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleDispositivo`
--

DROP TABLE IF EXISTS `detalleDispositivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalleDispositivo` (
  `grupoID` int(11) NOT NULL,
  `disID` int(11) NOT NULL,
  PRIMARY KEY (`grupoID`,`disID`),
  KEY `ix_detalleDispositivo_disID` (`disID`),
  KEY `ix_detalleDispositivo_grupoID` (`grupoID`),
  CONSTRAINT `detalleDispositivo_ibfk_1` FOREIGN KEY (`disID`) REFERENCES `dispositivo` (`disID`),
  CONSTRAINT `detalleDispositivo_ibfk_2` FOREIGN KEY (`grupoID`) REFERENCES `grupo` (`grupoID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleDispositivo`
--

LOCK TABLES `detalleDispositivo` WRITE;
/*!40000 ALTER TABLE `detalleDispositivo` DISABLE KEYS */;
INSERT INTO `detalleDispositivo` VALUES (1,1),(1,2),(1,3),(1,6);
/*!40000 ALTER TABLE `detalleDispositivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleMiembro`
--

DROP TABLE IF EXISTS `detalleMiembro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalleMiembro` (
  `grupoID` int(11) NOT NULL,
  `nickname` varchar(10) NOT NULL,
  PRIMARY KEY (`grupoID`,`nickname`),
  KEY `ix_detalleMiembro_grupoID` (`grupoID`),
  KEY `ix_detalleMiembro_nickname` (`nickname`),
  CONSTRAINT `detalleMiembro_ibfk_1` FOREIGN KEY (`grupoID`) REFERENCES `grupo` (`grupoID`),
  CONSTRAINT `detalleMiembro_ibfk_2` FOREIGN KEY (`nickname`) REFERENCES `usuario` (`nickname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleMiembro`
--

LOCK TABLES `detalleMiembro` WRITE;
/*!40000 ALTER TABLE `detalleMiembro` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalleMiembro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispositivo`
--

DROP TABLE IF EXISTS `dispositivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dispositivo` (
  `disID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estado` float NOT NULL,
  `clase` varchar(40) NOT NULL,
  `funcion` varchar(20) NOT NULL,
  PRIMARY KEY (`disID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispositivo`
--

LOCK TABLES `dispositivo` WRITE;
/*!40000 ALTER TABLE `dispositivo` DISABLE KEYS */;
INSERT INTO `dispositivo` VALUES (1,'asd','Actuador',0,'','Luminosidad'),(2,'asdq','Sensor',0,'','Persianas'),(3,'asdq1','Actuador',0,'','Temperatura'),(4,'asdasdfasdg','Actuador',0,'','Temperatura'),(5,'asdasdfasdg','Actuador',0,'','Temperatura'),(6,'asdasdfasdg','Actuador',0,'','Temperatura');
/*!40000 ALTER TABLE `dispositivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupo`
--

DROP TABLE IF EXISTS `grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo` (
  `grupoID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `descripccion` varchar(200) DEFAULT NULL,
  `clase` varchar(40) NOT NULL,
  PRIMARY KEY (`grupoID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo`
--

LOCK TABLES `grupo` WRITE;
/*!40000 ALTER TABLE `grupo` DISABLE KEYS */;
INSERT INTO `grupo` VALUES (1,'grupo','un grupo','');
/*!40000 ALTER TABLE `grupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicion`
--

DROP TABLE IF EXISTS `medicion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicion` (
  `medID` int(11) NOT NULL AUTO_INCREMENT,
  `disID` int(11) DEFAULT NULL,
  `valor` float NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`medID`),
  KEY `ix_medicion_disID` (`disID`),
  CONSTRAINT `medicion_ibfk_1` FOREIGN KEY (`disID`) REFERENCES `dispositivo` (`disID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicion`
--

LOCK TABLES `medicion` WRITE;
/*!40000 ALTER TABLE `medicion` DISABLE KEYS */;
/*!40000 ALTER TABLE `medicion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programaGrupo`
--

DROP TABLE IF EXISTS `programaGrupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programaGrupo` (
  `progGID` int(11) NOT NULL AUTO_INCREMENT,
  `grupoID` int(11) DEFAULT NULL,
  `nombre` varchar(20) NOT NULL,
  `descripccion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`progGID`),
  KEY `ix_programaGrupo_grupoID` (`grupoID`),
  CONSTRAINT `programaGrupo_ibfk_1` FOREIGN KEY (`grupoID`) REFERENCES `grupo` (`grupoID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programaGrupo`
--

LOCK TABLES `programaGrupo` WRITE;
/*!40000 ALTER TABLE `programaGrupo` DISABLE KEYS */;
/*!40000 ALTER TABLE `programaGrupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programaIndividual`
--

DROP TABLE IF EXISTS `programaIndividual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programaIndividual` (
  `progIID` int(11) NOT NULL AUTO_INCREMENT,
  `progGID` int(11) DEFAULT NULL,
  `disID` int(11) DEFAULT NULL,
  `valor` float NOT NULL,
  `fechaIni` date NOT NULL,
  `fechaFin` date NOT NULL,
  PRIMARY KEY (`progIID`),
  KEY `ix_programaIndividual_disID` (`disID`),
  KEY `ix_programaIndividual_progGID` (`progGID`),
  CONSTRAINT `programaIndividual_ibfk_1` FOREIGN KEY (`disID`) REFERENCES `dispositivo` (`disID`),
  CONSTRAINT `programaIndividual_ibfk_2` FOREIGN KEY (`progGID`) REFERENCES `programaGrupo` (`progGID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programaIndividual`
--

LOCK TABLES `programaIndividual` WRITE;
/*!40000 ALTER TABLE `programaIndividual` DISABLE KEYS */;
/*!40000 ALTER TABLE `programaIndividual` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `nickname` varchar(10) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `contraseña` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`nickname`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-25  0:49:15
