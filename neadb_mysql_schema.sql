CREATE TABLE `Route` (
	`idRoute` int(11) NOT NULL AUTO_INCREMENT,
	`BusNum` varchar(45) NOT NULL,
	`RouteLength` varchar(45) NOT NULL,
	PRIMARY KEY (`idRoute`)
);

CREATE TABLE `stop` (
	`idStop` int(11) NOT NULL AUTO_INCREMENT,
	`StopName` varchar(45) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (`idStop`)
);

CREATE TABLE `times` (
	`Primary key` int(11) NOT NULL AUTO_INCREMENT,
	`Routeid` int(11) NOT NULL,
	`Stopid` int(11) NOT NULL,
	`time` varchar(45) NOT NULL,
	PRIMARY KEY (`Primary key`)
);

ALTER TABLE `times` ADD CONSTRAINT `times_fk0` FOREIGN KEY (`Routeid`) REFERENCES `Route`(`idRoute`);

ALTER TABLE `times` ADD CONSTRAINT `times_fk1` FOREIGN KEY (`Stopid`) REFERENCES `stop`(`idStop`);

