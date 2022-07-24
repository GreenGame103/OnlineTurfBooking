/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - project
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`project` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `project`;

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(30) NOT NULL,
  `turf_id` int(11) DEFAULT NULL,
  `members` varchar(30) DEFAULT NULL,
  `date` date NOT NULL,
  `time` varchar(50) NOT NULL,
  `amount` float DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`booking_id`,`user_id`,`turf_id`,`members`,`date`,`time`,`amount`,`status`) values (1,3,1,'9s','2022-04-07','3',1400,'accepted'),(3,5,1,'7s','2022-03-30','10',1400,'accepted'),(4,5,2,'9s','2022-04-06','3',1400,'accepted'),(6,5,2,'7s','2022-04-13','3',1400,'accepted'),(7,6,3,'9s','2022-04-11','3',1400,'rejected'),(8,4,4,'9s','2022-04-12','3',1400,'accepted');

/*Table structure for table `card` */

DROP TABLE IF EXISTS `card`;

CREATE TABLE `card` (
  `cardid` int(11) NOT NULL AUTO_INCREMENT,
  `cno` varchar(50) DEFAULT NULL,
  `expiry` date DEFAULT NULL,
  `chname` varchar(50) DEFAULT NULL,
  `cvv` int(11) DEFAULT NULL,
  `balance` varchar(20) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`cardid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `card` */

insert  into `card`(`cardid`,`cno`,`expiry`,`chname`,`cvv`,`balance`,`userid`) values (1,'87654321','2022-08-01','manager',123,'16469500',1),(2,'12345678','2022-05-02','user',321,'13530500',2);

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`user_id`,`date`,`feedback`) values (1,3,'2022-04-07','not bad`'),(2,4,'2022-04-07','bad');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`user_name`,`password`,`type`) values (1,'admin','admin','admin'),(2,'sanjay@gmail.com','12345','manager'),(3,'satheesh@gmail.com','satheesh','user'),(4,'justin@gmail.com','justin','user'),(5,'vimal@gmail.com','vimal','user'),(6,'arjun@gmail.com','arjun','user'),(7,'neeraj@gmail.com','neeraj','manager'),(8,'akshay@gmail.com','akshay','manager');

/*Table structure for table `partner_request` */

DROP TABLE IF EXISTS `partner_request`;

CREATE TABLE `partner_request` (
  `partner_id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) DEFAULT NULL,
  `members` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`partner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `partner_request` */

insert  into `partner_request`(`partner_id`,`booking_id`,`members`,`status`) values (1,1,2,'pending');

/*Table structure for table `pr_user` */

DROP TABLE IF EXISTS `pr_user`;

CREATE TABLE `pr_user` (
  `ruid` int(11) NOT NULL AUTO_INCREMENT,
  `partner_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ruid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `pr_user` */

insert  into `pr_user`(`ruid`,`partner_id`,`user_id`) values (1,1,4);

/*Table structure for table `prop` */

DROP TABLE IF EXISTS `prop`;

CREATE TABLE `prop` (
  `prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `mail` varchar(40) DEFAULT NULL,
  `ph_no` varchar(11) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `hname` varchar(100) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`prop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `prop` */

insert  into `prop`(`prop_id`,`name`,`mail`,`ph_no`,`image`,`hname`,`place`,`post`,`pin`) values (2,'sanjay','sanjay@gmail.com','7909215813','/static/pic/220516-224042.jpg','pushpalayam','karimbam','karimbam','670141'),(7,'neeraj','neeraj@gmail.com','9074683559','/static/pic/220408-212731.jpg','neeraj house','moraza','moraza','670141'),(8,'akshay','akshay@gmail.com','9539310804','/static/pic/220517-000112.jpg','bbhouse','chuzhali','chuzhali','640141');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `rating` varchar(200) DEFAULT NULL,
  `turf_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`rating_id`,`user_id`,`date`,`rating`,`turf_id`) values (1,3,'2022-04-07','good \r\n',1),(2,4,'2022-04-07','good turf',1);

/*Table structure for table `tournament` */

DROP TABLE IF EXISTS `tournament`;

CREATE TABLE `tournament` (
  `tournament_id` int(11) NOT NULL AUTO_INCREMENT,
  `turf_id` int(11) DEFAULT NULL,
  `tournament_name` varchar(30) NOT NULL,
  `price` float NOT NULL,
  `date` date DEFAULT NULL,
  `details` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`tournament_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `tournament` */

insert  into `tournament`(`tournament_id`,`turf_id`,`tournament_name`,`price`,`date`,`details`) values (1,1,'startournament',15000,'2022-04-06','7s'),(2,5,'luckystar',15000,'2022-05-17','entry fee 1900');

/*Table structure for table `tournament_request1` */

DROP TABLE IF EXISTS `tournament_request1`;

CREATE TABLE `tournament_request1` (
  `tournament_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `tournament_id` int(11) DEFAULT NULL,
  `team_name` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`tournament_request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tournament_request1` */

insert  into `tournament_request1`(`tournament_request_id`,`user_id`,`tournament_id`,`team_name`,`date`,`status`) values (1,3,1,'superteam','2022-04-07','accepted'),(2,4,1,'bestteam','2022-04-07','accepted'),(3,5,1,'alakodeteam','2022-04-07','accepted'),(4,6,1,'arjunteam','2022-04-07','accepted'),(5,4,2,'fighters','2022-05-17','pending');

/*Table structure for table `tournament_shedule` */

DROP TABLE IF EXISTS `tournament_shedule`;

CREATE TABLE `tournament_shedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `tournament_id` int(11) DEFAULT NULL,
  `starting_date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `gametype` varchar(100) DEFAULT NULL,
  `team_1` varchar(100) DEFAULT NULL,
  `team_2` varchar(100) DEFAULT NULL,
  `break` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `winner` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tournament_shedule` */

insert  into `tournament_shedule`(`schedule_id`,`tournament_id`,`starting_date`,`time`,`gametype`,`team_1`,`team_2`,`break`,`status`,`winner`) values (1,1,'2022-04-08','10:00:00','Semi Finals','superteam','bestteam','5','winner is set','superteam'),(3,1,'2022-04-08','11:30:00','Semi Finals','alakodeteam','arjunteam','5','winner is set','arjunteam'),(4,1,'2022-04-11','10:20:00','Finals','superteam','arjunteam','10','winner is set','arjunteam'),(5,2,'2022-05-20','02:15:00','Semi Finals','Team 1','Team 2','5 min','pending','pending');

/*Table structure for table `tpayment` */

DROP TABLE IF EXISTS `tpayment`;

CREATE TABLE `tpayment` (
  `tpay` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `tid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `amt` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`tpay`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tpayment` */

insert  into `tpayment`(`tpay`,`userid`,`tid`,`date`,`amt`) values (1,3,1,'2022-04-07','15000.0'),(2,4,1,'2022-04-07','15000.0'),(3,5,1,'2022-04-07','15000.0'),(4,6,1,'2022-04-07','15000.0'),(5,4,2,'2022-05-17','15000.0');

/*Table structure for table `turf` */

DROP TABLE IF EXISTS `turf`;

CREATE TABLE `turf` (
  `turf_id` int(11) NOT NULL AUTO_INCREMENT,
  `turf_name` varchar(30) NOT NULL,
  `latitude` varchar(100) DEFAULT NULL,
  `Longitude` varchar(100) DEFAULT NULL,
  `ph_no` bigint(11) DEFAULT NULL,
  `prop_id` int(11) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `details` varchar(200) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `members` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`turf_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `turf` */

insert  into `turf`(`turf_id`,`turf_name`,`latitude`,`Longitude`,`ph_no`,`prop_id`,`image`,`details`,`price`,`time`,`members`) values (1,'carribeans','9.9312328','76.2673041',9546423532,2,'/static/pic/220407-034325.jpg','near by taliparamba',1000,'14:00','9s'),(2,'marakana','12.026227','75.3649476',9565222121,2,'/static/pic/220407-084948.jpg','7s,5s',100,'08:50','9s'),(3,'topturf','10.8505159','76.2710833',9523122165,2,'/static/pic/220407-090113.jpg','24hours',120,'09:06','9s'),(4,'Good days','12.02758','75.39245',9532415612,7,'/static/pic/220408-213313.jpg','24 houres',800,'21:30','9s'),(5,'san turf','9.9312328','76.2673041',9074683559,8,'/static/pic/220517-001035.jpg','5s ',1200,'04:10','9s');

/*Table structure for table `turfpayment` */

DROP TABLE IF EXISTS `turfpayment`;

CREATE TABLE `turfpayment` (
  `tupayid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `turfid` int(11) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`tupayid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `turfpayment` */

insert  into `turfpayment`(`tupayid`,`userid`,`turfid`,`amount`,`date`) values (1,3,1,1400,'2022-04-07'),(2,2,1,2500,'2022-04-07'),(3,5,1,1400,'2022-04-07'),(4,5,2,1400,'2022-04-07'),(5,4,2,1400,'2022-04-07'),(6,5,2,1400,'2022-04-07'),(8,4,4,1400,'2022-04-08');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(30) NOT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `ph_no` bigint(11) NOT NULL,
  `image` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  `hname` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`name`,`mail`,`ph_no`,`image`,`place`,`post`,`pin`,`hname`) values (3,'satheesh','satheesh@gmail.com',9074683559,'/static/pic/220407-032013.jpg','karimbam','karimbam','640141','rainbow'),(4,'justin','justin@gmail.com',9052658544,'/static/pic/220516-230010.jpg','trichambaram','trichambaram','640141','happyhouse'),(5,'vimal','vimal@gmail.com',9584256525,'/static/pic/220407-080824.jpg','alakode','alakode','670571','vimal house'),(6,'arjun','arjun@gmail.com',9385152451,'/static/pic/220407-081118.jpg','trichambaram','trichambaram','640141','arjun house');

/*Table structure for table `view_booking` */

DROP TABLE IF EXISTS `view_booking`;

CREATE TABLE `view_booking` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `turf_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `price` int(50) NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `view_booking` */

/*Table structure for table `winner_list` */

DROP TABLE IF EXISTS `winner_list`;

CREATE TABLE `winner_list` (
  `winner_id` int(11) NOT NULL AUTO_INCREMENT,
  `tournament_id` int(50) DEFAULT NULL,
  `winner` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`winner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `winner_list` */

insert  into `winner_list`(`winner_id`,`tournament_id`,`winner`) values (1,1,'arjunteam');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
