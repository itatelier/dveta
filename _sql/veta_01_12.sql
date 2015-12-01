/*
Navicat MySQL Data Transfer

Source Server         : Local
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : veta

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2015-12-01 11:02:35
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of addresses
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('8', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add user', '4', 'add_user');
INSERT INTO `auth_permission` VALUES ('11', 'Can change user', '4', 'change_user');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete user', '4', 'delete_user');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('17', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete session', '6', 'delete_session');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES ('1', 'pbkdf2_sha256$20000$7oOutS08fC2d$SvYR9XAaDGjHfrVmGDHBHZCj04KdYRaVC22XfUJGq/U=', '2015-11-30 17:49:44', '1', 'root', '', '', 'nikita@itatelier.ru', '1', '1', '2015-11-29 16:37:00');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_user_permissions
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
  CONSTRAINT `branches_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `branch_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `www` varchar(255) DEFAULT NULL,
  `org_types_id` int(11) NOT NULL,
  `rel_types_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `responsible_employee` int(11) DEFAULT '1',
  `date_add` datetime NOT NULL,
  `date_update` datetime DEFAULT NULL,
  `author_user` int(11) DEFAULT '1',
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

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
  KEY `company_id` (`company_id`)
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
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_1c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2015-11-29 12:10:46');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2015-11-29 12:10:46');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('4', 'contenttypes', '0002_remove_content_type_name', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('5', 'auth', '0002_alter_permission_name_max_length', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('6', 'auth', '0003_alter_user_email_max_length', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0004_alter_user_username_opts', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0005_alter_user_last_login_null', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0006_require_contenttypes_0002', '2015-11-29 12:10:47');
INSERT INTO `django_migrations` VALUES ('10', 'sessions', '0001_initial', '2015-11-29 12:10:47');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('g2pztoejq3ut0s0opkp3svo40trtabsa', 'ZTU4NjUzNDBhZmY4ZTcxMWRiNjYyMDE4NWNjMTNlNTcxYjQ4YjFhMjp7Il9hdXRoX3VzZXJfaGFzaCI6IjlhMzllNGZkMmQxYjYxNmQzMTBlNzY1OWZkMDZjN2RmNDM2NzI5OWQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2015-12-14 17:49:44');

-- ----------------------------
-- Table structure for dummy_companies
-- ----------------------------
DROP TABLE IF EXISTS `dummy_companies`;
CREATE TABLE `dummy_companies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `www` varchar(255) DEFAULT NULL,
  `org_types_id` int(11) NOT NULL,
  `rel_types_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_update` datetime DEFAULT NULL,
  `author_user` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `org_types_id` (`org_types_id`),
  KEY `rel_types_id` (`rel_types_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `dummy_companies_ibfk_1` FOREIGN KEY (`org_types_id`) REFERENCES `company_org_types` (`id`),
  CONSTRAINT `dummy_companies_ibfk_2` FOREIGN KEY (`rel_types_id`) REFERENCES `company_rel_types` (`id`),
  CONSTRAINT `dummy_companies_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `company_status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dummy_companies
-- ----------------------------
INSERT INTO `dummy_companies` VALUES ('101', 'Lectus Corp.', 'auctor, nunc nulla vulputate dui, nec tempus mauris erat', 'odio vel est', '2', '3', '4', '2015-09-26 10:14:43', '2015-09-12 19:51:44', '78');
INSERT INTO `dummy_companies` VALUES ('102', 'In Faucibus Orci Associates', 'magna a neque. Nullam ut nisi', 'sit amet, consectetuer', '1', '1', '5', '2016-09-03 00:17:54', '2015-03-28 09:24:42', '17');
INSERT INTO `dummy_companies` VALUES ('103', 'Dui Industries', 'arcu et pede. Nunc sed orci lobortis augue scelerisque', 'ut, pellentesque eget,', '1', '3', '1', '2015-05-06 10:19:04', '2015-02-09 20:24:28', '71');
INSERT INTO `dummy_companies` VALUES ('104', 'Aliquam Eu Foundation', 'Aliquam vulputate ullamcorper magna. Sed', 'lobortis, nisi nibh', '1', '2', '3', '2016-02-25 13:47:28', '2015-06-13 04:13:31', '74');
INSERT INTO `dummy_companies` VALUES ('105', 'Ultrices Posuere Cubilia Inc.', 'varius orci, in consequat enim diam vel', 'quam quis diam.', '1', '3', '1', '2015-11-16 16:29:20', '2015-05-12 13:06:26', '25');
INSERT INTO `dummy_companies` VALUES ('106', 'Fusce Aliquet Magna Associates', 'sem egestas blandit. Nam nulla magna, malesuada vel, convallis in,', 'nec tempus scelerisque,', '1', '3', '4', '2016-02-06 12:34:09', '2015-03-03 04:30:14', '21');
INSERT INTO `dummy_companies` VALUES ('107', 'Enim Nec Institute', 'imperdiet non, vestibulum nec, euismod in,', 'ligula tortor, dictum', '2', '3', '2', '2015-05-08 09:40:04', '2016-01-04 05:08:22', '46');
INSERT INTO `dummy_companies` VALUES ('108', 'Ac Libero Nec Inc.', 'lacus. Nulla tincidunt, neque vitae semper egestas, urna', 'risus. Duis a', '1', '2', '3', '2016-07-06 09:39:08', '2016-01-08 09:49:54', '64');
INSERT INTO `dummy_companies` VALUES ('109', 'Dictum Phasellus Corp.', 'tincidunt pede ac urna. Ut tincidunt vehicula', 'bibendum sed, est.', '1', '3', '4', '2016-06-04 22:29:09', '2015-05-30 02:44:11', '10');
INSERT INTO `dummy_companies` VALUES ('110', 'Massa Industries', 'dignissim tempor arcu. Vestibulum ut eros non enim', 'Mauris magna. Duis', '1', '2', '4', '2015-05-24 14:14:02', '2016-09-02 13:55:52', '65');
INSERT INTO `dummy_companies` VALUES ('111', 'Elit Elit Fermentum Institute', 'nunc sed libero. Proin sed turpis nec mauris', 'metus. In nec', '2', '4', '3', '2016-02-15 00:27:14', '2016-11-19 08:34:26', '72');
INSERT INTO `dummy_companies` VALUES ('112', 'Donec Elementum Institute', 'amet, faucibus ut, nulla. Cras eu tellus', 'mattis ornare, lectus', '2', '3', '4', '2016-04-24 01:49:13', '2016-01-01 17:37:14', '74');
INSERT INTO `dummy_companies` VALUES ('113', 'Tellus Limited', 'Fusce dolor quam, elementum at,', 'et, eros. Proin', '2', '2', '1', '2015-08-26 17:36:01', '2016-07-20 11:42:34', '46');
INSERT INTO `dummy_companies` VALUES ('114', 'Feugiat Lorem LLP', 'Nunc sollicitudin commodo ipsum. Suspendisse', 'dolor dapibus gravida.', '1', '4', '2', '2016-06-08 16:47:08', '2015-12-04 18:04:08', '77');
INSERT INTO `dummy_companies` VALUES ('115', 'Auctor Non Inc.', 'lorem ac risus. Morbi metus. Vivamus', 'et magnis dis', '1', '3', '3', '2016-10-20 12:12:13', '2015-07-25 18:47:52', '70');
INSERT INTO `dummy_companies` VALUES ('116', 'Donec Elementum Lorem Industries', 'Nulla facilisi. Sed neque. Sed eget lacus.', 'erat volutpat. Nulla', '1', '1', '5', '2015-03-04 12:18:56', '2016-09-16 03:01:37', '56');
INSERT INTO `dummy_companies` VALUES ('117', 'Tellus Sem Incorporated', 'tempor lorem, eget mollis lectus pede et risus. Quisque', 'lorem eu metus.', '2', '2', '3', '2015-07-27 12:45:10', '2014-12-04 08:14:51', '12');
INSERT INTO `dummy_companies` VALUES ('118', 'Erat Institute', 'ac nulla. In tincidunt congue', 'lorem semper auctor.', '2', '2', '3', '2015-09-30 21:35:08', '2016-06-20 13:49:17', '91');
INSERT INTO `dummy_companies` VALUES ('119', 'Dis Parturient Montes LLP', 'quis accumsan convallis, ante lectus', 'diam eu dolor', '1', '3', '5', '2016-09-13 23:38:31', '2015-08-26 22:33:59', '28');
INSERT INTO `dummy_companies` VALUES ('120', 'Nibh Lacinia Orci Institute', 'sed pede. Cum sociis natoque', 'urna. Ut tincidunt', '1', '3', '4', '2015-09-09 22:07:27', '2015-11-16 21:41:20', '92');
INSERT INTO `dummy_companies` VALUES ('121', 'Placerat Orci Corp.', 'felis orci, adipiscing non, luctus sit amet, faucibus ut, nulla.', 'malesuada id, erat.', '2', '2', '5', '2015-08-12 17:15:20', '2015-05-20 05:25:13', '47');
INSERT INTO `dummy_companies` VALUES ('122', 'Mollis Vitae Posuere LLC', 'est. Mauris eu turpis. Nulla', 'consequat dolor vitae', '2', '2', '3', '2015-04-17 15:44:58', '2015-09-08 07:54:48', '31');
INSERT INTO `dummy_companies` VALUES ('123', 'Faucibus Orci Associates', 'laoreet, libero et tristique pellentesque,', 'neque. In ornare', '2', '2', '4', '2015-10-11 20:41:05', '2016-03-28 20:22:21', '77');
INSERT INTO `dummy_companies` VALUES ('124', 'Quis Foundation', 'eget magna. Suspendisse tristique neque', 'Morbi accumsan laoreet', '1', '1', '1', '2016-08-28 18:32:23', '2016-06-20 20:18:11', '37');
INSERT INTO `dummy_companies` VALUES ('125', 'Elementum Company', 'iaculis odio. Nam interdum enim', 'Fusce fermentum fermentum', '1', '1', '3', '2015-05-24 12:40:59', '2015-04-02 00:07:09', '67');
INSERT INTO `dummy_companies` VALUES ('126', 'Sem Industries', 'vitae velit egestas lacinia. Sed congue, elit sed consequat', 'ut erat. Sed', '1', '3', '5', '2015-11-23 11:11:42', '2015-08-01 09:55:26', '82');
INSERT INTO `dummy_companies` VALUES ('127', 'Sollicitudin Adipiscing Industries', 'per conubia nostra, per inceptos hymenaeos. Mauris ut quam vel', 'tempor, est ac', '1', '4', '2', '2015-01-20 20:30:24', '2016-10-19 03:47:12', '11');
INSERT INTO `dummy_companies` VALUES ('128', 'Tortor Dictum LLC', 'ac risus. Morbi metus. Vivamus euismod urna. Nullam lobortis', 'Donec consectetuer mauris', '1', '3', '3', '2016-10-14 23:46:20', '2016-05-17 07:20:52', '78');
INSERT INTO `dummy_companies` VALUES ('129', 'Elit Elit Consulting', 'Suspendisse eleifend. Cras sed leo.', 'senectus et netus', '2', '3', '3', '2015-08-27 21:30:06', '2016-09-30 20:25:47', '4');
INSERT INTO `dummy_companies` VALUES ('130', 'Scelerisque Sed Sapien Associates', 'in molestie tortor nibh sit amet orci. Ut', 'at, velit. Cras', '1', '3', '1', '2016-08-21 06:36:27', '2015-07-14 08:08:48', '94');
INSERT INTO `dummy_companies` VALUES ('131', 'Leo Elementum LLP', 'eget magna. Suspendisse tristique neque venenatis lacus. Etiam', 'egestas, urna justo', '1', '3', '2', '2015-01-25 00:28:05', '2014-12-11 08:16:58', '50');
INSERT INTO `dummy_companies` VALUES ('132', 'Diam Eu Company', 'Curae Phasellus ornare. Fusce mollis. Duis sit amet diam', 'Donec luctus aliquet', '2', '1', '1', '2016-02-02 18:22:44', '2014-12-02 16:03:11', '96');
INSERT INTO `dummy_companies` VALUES ('133', 'Aliquam Adipiscing Lacus Consulting', 'sagittis felis. Donec tempor, est ac mattis semper,', 'Suspendisse commodo tincidunt', '1', '2', '3', '2016-01-07 20:18:19', '2016-07-11 07:24:06', '99');
INSERT INTO `dummy_companies` VALUES ('134', 'Nisl Quisque Fringilla LLC', 'et, rutrum eu, ultrices sit', 'non, hendrerit id,', '1', '1', '3', '2015-07-30 10:38:17', '2015-04-25 18:31:11', '48');
INSERT INTO `dummy_companies` VALUES ('135', 'Parturient Montes Nascetur Ltd', 'tempor lorem, eget mollis lectus pede et risus. Quisque libero', 'vulputate dui, nec', '2', '1', '4', '2016-05-02 21:25:02', '2016-06-13 13:36:44', '22');
INSERT INTO `dummy_companies` VALUES ('136', 'Elementum LLC', 'velit eu sem. Pellentesque ut ipsum ac mi', 'nunc. In at', '2', '4', '2', '2016-05-27 06:39:32', '2016-07-03 15:18:48', '89');
INSERT INTO `dummy_companies` VALUES ('137', 'Ac Mattis Ornare Ltd', 'massa. Quisque porttitor eros nec tellus. Nunc', 'Nam consequat dolor', '2', '2', '5', '2016-07-21 08:34:01', '2016-02-12 13:37:20', '79');
INSERT INTO `dummy_companies` VALUES ('138', 'Aliquam Ltd', 'ac mi eleifend egestas. Sed pharetra, felis', 'malesuada augue ut', '2', '3', '1', '2015-03-29 20:45:38', '2016-08-18 16:14:16', '94');
INSERT INTO `dummy_companies` VALUES ('139', 'Lobortis Quam Associates', 'ultrices posuere cubilia Curae Phasellus', 'id ante dictum', '1', '2', '3', '2016-11-15 05:45:33', '2015-05-30 09:04:28', '45');
INSERT INTO `dummy_companies` VALUES ('140', 'Mauris Morbi Limited', 'semper cursus. Integer mollis. Integer tincidunt', 'Cras vulputate velit', '1', '4', '4', '2016-04-15 15:55:50', '2015-04-25 05:55:05', '32');
INSERT INTO `dummy_companies` VALUES ('141', 'Magnis Dis Inc.', 'eu tellus eu augue porttitor interdum. Sed auctor odio a', 'ut, molestie in,', '1', '3', '1', '2015-07-31 08:19:00', '2015-11-22 07:31:58', '36');
INSERT INTO `dummy_companies` VALUES ('142', 'Et Rutrum Eu Limited', 'aliquam arcu. Aliquam ultrices iaculis odio. Nam interdum enim non', 'Mauris non dui', '1', '2', '3', '2015-04-23 22:33:47', '2016-05-12 16:17:00', '59');
INSERT INTO `dummy_companies` VALUES ('143', 'Maecenas Ornare PC', 'fermentum arcu. Vestibulum ante ipsum primis in faucibus orci', 'orci luctus et', '2', '2', '2', '2015-11-07 23:22:56', '2015-05-26 20:40:16', '45');
INSERT INTO `dummy_companies` VALUES ('144', 'Nunc Sed Libero Consulting', 'id ante dictum cursus. Nunc mauris', 'magna. Praesent interdum', '1', '4', '5', '2015-09-14 19:43:15', '2016-07-25 19:32:47', '84');
INSERT INTO `dummy_companies` VALUES ('145', 'Nunc Laoreet Company', 'magna, malesuada vel, convallis in,', 'felis ullamcorper viverra.', '2', '4', '2', '2015-04-12 17:42:36', '2015-12-06 00:36:16', '84');
INSERT INTO `dummy_companies` VALUES ('146', 'Montes Nascetur Foundation', 'euismod enim. Etiam gravida molestie arcu. Sed eu nibh vulputate', 'elit pede, malesuada', '1', '2', '4', '2016-01-13 20:27:56', '2015-11-10 05:47:38', '52');
INSERT INTO `dummy_companies` VALUES ('147', 'Arcu Inc.', 'mattis semper, dui lectus rutrum urna, nec', 'vitae velit egestas', '1', '1', '1', '2015-05-16 23:15:05', '2015-09-11 07:42:23', '93');
INSERT INTO `dummy_companies` VALUES ('148', 'Purus Corp.', 'Proin velit. Sed malesuada augue ut', 'lorem, eget mollis', '1', '3', '4', '2016-08-13 07:53:25', '2015-12-17 07:17:06', '16');
INSERT INTO `dummy_companies` VALUES ('149', 'Taciti Sociosqu Corporation', 'tellus eu augue porttitor interdum. Sed auctor odio', 'eget odio. Aliquam', '1', '3', '2', '2016-10-05 12:05:57', '2015-11-13 03:06:38', '17');
INSERT INTO `dummy_companies` VALUES ('150', 'Nec Ante Limited', 'elementum, lorem ut aliquam iaculis, lacus pede sagittis augue,', 'a, magna. Lorem', '1', '1', '1', '2015-05-21 08:43:57', '2015-09-28 02:04:50', '45');
INSERT INTO `dummy_companies` VALUES ('151', 'Dis Parturient Ltd', 'nunc, ullamcorper eu, euismod ac, fermentum vel, mauris. Integer', 'dui, semper et,', '2', '1', '5', '2016-07-09 12:46:12', '2015-09-01 12:59:03', '47');
INSERT INTO `dummy_companies` VALUES ('152', 'Parturient Montes Nascetur Ltd', 'amet lorem semper auctor. Mauris vel turpis. Aliquam adipiscing lobortis', 'eget tincidunt dui', '2', '4', '4', '2016-07-23 21:12:50', '2015-12-30 06:37:39', '93');
INSERT INTO `dummy_companies` VALUES ('153', 'Donec Luctus Aliquet PC', 'egestas rhoncus. Proin nisl sem, consequat nec,', 'ante ipsum primis', '1', '2', '4', '2016-03-19 17:36:19', '2015-03-23 14:43:03', '55');
INSERT INTO `dummy_companies` VALUES ('154', 'Non Luctus Sit LLP', 'molestie. Sed id risus quis diam luctus lobortis. Class aptent', 'facilisis facilisis, magna', '1', '2', '2', '2014-12-23 14:40:51', '2014-12-13 20:26:07', '2');
INSERT INTO `dummy_companies` VALUES ('155', 'Turpis Corp.', 'lacus. Ut nec urna et arcu imperdiet ullamcorper. Duis', 'interdum libero dui', '2', '2', '3', '2016-05-06 00:41:28', '2016-05-05 01:39:59', '21');
INSERT INTO `dummy_companies` VALUES ('156', 'Enim Gravida PC', 'dolor vitae dolor. Donec fringilla. Donec feugiat', 'viverra. Maecenas iaculis', '1', '1', '3', '2016-08-10 20:31:50', '2016-02-01 22:55:15', '78');
INSERT INTO `dummy_companies` VALUES ('157', 'Sed PC', 'ligula. Aenean gravida nunc sed', 'nec tempus scelerisque,', '1', '3', '3', '2016-08-21 22:28:43', '2016-07-27 02:32:32', '62');
INSERT INTO `dummy_companies` VALUES ('158', 'Libero Mauris Consulting', 'tincidunt, neque vitae semper egestas,', 'erat. Sed nunc', '2', '3', '5', '2015-11-27 17:51:22', '2016-08-11 11:41:21', '8');
INSERT INTO `dummy_companies` VALUES ('159', 'Semper LLC', 'suscipit nonummy. Fusce fermentum fermentum arcu.', 'risus. Nulla eget', '1', '2', '4', '2015-10-20 03:25:58', '2015-02-03 08:20:42', '87');
INSERT INTO `dummy_companies` VALUES ('160', 'Dictum Mi Inc.', 'est. Mauris eu turpis. Nulla aliquet.', 'interdum. Curabitur dictum.', '2', '4', '4', '2015-10-03 16:53:37', '2015-07-13 09:35:58', '80');
INSERT INTO `dummy_companies` VALUES ('161', 'Mauris Sit Corporation', 'porttitor scelerisque neque. Nullam nisl. Maecenas malesuada fringilla', 'a, dui. Cras', '2', '4', '4', '2016-03-31 18:51:21', '2015-04-10 04:59:18', '32');
INSERT INTO `dummy_companies` VALUES ('162', 'Nonummy Ac PC', 'aliquam eros turpis non enim.', 'sem semper erat,', '2', '4', '4', '2015-03-05 21:22:09', '2016-10-04 22:53:19', '71');
INSERT INTO `dummy_companies` VALUES ('163', 'Aliquam PC', 'orci luctus et ultrices posuere cubilia Curae Phasellus ornare.', 'mauris ipsum porta', '2', '3', '1', '2016-02-20 09:07:45', '2015-06-08 09:15:39', '7');
INSERT INTO `dummy_companies` VALUES ('164', 'Libero Associates', 'Nam porttitor scelerisque neque. Nullam', 'Morbi sit amet', '2', '1', '3', '2016-07-28 03:17:34', '2015-04-30 21:16:22', '18');
INSERT INTO `dummy_companies` VALUES ('165', 'Penatibus Ltd', 'per inceptos hymenaeos. Mauris ut quam vel sapien', 'Quisque libero lacus,', '1', '2', '5', '2015-08-26 00:22:27', '2015-12-25 22:25:04', '43');
INSERT INTO `dummy_companies` VALUES ('166', 'Nec Corporation', 'lectus. Cum sociis natoque penatibus et magnis', 'Vivamus euismod urna.', '2', '4', '5', '2016-05-21 09:59:17', '2015-09-24 12:08:13', '81');
INSERT INTO `dummy_companies` VALUES ('167', 'Ut Corp.', 'ullamcorper. Duis cursus, diam at pretium aliquet, metus urna', 'venenatis lacus. Etiam', '1', '1', '1', '2016-02-07 02:04:41', '2015-05-13 12:51:15', '60');
INSERT INTO `dummy_companies` VALUES ('168', 'Non Dui Nec Limited', 'Vivamus euismod urna. Nullam lobortis', 'Sed dictum. Proin', '1', '1', '1', '2015-05-18 16:15:33', '2015-11-08 08:15:59', '2');
INSERT INTO `dummy_companies` VALUES ('169', 'Praesent Corporation', 'massa rutrum magna. Cras convallis convallis dolor.', 'diam. Sed diam', '2', '4', '3', '2016-02-21 11:33:27', '2016-11-01 23:55:02', '2');
INSERT INTO `dummy_companies` VALUES ('170', 'Pellentesque Ultricies Industries', 'tempor augue ac ipsum. Phasellus vitae mauris sit amet lorem', 'dis parturient montes,', '2', '1', '2', '2016-07-31 03:10:29', '2016-03-23 09:37:29', '86');
INSERT INTO `dummy_companies` VALUES ('171', 'Quisque Varius Ltd', 'Curabitur sed tortor. Integer aliquam adipiscing', 'mauris sit amet', '1', '3', '5', '2015-04-29 17:52:05', '2016-05-11 14:31:33', '42');
INSERT INTO `dummy_companies` VALUES ('172', 'Nisi Associates', 'Integer eu lacus. Quisque imperdiet, erat nonummy ultricies', 'eget metus. In', '1', '4', '4', '2015-08-17 16:13:23', '2015-05-15 22:42:16', '38');
INSERT INTO `dummy_companies` VALUES ('173', 'Donec Sollicitudin Inc.', 'nunc interdum feugiat. Sed nec', 'Duis gravida. Praesent', '1', '3', '4', '2016-06-17 07:40:51', '2016-10-12 09:58:45', '49');
INSERT INTO `dummy_companies` VALUES ('174', 'Imperdiet Nec Leo Associates', 'pede ac urna. Ut tincidunt vehicula risus. Nulla', 'at auctor ullamcorper,', '2', '1', '3', '2016-11-12 14:39:31', '2015-11-18 15:36:19', '75');
INSERT INTO `dummy_companies` VALUES ('175', 'Nibh Donec Consulting', 'enim. Mauris quis turpis vitae purus gravida sagittis. Duis', 'et risus. Quisque', '1', '4', '3', '2016-09-08 17:24:00', '2015-06-26 02:00:44', '67');
INSERT INTO `dummy_companies` VALUES ('176', 'Tellus LLC', 'nascetur ridiculus mus. Aenean eget magna. Suspendisse', 'elit. Nulla facilisi.', '2', '1', '1', '2016-10-02 08:39:34', '2016-09-14 09:48:30', '76');
INSERT INTO `dummy_companies` VALUES ('177', 'Dignissim Tempor Arcu Limited', 'dui. Fusce diam nunc, ullamcorper', 'non magna. Nam', '1', '1', '4', '2014-12-04 05:21:08', '2016-10-14 02:56:50', '94');
INSERT INTO `dummy_companies` VALUES ('178', 'Non Sapien Corporation', 'turpis. Aliquam adipiscing lobortis risus.', 'Nunc sed orci', '2', '1', '3', '2015-12-01 23:41:52', '2015-05-08 17:31:49', '77');
INSERT INTO `dummy_companies` VALUES ('179', 'Lorem Ut Aliquam Foundation', 'ac sem ut dolor dapibus', 'Integer tincidunt aliquam', '1', '3', '3', '2016-09-14 13:22:10', '2016-05-21 13:58:00', '30');
INSERT INTO `dummy_companies` VALUES ('180', 'Vestibulum Accumsan Neque Company', 'Sed pharetra, felis eget varius ultrices, mauris ipsum porta', 'Cum sociis natoque', '2', '1', '5', '2015-07-11 11:37:05', '2016-04-07 13:14:04', '4');
INSERT INTO `dummy_companies` VALUES ('181', 'Duis Dignissim LLP', 'luctus et ultrices posuere cubilia Curae', 'pharetra nibh. Aliquam', '2', '3', '3', '2016-09-24 06:11:07', '2015-04-27 08:06:59', '76');
INSERT INTO `dummy_companies` VALUES ('182', 'Facilisis Suspendisse Institute', 'Sed congue, elit sed consequat auctor, nunc nulla', 'urna justo faucibus', '2', '2', '3', '2016-08-30 17:51:02', '2015-04-03 06:55:00', '98');
INSERT INTO `dummy_companies` VALUES ('183', 'Proin Vel Nisl Limited', 'tempus scelerisque, lorem ipsum sodales purus, in molestie tortor', 'malesuada id, erat.', '2', '3', '4', '2015-08-11 09:31:03', '2016-04-18 16:50:21', '52');
INSERT INTO `dummy_companies` VALUES ('184', 'Mattis PC', 'nec, malesuada ut, sem. Nulla interdum. Curabitur', 'lobortis tellus justo', '1', '4', '2', '2015-02-08 14:27:56', '2015-06-11 08:22:29', '24');
INSERT INTO `dummy_companies` VALUES ('185', 'Est Associates', 'Nunc mauris elit, dictum eu, eleifend', 'nascetur ridiculus mus.', '1', '2', '4', '2016-07-09 15:11:09', '2015-07-08 06:28:21', '6');
INSERT INTO `dummy_companies` VALUES ('186', 'Ac Ipsum Ltd', 'facilisis facilisis, magna tellus faucibus leo, in', 'nonummy ultricies ornare,', '1', '2', '1', '2015-09-15 12:56:35', '2016-08-23 03:59:12', '47');
INSERT INTO `dummy_companies` VALUES ('187', 'Enim Nunc Industries', 'ante bibendum ullamcorper. Duis cursus,', 'nec mauris blandit', '1', '1', '2', '2016-08-23 05:16:02', '2016-08-12 09:20:24', '92');
INSERT INTO `dummy_companies` VALUES ('188', 'Curabitur Inc.', 'neque sed dictum eleifend, nunc risus varius orci,', 'lobortis. Class aptent', '2', '3', '5', '2015-04-12 21:11:05', '2016-11-27 14:13:10', '6');
INSERT INTO `dummy_companies` VALUES ('189', 'Vel Corporation', 'Etiam laoreet, libero et tristique pellentesque,', 'Suspendisse non leo.', '2', '4', '2', '2016-01-16 23:21:56', '2015-04-29 06:49:23', '12');
INSERT INTO `dummy_companies` VALUES ('190', 'Sem Elit Pharetra Inc.', 'Proin ultrices. Duis volutpat nunc sit amet', 'felis eget varius', '1', '2', '1', '2015-07-08 16:19:54', '2015-05-27 17:52:15', '72');
INSERT INTO `dummy_companies` VALUES ('191', 'Aliquet Proin Velit Limited', 'Duis mi enim, condimentum eget, volutpat ornare, facilisis eget,', 'Quisque ac libero', '2', '2', '3', '2016-08-22 18:42:38', '2015-02-12 10:06:38', '68');
INSERT INTO `dummy_companies` VALUES ('192', 'Nec Ante Maecenas Associates', 'vel est tempor bibendum. Donec felis orci,', 'ornare, lectus ante', '1', '4', '1', '2016-10-01 05:35:09', '2016-02-10 15:43:21', '96');
INSERT INTO `dummy_companies` VALUES ('193', 'Vulputate Corp.', 'vitae erat vel pede blandit', 'tincidunt orci quis', '1', '1', '2', '2015-05-14 11:02:47', '2016-08-04 17:07:28', '58');
INSERT INTO `dummy_companies` VALUES ('194', 'Cursus Vestibulum Mauris LLC', 'non, luctus sit amet, faucibus', 'senectus et netus', '1', '2', '5', '2015-05-04 11:28:06', '2015-02-03 05:26:27', '31');
INSERT INTO `dummy_companies` VALUES ('195', 'Sed Foundation', 'leo, in lobortis tellus justo sit amet', 'consequat purus. Maecenas', '1', '4', '5', '2016-03-17 18:41:47', '2016-03-22 03:21:27', '45');
INSERT INTO `dummy_companies` VALUES ('196', 'Purus Maecenas Industries', 'torquent per conubia nostra, per inceptos hymenaeos. Mauris', 'ornare. In faucibus.', '2', '2', '1', '2015-08-13 12:08:51', '2015-09-01 02:37:28', '74');
INSERT INTO `dummy_companies` VALUES ('197', 'Integer Sem Industries', 'Etiam ligula tortor, dictum eu,', 'Cras pellentesque. Sed', '1', '2', '5', '2015-01-17 07:27:46', '2014-12-14 09:12:03', '10');
INSERT INTO `dummy_companies` VALUES ('198', 'Adipiscing Ltd', 'aliquam eros turpis non enim. Mauris quis', 'aliquam eros turpis', '2', '2', '1', '2016-11-19 16:57:03', '2016-05-18 12:23:24', '71');
INSERT INTO `dummy_companies` VALUES ('199', 'Orci Luctus Company', 'natoque penatibus et magnis dis', 'consequat enim diam', '1', '4', '5', '2016-09-10 11:49:27', '2015-09-01 21:55:30', '59');
INSERT INTO `dummy_companies` VALUES ('200', 'Lacus Consulting', 'id sapien. Cras dolor dolor, tempus non, lacinia at,', 'Nullam lobortis quam', '2', '4', '3', '2015-04-24 10:43:05', '2015-05-12 11:45:44', '56');

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
