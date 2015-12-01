/*
Navicat MySQL Data Transfer

Source Server         : Local
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : veta

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2015-11-25 10:50:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for addresses
-- ----------------------------
DROP TABLE IF EXISTS `addresses`;
CREATE TABLE `addresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `postalcode` int(11) DEFAULT NULL,
  `city` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `app` varchar(255) NOT NULL,
  `app_extra` varchar(255) DEFAULT NULL,
  `comment` text,
  `date_add` datetime NOT NULL,
  `date_update` datetime NOT NULL,
  `branch_main` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of addresses
-- ----------------------------

-- ----------------------------
-- Table structure for branches
-- ----------------------------
DROP TABLE IF EXISTS `branches`;
CREATE TABLE `branches` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type_id` int(10) NOT NULL,
  `company_id` int(10) NOT NULL,
  `date_add` datetime NOT NULL,
  `date_update` datetime NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `description` text,
  `address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`),
  KEY `type_id` (`type_id`),
  KEY `branches_ibfk_1` (`company_id`),
  CONSTRAINT `branches_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `branches_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `branch_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of branches
-- ----------------------------

-- ----------------------------
-- Table structure for branch_types
-- ----------------------------
DROP TABLE IF EXISTS `branch_types`;
CREATE TABLE `branch_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of branch_types
-- ----------------------------

-- ----------------------------
-- Table structure for client_options
-- ----------------------------
DROP TABLE IF EXISTS `client_options`;
CREATE TABLE `client_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) NOT NULL,
  `request_tickets` tinyint(255) DEFAULT NULL COMMENT 'Предоставлять талоны с полигонов',
  `request_special_sign` tinyint(255) DEFAULT NULL COMMENT 'Делать отметки на объектах',
  `request_freq` tinyint(255) DEFAULT NULL COMMENT 'Частота вывозов',
  `use_client_talons_only` tinyint(255) DEFAULT NULL COMMENT 'Требование использовать на полигоне выданные клиентом талоны',
  `pay_condition` tinyint(255) DEFAULT NULL COMMENT 'Условия оплаты:по постановке, по вывозу',
  `pay_type` tinyint(255) DEFAULT NULL COMMENT 'Форма оплаты: нал, безнал',
  `move_price` int(11) DEFAULT NULL COMMENT 'стоимость ходки для водителя в рублях',
  `credit_limit` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of client_options
-- ----------------------------

-- ----------------------------
-- Table structure for companies
-- ----------------------------
DROP TABLE IF EXISTS `companies`;
CREATE TABLE `companies` (
  `id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `www` varchar(255) DEFAULT NULL,
  `org_types_id` int(11) NOT NULL,
  `rel_types_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `responsible_employee` int(255) NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_update` datetime DEFAULT NULL,
  `author_user` int(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of companies
-- ----------------------------

-- ----------------------------
-- Table structure for company_org_types
-- ----------------------------
DROP TABLE IF EXISTS `company_org_types`;
CREATE TABLE `company_org_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of company_org_types
-- ----------------------------
INSERT INTO `company_org_types` VALUES ('1', 'Частник');
INSERT INTO `company_org_types` VALUES ('2', 'Фирма');

-- ----------------------------
-- Table structure for company_rel_types
-- ----------------------------
DROP TABLE IF EXISTS `company_rel_types`;
CREATE TABLE `company_rel_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of company_rel_types
-- ----------------------------
INSERT INTO `company_rel_types` VALUES ('1', 'Своя');
INSERT INTO `company_rel_types` VALUES ('2', 'Клиент');
INSERT INTO `company_rel_types` VALUES ('3', 'Партнер');
INSERT INTO `company_rel_types` VALUES ('4', 'Поставщик');

-- ----------------------------
-- Table structure for company_status
-- ----------------------------
DROP TABLE IF EXISTS `company_status`;
CREATE TABLE `company_status` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of company_status
-- ----------------------------
INSERT INTO `company_status` VALUES ('1', 'Новый');
INSERT INTO `company_status` VALUES ('2', 'Готов ');
INSERT INTO `company_status` VALUES ('3', 'В работе');
INSERT INTO `company_status` VALUES ('4', 'Заморожен');
INSERT INTO `company_status` VALUES ('5', 'Архив');

-- ----------------------------
-- Table structure for contragents
-- ----------------------------
DROP TABLE IF EXISTS `contragents`;
CREATE TABLE `contragents` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `company_id` int(10) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `type_id` int(255) NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_update` datetime DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `contragents_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of contragents
-- ----------------------------

-- ----------------------------
-- Table structure for contragent_groups
-- ----------------------------
DROP TABLE IF EXISTS `contragent_groups`;
CREATE TABLE `contragent_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of contragent_groups
-- ----------------------------
INSERT INTO `contragent_groups` VALUES ('1', 'Служебные');
INSERT INTO `contragent_groups` VALUES ('2', 'Водители');
INSERT INTO `contragent_groups` VALUES ('3', 'Сотрудники');
INSERT INTO `contragent_groups` VALUES ('4', 'Клиенты');

-- ----------------------------
-- Table structure for contragent_types
-- ----------------------------
DROP TABLE IF EXISTS `contragent_types`;
CREATE TABLE `contragent_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of contragent_types
-- ----------------------------
INSERT INTO `contragent_types` VALUES ('1', 'Физическое лицо');
INSERT INTO `contragent_types` VALUES ('2', 'Юридическое лицо');
INSERT INTO `contragent_types` VALUES ('3', 'Индивидуальный предприниматель');

-- ----------------------------
-- Table structure for employee_roles
-- ----------------------------
DROP TABLE IF EXISTS `employee_roles`;
CREATE TABLE `employee_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of employee_roles
-- ----------------------------
INSERT INTO `employee_roles` VALUES ('1', 'Диспетчер');
INSERT INTO `employee_roles` VALUES ('2', 'Водитель');

-- ----------------------------
-- Table structure for employee_types
-- ----------------------------
DROP TABLE IF EXISTS `employee_types`;
CREATE TABLE `employee_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of employee_types
-- ----------------------------
INSERT INTO `employee_types` VALUES ('1', 'Контакт');
INSERT INTO `employee_types` VALUES ('2', 'Штатный');
INSERT INTO `employee_types` VALUES ('3', 'Временный');

-- ----------------------------
-- Table structure for employies
-- ----------------------------
DROP TABLE IF EXISTS `employies`;
CREATE TABLE `employies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `branch_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_update` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of employies
-- ----------------------------

-- ----------------------------
-- Table structure for persons
-- ----------------------------
DROP TABLE IF EXISTS `persons`;
CREATE TABLE `persons` (
  `id` int(11) NOT NULL,
  `family_name` varchar(255) NOT NULL,
  `given_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `nick_name` varchar(255) DEFAULT NULL,
  `birth_date` datetime DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `date_add` datetime NOT NULL,
  `date_update` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`),
  KEY `company_id` (`company_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `persons_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `persons_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `person_status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of persons
-- ----------------------------

-- ----------------------------
-- Table structure for person_status
-- ----------------------------
DROP TABLE IF EXISTS `person_status`;
CREATE TABLE `person_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of person_status
-- ----------------------------
INSERT INTO `person_status` VALUES ('1', 'Активный');
INSERT INTO `person_status` VALUES ('2', 'Не активный');
