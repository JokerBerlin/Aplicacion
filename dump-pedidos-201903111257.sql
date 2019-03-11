-- MySQL dump 10.17  Distrib 10.3.12-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: pedidos
-- ------------------------------------------------------
-- Server version	10.3.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_almacen`
--

DROP TABLE IF EXISTS `app_almacen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_almacen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_anulacionventa`
--

DROP TABLE IF EXISTS `app_anulacionventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_anulacionventa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `venta_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_anulacionventa_usuario_id_1a115574_fk_auth_user_id` (`usuario_id`),
  KEY `app_anulacionventa_venta_id_8eb643f9` (`venta_id`),
  CONSTRAINT `app_anulacionventa_usuario_id_1a115574_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `app_anulacionventa_venta_id_8eb643f9_fk_app_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `app_venta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_aperturacaja`
--

DROP TABLE IF EXISTS `app_aperturacaja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_aperturacaja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `monto` double NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `caja_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_aperturacaja_caja_id_3b8f823b` (`caja_id`),
  CONSTRAINT `app_aperturacaja_caja_id_3b8f823b_fk_app_caja_id` FOREIGN KEY (`caja_id`) REFERENCES `app_caja` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_caja`
--

DROP TABLE IF EXISTS `app_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_caja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_categoria`
--

DROP TABLE IF EXISTS `app_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_categoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_cierrecaja`
--

DROP TABLE IF EXISTS `app_cierrecaja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_cierrecaja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `monto` double NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `aperturacaja_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_cierrecaja_aperturacaja_id_0fa511a7_fk_app_aperturacaja_id` (`aperturacaja_id`),
  CONSTRAINT `app_cierrecaja_aperturacaja_id_0fa511a7_fk_app_aperturacaja_id` FOREIGN KEY (`aperturacaja_id`) REFERENCES `app_aperturacaja` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_cliente`
--

DROP TABLE IF EXISTS `app_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_cliente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `direccion` varchar(45) NOT NULL,
  `longitud` varchar(25) DEFAULT NULL,
  `latitud` varchar(25) DEFAULT NULL,
  `numerodocumento` varchar(11) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `precio_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `app_cliente_precio_id_8f1f0a58` (`precio_id`),
  CONSTRAINT `app_cliente_precio_id_8f1f0a58_fk_app_precio_id` FOREIGN KEY (`precio_id`) REFERENCES `app_precio` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_cobro`
--

DROP TABLE IF EXISTS `app_cobro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_cobro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `monto` double NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `recibo_id` int(11) DEFAULT NULL,
  `venta_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_cobro_recibo_id_af155a1e` (`recibo_id`),
  KEY `app_cobro_venta_id_57811e29` (`venta_id`),
  CONSTRAINT `app_cobro_recibo_id_af155a1e_fk_app_recibo_id` FOREIGN KEY (`recibo_id`) REFERENCES `app_recibo` (`id`),
  CONSTRAINT `app_cobro_venta_id_57811e29_fk_app_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `app_venta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_detalletipooperacion`
--

DROP TABLE IF EXISTS `app_detalletipooperacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_detalletipooperacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `tipooperacion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_detalletipooperacion_tipooperacion_id_82cdef98` (`tipooperacion_id`),
  CONSTRAINT `app_detalletipoopera_tipooperacion_id_82cdef98_fk_app_tipoo` FOREIGN KEY (`tipooperacion_id`) REFERENCES `app_tipooperacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_empleado`
--

DROP TABLE IF EXISTS `app_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_empleado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `imei` varchar(45) DEFAULT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `perfil` int(11) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `almacen_id` int(11) NOT NULL,
  `caja_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `app_empleado_almacen_id_a3e5945d_fk_app_almacen_id` (`almacen_id`),
  KEY `app_empleado_caja_id_ecdc0955_fk_app_caja_id` (`caja_id`),
  CONSTRAINT `app_empleado_almacen_id_a3e5945d_fk_app_almacen_id` FOREIGN KEY (`almacen_id`) REFERENCES `app_almacen` (`id`),
  CONSTRAINT `app_empleado_caja_id_ecdc0955_fk_app_caja_id` FOREIGN KEY (`caja_id`) REFERENCES `app_caja` (`id`),
  CONSTRAINT `app_empleado_usuario_id_a6040fce_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_error`
--

DROP TABLE IF EXISTS `app_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_error` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `actividad` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_lote`
--

DROP TABLE IF EXISTS `app_lote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_lote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `fechavencimiento` date DEFAULT NULL,
  `modificado` datetime NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `nrecibo` varchar(45) DEFAULT NULL,
  `proveedor_id` int(11) NOT NULL,
  `recibo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_lote_proveedor_id_d006fd51` (`proveedor_id`),
  KEY `app_lote_recibo_id_a2e0914a` (`recibo_id`),
  CONSTRAINT `app_lote_proveedor_id_d006fd51_fk_app_proveedor_id` FOREIGN KEY (`proveedor_id`) REFERENCES `app_proveedor` (`id`),
  CONSTRAINT `app_lote_recibo_id_a2e0914a_fk_app_recibo_id` FOREIGN KEY (`recibo_id`) REFERENCES `app_recibo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_movimiento`
--

DROP TABLE IF EXISTS `app_movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_movimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `cantidad_producto` double NOT NULL,
  `pedido_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_movimiento_pedido_id_2149d2d3` (`pedido_id`),
  CONSTRAINT `app_movimiento_pedido_id_2149d2d3_fk_app_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `app_pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_operacion`
--

DROP TABLE IF EXISTS `app_operacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_operacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `monto` double NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `caja_id` int(11) NOT NULL,
  `cobro_id` int(11) DEFAULT NULL,
  `detalletipooperacion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_operacion_caja_id_340d8f75_fk_app_caja_id` (`caja_id`),
  KEY `app_operacion_cobro_id_21501b9e_fk_app_cobro_id` (`cobro_id`),
  KEY `app_operacion_detalletipooperacion_a392b9d1_fk_app_detal` (`detalletipooperacion_id`),
  CONSTRAINT `app_operacion_caja_id_340d8f75_fk_app_caja_id` FOREIGN KEY (`caja_id`) REFERENCES `app_caja` (`id`),
  CONSTRAINT `app_operacion_cobro_id_21501b9e_fk_app_cobro_id` FOREIGN KEY (`cobro_id`) REFERENCES `app_cobro` (`id`),
  CONSTRAINT `app_operacion_detalletipooperacion_a392b9d1_fk_app_detal` FOREIGN KEY (`detalletipooperacion_id`) REFERENCES `app_detalletipooperacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_pedido`
--

DROP TABLE IF EXISTS `app_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_pedido` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `estado` int(11) NOT NULL,
  `tipo` int(11) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `empleado_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_pedido_cliente_id_e42e9f61_fk_app_cliente_id` (`cliente_id`),
  KEY `app_pedido_empleado_id_2d8272b6_fk_app_empleado_id` (`empleado_id`),
  CONSTRAINT `app_pedido_cliente_id_e42e9f61_fk_app_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_cliente` (`id`),
  CONSTRAINT `app_pedido_empleado_id_2d8272b6_fk_app_empleado_id` FOREIGN KEY (`empleado_id`) REFERENCES `app_empleado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_precio`
--

DROP TABLE IF EXISTS `app_precio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_precio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_presentacion`
--

DROP TABLE IF EXISTS `app_presentacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_presentacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `codigo` varchar(45) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_producto`
--

DROP TABLE IF EXISTS `app_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `codigo` varchar(45) DEFAULT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `valor` double NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_producto_almacens`
--

DROP TABLE IF EXISTS `app_producto_almacens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_producto_almacens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad` double NOT NULL,
  `cantidadinicial` double NOT NULL,
  `precioCompra` double DEFAULT NULL,
  `almacen_id` int(11) NOT NULL,
  `lote_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_producto_almacens_almacen_id_48c16381_fk_app_almacen_id` (`almacen_id`),
  KEY `app_producto_almacens_lote_id_a0ae9e14_fk_app_lote_id` (`lote_id`),
  KEY `app_producto_almacens_producto_id_d4d92813_fk_app_producto_id` (`producto_id`),
  CONSTRAINT `app_producto_almacens_almacen_id_48c16381_fk_app_almacen_id` FOREIGN KEY (`almacen_id`) REFERENCES `app_almacen` (`id`),
  CONSTRAINT `app_producto_almacens_lote_id_a0ae9e14_fk_app_lote_id` FOREIGN KEY (`lote_id`) REFERENCES `app_lote` (`id`),
  CONSTRAINT `app_producto_almacens_producto_id_d4d92813_fk_app_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `app_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_producto_categorias`
--

DROP TABLE IF EXISTS `app_producto_categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_producto_categorias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `categoria_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_producto_categor_categoria_id_8f2d77e4_fk_app_categ` (`categoria_id`),
  KEY `app_producto_categorias_producto_id_3401d4f3_fk_app_producto_id` (`producto_id`),
  CONSTRAINT `app_producto_categor_categoria_id_8f2d77e4_fk_app_categ` FOREIGN KEY (`categoria_id`) REFERENCES `app_categoria` (`id`),
  CONSTRAINT `app_producto_categorias_producto_id_3401d4f3_fk_app_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `app_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_producto_presentacions`
--

DROP TABLE IF EXISTS `app_producto_presentacions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_producto_presentacions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producto_id` int(11) NOT NULL,
  `presentacion_id` int(11) NOT NULL,
  `valor` double NOT NULL DEFAULT 1,
  `unidadprincipal` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_producto_presentacio_producto_id_presentacion_1229b37a_uniq` (`producto_id`,`presentacion_id`),
  KEY `app_producto_present_presentacion_id_e45d5b10_fk_app_prese` (`presentacion_id`),
  CONSTRAINT `app_producto_present_presentacion_id_e45d5b10_fk_app_prese` FOREIGN KEY (`presentacion_id`) REFERENCES `app_presentacion` (`id`),
  CONSTRAINT `app_producto_present_producto_id_b1941332_fk_app_produ` FOREIGN KEY (`producto_id`) REFERENCES `app_producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_producto_presentacions_precios`
--

DROP TABLE IF EXISTS `app_producto_presentacions_precios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_producto_presentacions_precios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `precio_id` int(11) NOT NULL,
  `productopresentacions_id` int(11) NOT NULL,
  `valor` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_producto_presentacions_precios_app_precio_FK` (`precio_id`),
  KEY `app_producto_presentacions_precios_app_producto_presentacions_FK` (`productopresentacions_id`),
  CONSTRAINT `app_producto_presentacions_precios_app_precio_FK` FOREIGN KEY (`precio_id`) REFERENCES `app_precio` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `app_producto_presentacions_precios_app_producto_presentacions_FK` FOREIGN KEY (`productopresentacions_id`) REFERENCES `app_producto_presentacions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_proveedor`
--

DROP TABLE IF EXISTS `app_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_proveedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `direccion` varchar(45) NOT NULL,
  `documento` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_recibo`
--

DROP TABLE IF EXISTS `app_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_recibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_ruta`
--

DROP TABLE IF EXISTS `app_ruta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_ruta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `fecha` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `repartidor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_ruta_repartidor_id_365e821b_fk_app_empleado_id` (`repartidor_id`),
  CONSTRAINT `app_ruta_repartidor_id_365e821b_fk_app_empleado_id` FOREIGN KEY (`repartidor_id`) REFERENCES `app_empleado` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_ruta_clientes`
--

DROP TABLE IF EXISTS `app_ruta_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_ruta_clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ruta_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `modificacion` datetime DEFAULT NULL,
  `activo` tinyint(4) DEFAULT 1,
  `estado` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_ruta_clientes_ruta_id_cliente_id_bf8257bb_uniq` (`ruta_id`,`cliente_id`),
  KEY `app_ruta_clientes_cliente_id_f415e4a7_fk_app_cliente_id` (`cliente_id`),
  CONSTRAINT `app_ruta_clientes_cliente_id_f415e4a7_fk_app_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_cliente` (`id`),
  CONSTRAINT `app_ruta_clientes_ruta_id_58246996_fk_app_ruta_id` FOREIGN KEY (`ruta_id`) REFERENCES `app_ruta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_serie`
--

DROP TABLE IF EXISTS `app_serie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_serie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numeroSerie` varchar(3) NOT NULL,
  `recibo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_serie_recibo_id_ff1e99aa_fk_app_recibo_id` (`recibo_id`),
  CONSTRAINT `app_serie_recibo_id_ff1e99aa_fk_app_recibo_id` FOREIGN KEY (`recibo_id`) REFERENCES `app_recibo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_tipooperacion`
--

DROP TABLE IF EXISTS `app_tipooperacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_tipooperacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_tipoventa`
--

DROP TABLE IF EXISTS `app_tipoventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_tipoventa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_venta`
--

DROP TABLE IF EXISTS `app_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_venta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `monto` double NOT NULL,
  `nrecibo` varchar(45) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `pedido_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_venta_cliente_id_449dcf19_fk_app_cliente_id` (`cliente_id`),
  KEY `app_venta_pedido_id_ee2b4b3e_fk_app_pedido_id` (`pedido_id`),
  CONSTRAINT `app_venta_cliente_id_449dcf19_fk_app_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_cliente` (`id`),
  CONSTRAINT `app_venta_pedido_id_ee2b4b3e_fk_app_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `app_pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_venta_tipoventa`
--

DROP TABLE IF EXISTS `app_venta_tipoventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_venta_tipoventa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `venta_id` int(11) NOT NULL,
  `tipoventa_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_venta_tipoventa_venta_id_tipoventa_id_c4fe14f6_uniq` (`venta_id`,`tipoventa_id`),
  KEY `app_venta_tipoventa_tipoventa_id_22a49887_fk_app_tipoventa_id` (`tipoventa_id`),
  CONSTRAINT `app_venta_tipoventa_tipoventa_id_22a49887_fk_app_tipoventa_id` FOREIGN KEY (`tipoventa_id`) REFERENCES `app_tipoventa` (`id`),
  CONSTRAINT `app_venta_tipoventa_venta_id_49be0981_fk_app_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `app_venta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_visita`
--

DROP TABLE IF EXISTS `app_visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_visita` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `modificacion` datetime NOT NULL,
  `nivel` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `empleado_id` int(11) NOT NULL,
  `rutacliente_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_visita_empleado_id_16ee0484_fk_app_empleado_id` (`empleado_id`),
  KEY `app_visita_rutacliente_id_2b406aa6_fk_app_ruta_clientes_id` (`rutacliente_id`),
  CONSTRAINT `app_visita_empleado_id_16ee0484_fk_app_empleado_id` FOREIGN KEY (`empleado_id`) REFERENCES `app_empleado` (`id`),
  CONSTRAINT `app_visita_rutacliente_id_2b406aa6_fk_app_ruta_clientes_id` FOREIGN KEY (`rutacliente_id`) REFERENCES `app_ruta_clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_visita_clientes`
--

DROP TABLE IF EXISTS `app_visita_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_visita_clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `visita_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_visita_clientes_visita_id_cliente_id_05c8dab8_uniq` (`visita_id`,`cliente_id`),
  KEY `app_visita_clientes_cliente_id_189f48ed_fk_app_cliente_id` (`cliente_id`),
  CONSTRAINT `app_visita_clientes_cliente_id_189f48ed_fk_app_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_cliente` (`id`),
  CONSTRAINT `app_visita_clientes_visita_id_70ddc949_fk_app_visita_id` FOREIGN KEY (`visita_id`) REFERENCES `app_visita` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'pedidos'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-11 12:57:17
