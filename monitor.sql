/*
Navicat MySQL Data Transfer

Source Server         : 10.0.3.33
Source Server Version : 50559
Source Host           : 10.0.3.33:3306
Source Database       : monitor

Target Server Type    : MYSQL
Target Server Version : 50559
File Encoding         : 65001

Date: 2018-05-30 09:42:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cloud_result_in_row
-- ----------------------------
DROP TABLE IF EXISTS `cloud_result_in_row`;
CREATE TABLE `cloud_result_in_row` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `max_memory` int(255) DEFAULT NULL,
  `memory_usage` float(255,0) DEFAULT NULL,
  `number_cpus` int(11) DEFAULT NULL,
  `cpu_usage` float(255,0) DEFAULT NULL,
  `net_rx_bytes` int(255) DEFAULT NULL,
  `net_rx_packets` int(255) DEFAULT NULL,
  `net_rx_errs` int(255) DEFAULT NULL,
  `net_rx_drop` int(255) DEFAULT NULL,
  `net_tx_bytes` int(255) DEFAULT NULL,
  `net_tx_packets` int(255) DEFAULT NULL,
  `net_tx_errs` int(255) DEFAULT NULL,
  `net_tx_drop` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5333 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for cloud_vhost
-- ----------------------------
DROP TABLE IF EXISTS `cloud_vhost`;
CREATE TABLE `cloud_vhost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `enable` varchar(255) DEFAULT NULL,
  `profile` varchar(255) DEFAULT NULL,
  `allocation` varchar(255) DEFAULT NULL,
  `windows` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for linux_arp
-- ----------------------------
DROP TABLE IF EXISTS `linux_arp`;
CREATE TABLE `linux_arp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `Interface` varchar(255) DEFAULT NULL,
  `Ip` varchar(255) DEFAULT NULL,
  `Mac` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1101 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for linux_ifconfig
-- ----------------------------
DROP TABLE IF EXISTS `linux_ifconfig`;
CREATE TABLE `linux_ifconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `Interface` varchar(255) DEFAULT NULL,
  `Ip` varchar(255) DEFAULT NULL,
  `Mac` varchar(255) DEFAULT NULL,
  `Mode` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=774 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for linux_lsmod
-- ----------------------------
DROP TABLE IF EXISTS `linux_lsmod`;
CREATE TABLE `linux_lsmod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `Module` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17090 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for linux_pslist
-- ----------------------------
DROP TABLE IF EXISTS `linux_pslist`;
CREATE TABLE `linux_pslist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `Offset` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Pid` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25759 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for monitor_file_change
-- ----------------------------
DROP TABLE IF EXISTS `monitor_file_change`;
CREATE TABLE `monitor_file_change` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `md5` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for monitor_file_list
-- ----------------------------
DROP TABLE IF EXISTS `monitor_file_list`;
CREATE TABLE `monitor_file_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for registry_change
-- ----------------------------
DROP TABLE IF EXISTS `registry_change`;
CREATE TABLE `registry_change` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `registry` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `key_name` varchar(255) DEFAULT NULL,
  `key_type` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for registry_list
-- ----------------------------
DROP TABLE IF EXISTS `registry_list`;
CREATE TABLE `registry_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `registry` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `md5` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for windows_lsmod
-- ----------------------------
DROP TABLE IF EXISTS `windows_lsmod`;
CREATE TABLE `windows_lsmod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `Module` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for windows_pslist
-- ----------------------------
DROP TABLE IF EXISTS `windows_pslist`;
CREATE TABLE `windows_pslist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) DEFAULT NULL,
  `Offset` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Pid` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=268 DEFAULT CHARSET=latin1;
